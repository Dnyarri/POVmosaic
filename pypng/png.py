#!/usr/bin/env python

# png.py - PNG encoder/decoder in pure Python
#
# Copyright (C) 2006 Johann C. Rocholl <johann@browsershots.org>
# Portions Copyright (C) 2009 David Jones <drj@pobox.com>
# And probably portions Copyright (C) 2006 Nicko van Someren <nicko@nicko.org>
#
# Original concept by Johann C. Rocholl.
#
# LICENCE (MIT)
#
# Permission is hereby granted, free of charge, to any person
# obtaining a copy of this software and associated documentation files
# (the "Software"), to deal in the Software without restriction,
# including without limitation the rights to use, copy, modify, merge,
# publish, distribute, sublicense, and/or sell copies of the Software,
# and to permit persons to whom the Software is furnished to do so,
# subject to the following conditions:
#
# The above copyright notice and this permission notice shall be
# included in all copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND,
# EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF
# MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND
# NONINFRINGEMENT. IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT HOLDERS
# BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER IN AN
# ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN
# CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
# SOFTWARE.

"""
The ``png`` module can read and write PNG files.

Installation and Overview
-------------------------

``pip install pypng``

For help, type ``import png; help(png)`` in your python interpreter.

A good place to start is the :class:`Reader` and :class:`Writer` classes.

Coverage of PNG formats is fairly complete;
all allowable bit depths (1/2/4/8/16/24/32/48/64 bits per pixel) and
colour combinations are supported:

- greyscale (1/2/4/8/16 bit);
- RGB, RGBA, LA (greyscale with alpha) with 8/16 bits per channel;
- colour mapped images (1/2/4/8 bit).

Interlaced images,
originally intended for progressive display when downloading,
are supported for reading (but not for writing).

A number of optional chunks can be specified (when writing)
and understood (when reading): ``tRNS``, ``bKGD``, ``gAMA``.

The ``sBIT`` chunk can be used to specify precision for
non-native bit depths.

Requires Python 3.5 or higher.
Installation is trivial,
but see the ``README.txt`` file (with the source distribution) for details.

Full use of all features will need some reading of the PNG specification
https://www.w3.org/TR/2003/REC-PNG-20031110/.

The package also comes with command line utilities.

- ``pripamtopng`` converts
  `Netpbm <https://netpbm.sourceforge.net/>`_ PAM/PNM files to PNG;
- ``pripngtopam`` converts PNG to file PAM/PNM.

There are a few more for simple PNG manipulations.

Spelling and Terminology
------------------------

Generally British English spelling is used in the documentation.
So that's "greyscale" and "colour".
This not only matches the author's native language,
it's also used by the PNG specification.

Colour Models
-------------

The major colour models supported by PNG (and hence by PyPNG) are:

- greyscale;
- greyscale--alpha;
- RGB;
- RGB--alpha.

Also referred to using the abbreviations: L, LA, RGB, RGBA.
Each letter codes a single channel:
*L* is for Luminance or Luma or Lightness (greyscale images);
*A* stands for Alpha, the opacity channel
(used for transparency effects, but higher values are more opaque,
so it makes sense to call it opacity);
*R*, *G*, *B* stand for Red, Green, Blue (colour image).

Lists, arrays, sequences, and so on
-----------------------------------

When getting pixel data out of this module (reading) and
presenting data to this module (writing) there are
a number of ways the data could be represented as a Python value.

The preferred format is a sequence of *rows*,
which each row being a sequence of *values*.
In this format, the values are in pixel order,
with all the values from all the pixels in a row
being concatenated into a single sequence for that row.

Consider an image that is 3 pixels wide by 2 pixels high, and each pixel
has RGB components:

Sequence of rows::

  list([R,G,B, R,G,B, R,G,B],
       [R,G,B, R,G,B, R,G,B])

Each row appears as its own list,
but the pixels are flattened so that three values for one pixel
simply follow the three values for the previous pixel.

This is the preferred because
it provides a good compromise between space and convenience.
PyPNG regards itself as at liberty to replace any sequence type with
any sufficiently compatible other sequence type;
in practice each row is an array (``bytearray`` or ``array.array``).

To allow streaming the outer list is sometimes
an iterator rather than an explicit list.

An alternative format is a single array holding all the values.

Array of values::

  [R,G,B, R,G,B, R,G,B,
   R,G,B, R,G,B, R,G,B]

The entire image is one single giant sequence of colour values.
Generally an array will be used (to save space), not a list.

The top row comes first,
and within each row the pixels are ordered from left-to-right.
Within a pixel the values appear in the order R-G-B-A
(or L-A for greyscale--alpha).

There is another format, which should only be used with caution.
It is mentioned because it is used internally,
is close to what lies inside a PNG file itself,
and has some support from the public API.
This format is called *packed*.
When packed, each row is a sequence of bytes (integers from 0 to 255),
just as it is before PNG scanline filtering is applied.
When the bit depth is 8 this is the same as a sequence of rows;
when the bit depth is less than 8 (1, 2 and 4),
several pixels are packed into each byte;
when the bit depth is 16 each pixel value is decomposed into 2 bytes
(and *packed* is a misnomer).
This format is used by the `Writer.write_packed` method.
It isn't usually a convenient format,
but may be just right if the source data for
the PNG image comes from something that uses a similar format
(for example, 1-bit BMPs, or another PNG file).
"""

__version__ = "0.20250521.0"

import collections
import io  # For io.BytesIO
import itertools
import math
import re
import struct
import sys

# https://docs.python.org/3.5/library/warnings.html
import warnings
import zlib

from array import array


__all__ = ["ProtocolError", "Image", "Reader", "Writer", "write_chunks", "from_array"]


# The PNG signature.
# https://www.w3.org/TR/PNG/#5PNG-file-signature
signature = struct.pack("8B", 137, 80, 78, 71, 13, 10, 26, 10)

# The xstart, ystart, xstep, ystep for the Adam7 interlace passes.
adam7 = (
    (0, 0, 8, 8),
    (4, 0, 8, 8),
    (0, 4, 4, 8),
    (2, 0, 4, 4),
    (0, 2, 2, 4),
    (1, 0, 2, 2),
    (0, 1, 1, 2),
)


def adam7_generate(width, height):
    """
    Generate the coordinates for the reduced scanlines
    of an Adam7 interlaced image
    of size `width` by `height` pixels.

    Yields a generator for each pass,
    and each pass generator yields a series of (x, y, xstep) triples,
    each one identifying a reduced scanline consisting of
    pixels starting at (x, y) and taking every xstep pixel to the right.
    """

    for xstart, ystart, xstep, ystep in adam7:
        if xstart >= width:
            continue
        yield ((xstart, y, xstep) for y in range(ystart, height, ystep))


# Models the 'pHYs' chunk (used by the Reader)
Resolution = collections.namedtuple("_Resolution", "x y unit_is_meter")


def group(s, n):
    return list(zip(*[iter(s)] * n))


def isarray(x):
    return isinstance(x, array)


def check_palette(palette):
    """
    Check a palette argument (to the :class:`Writer` class) for validity.
    Returns the palette as a list if okay;
    raises an exception otherwise.
    """

    # None is the default and is allowed.
    if palette is None:
        return None

    p = list(palette)
    if not (0 < len(p) <= 256):
        raise ProtocolError(
            "a palette must have between 1 and 256 entries,"
            " see https://www.w3.org/TR/PNG/#11PLTE"
        )
    seen_triple = False
    for i, t in enumerate(p):
        if len(t) not in (3, 4):
            raise ProtocolError("palette entry %d: entries must be 3- or 4-tuples." % i)
        if len(t) == 3:
            seen_triple = True
        if seen_triple and len(t) == 4:
            raise ProtocolError(
                "palette entry %d: all 4-tuples must precede all 3-tuples" % i
            )
        for x in t:
            if int(x) != x or not (0 <= x <= 255):
                raise ProtocolError(
                    "palette entry %d: " "values must be integer: 0 <= x <= 255" % i
                )
    return p


def check_sizes(size, width, height):
    """
    Check that these arguments, if supplied, are consistent.
    Return a (width, height) pair.
    """

    if not size:
        return width, height

    if len(size) != 2:
        raise ProtocolError(
            "size argument should be a pair (width, height) instead is %r" % (size,)
        )
    if width is not None and width != size[0]:
        raise ProtocolError(
            "size[0] (%r) and width (%r) should match when both are used."
            % (size[0], width)
        )
    if height is not None and height != size[1]:
        raise ProtocolError(
            "size[1] (%r) and height (%r) should match when both are used."
            % (size[1], height)
        )
    return size


def check_color(c, greyscale, which):
    """
    Checks that a colour argument for transparent or background options
    is the right form.
    Returns the colour
    (which, if it's a bare integer, is "corrected" to a 1-tuple).
    """

    if c is None:
        return c
    if greyscale:
        try:
            len(c)
        except TypeError:
            c = (c,)
        if len(c) != 1:
            raise ProtocolError("%s for greyscale must be 1-tuple" % which)
        if not is_natural(c[0]):
            raise ProtocolError("%s colour for greyscale must be integer" % which)
    else:
        if not (
            len(c) == 3 and is_natural(c[0]) and is_natural(c[1]) and is_natural(c[2])
        ):
            raise ProtocolError("%s colour must be a triple of integers" % which)
    return c


class Error(Exception):
    def __str__(self):
        return self.__class__.__name__ + ": " + " ".join(self.args)


class FormatError(Error):
    """
    Problem with input file format.
    In other words, PNG file does not conform to
    the specification in some way and is invalid.
    """


class ProtocolError(Error):
    """
    Problem with the way the programming interface has been used,
    or the data presented to it.
    """


class ChunkError(FormatError):
    pass


class Default:
    """The default for the greyscale parameter."""


class Writer:
    """
    PNG encoder in pure Python.
    """

    def __init__(
        self,
        width=None,
        height=None,
        size=None,
        greyscale=Default,
        alpha=False,
        bitdepth=8,
        palette=None,
        transparent=None,
        background=None,
        gamma=None,
        compression=None,
        planes=None,
        colormap=None,
        maxval=None,
        chunk_limit=2 ** 20,
        physical=tuple(),
        x_pixels_per_unit=None,
        y_pixels_per_unit=None,
        unit_is_meter=False,
    ):
        """
        Create a PNG encoder object.

        Arguments:

        width, height
          Image size in pixels, as two separate arguments.
        size
          Image size (w,h) in pixels, as single argument.
        greyscale
          Pixels are greyscale, not RGB.
        alpha
          Input data has alpha channel (RGBA or LA).
        bitdepth
          Bit depth: from 1 to 16 (for each channel).
        palette
          Create a palette (PLTE chunk); enable colormap if it
          is not specified.
        transparent
          Specify a transparent colour (create a ``tRNS`` chunk).
        background
          Specify a default background colour (create a ``bKGD`` chunk).
        gamma
          Specify a gamma value (create a ``gAMA`` chunk).
        compression
          zlib compression level: in range 0 to 9, or -1, or None;
        planes
          Number of planes (values per pixel)
        colormap
          True for type 3 PNG (a palette is required)
        chunk_limit
          Write multiple ``IDAT`` chunks to save memory.
        physical
          Write ``pHYs`` chunk using 3 values in a list.
        x_pixels_per_unit
          Use *physical* argument instead.
        y_pixels_per_unit
          Use *physical* argument instead.
        unit_is_meter
          Use *physical* argument instead.

        The image size (in pixels) can be specified either by using the
        *width* and *height* arguments, or with the single *size*
        argument.
        If *size* is used it should be a pair (*width*, *height*).

        The *greyscale* argument indicates whether input pixels
        are greyscale (when true), or colour (when false).
        The default is true unless *palette* is used.

        The *alpha* argument (a boolean) specifies
        whether input pixels have an alpha channel (or not).

        *bitdepth* specifies the bit depth of the source pixel values.
        Each channel may have a different bit depth.
        Each source pixel must have values that are
        an integer between 0 and ``2**bitdepth-1``, where
        *bitdepth* is the bit depth for the corresponding channel.
        For example, 8-bit images have values between 0 and 255.
        PNG only stores images with bit depths of
        1,2,4,8, or 16 (the same for all channels).
        When *bitdepth* is not one of these values or where
        channels have different bit depths,
        the next highest valid bit depth is selected,
        and an ``sBIT`` (significant bits) chunk is generated
        that specifies the original precision of the source image.
        In this case the supplied pixel values will be rescaled to
        fit the range of the selected bit depth.

        The PNG file format supports many bit depth / colour model
        combinations, but not all.
        The details are somewhat arcane
        (refer to the PNG specification for full details).
        Briefly:
        Bit depths < 8 (1,2,4) are only allowed with greyscale and
        colour mapped images;
        colour mapped images cannot have bit depth 16.

        For colour mapped images
        (when the *colormap* argument is true,
        or has been implicitly made true via the *palette*
        argument)
        the *bitdepth* argument must match one of
        the valid PNG bit depths: 1, 2, 4, or 8.
        (It is valid to have a PNG image with a palette and
        an ``sBIT`` chunk, but the meaning is slightly different;
        it would be awkward to use the *bitdepth* argument for this.)

        The *colormap* option, when true,
        the PNG colour type is set to 3;
        *greyscale* must not be true; *alpha* must not be true;
        *transparent* must not be set.
        The bit depth must be 1,2,4, or 8.
        When a colour mapped image is created,
        the pixel values are palette indexes and
        the *bitdepth* argument specifies the size of these indexes
        (not the size of the colour values in the palette).

        The *palette* argument adds a palette.
        It also implicitly sets the *colormap* (to True) if
        the *colormap* option is defaulted
        (thus making a colour type 3 PNG).

        The palette argument value should be a sequence of 3- or
        4-tuples.
        3-tuples specify RGB palette entries;
        4-tuples specify RGBA palette entries.
        All the 4-tuples (if present) must come before all the 3-tuples.
        A ``PLTE`` chunk is created;
        if there are 4-tuples then a ``tRNS`` chunk is created as well.
        The ``PLTE`` chunk will contain all the RGB triples in the same
        sequence;
        the ``tRNS`` chunk will contain the alpha channel for
        all the 4-tuples, in the same sequence.
        Palette entries are always 8-bit.

        If specified, the *transparent* and *background* parameters must be
        a tuple with one element for each channel in the image.
        Either a 3-tuple of integer (RGB) values for a colour image, or
        a 1-tuple of a single integer for a greyscale image.

        If specified, the *gamma* parameter must be a positive number
        (generally, a `float`).
        A ``gAMA`` chunk will be created.
        Note that this will not change the values of the pixels as
        they appear in the PNG file,
        they are assumed to have already
        been converted appropriately for the gamma specified.

        The *compression* argument specifies the compression level.
        It is passed to the ``zlib`` module (unless it is `None`,
        in which case nothing is passed, and ``zlib`` defaults are used).
        Values from 1 to 9 (highest) specify compression.
        0 means no compression.
        -1 is the ``zlib`` default (and so will also be used
        when this argument is `None`) and indicates
        the default level of compression (which is generally acceptable).

        *chunk_limit* is used to limit the amount of memory used whilst
        compressing the image.
        In order to avoid using large amounts of memory,
        multiple ``IDAT`` chunks may be created.

        *physical* should be a list of up to 3 items: [xpp, ypp, ism].
        *xpp* is x-pixels-per-unit; *ypp* is y-pixels-per-unit
        (defaults to xpp if not present); *ism* is is-meter,
        ``True`` when the x- and y-resolutions are specified per meter
        (defaults to ``False`` if not present).

        *x_pixels_per_unit*
        *y_pixels_per_unit*
        *unit_is_meter*
        alternative to using *physical* keyword. *physical* will
        override these values.

        """

        # At the moment the `planes` argument is ignored;
        # its purpose is to act as a placeholder so that
        # ``Writer(x, y, **info)`` works, where `info` is a dictionary
        # returned by Reader.read and friends.

        width, height = check_sizes(size, width, height)
        del size

        if not is_natural(width) or not is_natural(height):
            raise ProtocolError("width and height must be integers")
        if width <= 0 or height <= 0:
            raise ProtocolError("width and height must be greater than zero")
        # https://www.w3.org/TR/PNG/#7Integers-and-byte-order
        if width > 2 ** 31 - 1 or height > 2 ** 31 - 1:
            raise ProtocolError("width and height cannot exceed 2**31-1")

        if alpha and transparent is not None:
            raise ProtocolError("transparent colour not allowed with alpha channel")

        # bitdepth is either single integer, or tuple of integers.
        # Convert to tuple.
        try:
            len(bitdepth)
        except TypeError:
            bitdepth = (bitdepth,)
        for b in bitdepth:
            valid = is_natural(b) and 1 <= b <= 16
            if not valid:
                raise ProtocolError(
                    "each bitdepth %r must be a positive integer <= 16" % (bitdepth,)
                )

        # Check palette, and coerce to list
        palette = check_palette(palette)

        # palette sets colormap only if colormap has been defaulted
        if colormap is None:
            colormap = bool(palette)

        # Check palette is available when colormap is true
        if colormap and not palette:
            raise ProtocolError("palette must be present when colormap is true")

        # Calculate channels, and
        # expand bitdepth to be one element per channel.
        alpha = bool(alpha)
        colormap = bool(colormap)
        if greyscale is Default and palette:
            greyscale = False
        greyscale = bool(greyscale)
        if colormap:
            color_planes = 1
            planes = 1
        else:
            color_planes = (3, 1)[greyscale]
            planes = color_planes + alpha
        if len(bitdepth) == 1:
            bitdepth *= planes

        bitdepth, self.rescale = check_bitdepth_rescale(
            colormap, bitdepth, transparent, alpha, greyscale
        )

        # These are assertions, because above logic should have
        # corrected or raised all problematic cases.
        if bitdepth < 8:
            assert greyscale or colormap
            assert not alpha
        if bitdepth > 8:
            assert not colormap

        transparent = check_color(transparent, greyscale, "transparent")
        background = check_color(background, greyscale, "background")

        if len(physical) == 0:
            pass
        elif len(physical) == 1:
            (x_pixels_per_unit,) = physical
            (y_pixels_per_unit,) = physical
        elif len(physical) == 2:
            x_pixels_per_unit, y_pixels_per_unit = physical
        elif len(physical) == 3:
            x_pixels_per_unit, y_pixels_per_unit, unit_is_meter = physical
        else:
            raise ProtocolError(
                "Too many items in `physical` parameter %r" % (physical,)
            )

        # It's important that the true boolean values
        # (greyscale, alpha, colormap) are converted
        # to bool because Iverson's convention is relied upon later on.
        self.width = width
        self.height = height
        self.transparent = transparent
        self.background = background
        self.gamma = gamma
        self.greyscale = greyscale
        self.alpha = alpha
        self.colormap = colormap
        self.bitdepth = int(bitdepth)
        self.compression = compression
        self.chunk_limit = chunk_limit
        self.palette = palette
        self.x_pixels_per_unit = x_pixels_per_unit
        self.y_pixels_per_unit = y_pixels_per_unit
        self.unit_is_meter = bool(unit_is_meter)

        self.color_type = 4 * self.alpha + 2 * (not greyscale) + 1 * self.colormap
        assert self.color_type in (0, 2, 3, 4, 6)

        self.color_planes = color_planes
        self.planes = planes
        # :todo: fix for bitdepth < 8
        self.psize = (self.bitdepth / 8) * self.planes

    def write(self, outfile, rows):
        """
        Write a PNG image to the output file.
        *rows* should be an iterable that yields each row
        (each row is a sequence of values).

        This method only consumes sufficient rows for the PNG
        file (``self.height`` rows).
        Extra rows are left unconsumed, but insufficient rows
        will raise a `ProtocolError`.
        Each row should have ``self.width * self.planes`` values.
        """

        # Values per row
        vpr = self.width * self.planes

        def check_rows(rows):
            """
            Yield each row in rows,
            but check each row first (for correct width).
            """
            for i, row in enumerate(rows):
                try:
                    wrong_length = len(row) != vpr
                except TypeError:
                    # When using an itertools.ichain object or
                    # other generator not supporting __len__,
                    # we set this to False to skip the check.
                    wrong_length = False
                if wrong_length:
                    # Note: row numbers start at 0.
                    raise ProtocolError(
                        "Expected %d values but got %d values, in row %d"
                        % (vpr, len(row), i)
                    )
                yield row

        return self.write_passes(outfile, check_rows(rows))

    def write_passes(self, outfile, rows):
        """
        Write a PNG image to the output file.

        Most users are expected to find the `write` or
        `write_array` method more convenient.

        The rows should be given to this method in the order that
        they appear in the output file.
        For straightlaced images, this is the usual top to bottom ordering.
        For interlaced images the rows should have been interlaced before
        passing them to this function (though PyPNG no longer
        writes interlaced images).

        *rows* should be an iterable that yields each row
        (each row being a sequence of values).
        """

        # Ensure rows are scaled (to 4-/8-/16-bit),
        # and packed into bytes.

        if self.rescale:
            rows = rescale_rows(rows, self.rescale)

        if self.bitdepth < 8:
            rows = pack_rows(rows, self.bitdepth)
        elif self.bitdepth == 16:
            rows = unpack_rows(rows)

        return self.write_packed(outfile, rows)

    def write_packed(self, outfile, rows):
        """
        Write PNG file to *outfile*.
        *rows* should be an iterator that yields each packed row;
        a packed row being a sequence of packed bytes.

        The rows have a filter byte prefixed and
        are then compressed into one or more ``IDAT`` chunks.
        They are not processed any further,
        so if bitdepth is other than 1, 2, 4, 8, 16,
        the pixel values should have been scaled
        before passing them to this method.

        For interlaced images (no longer written by PyPNG),
        the rows should be
        presented in the order that they appear in the file.
        """

        self.write_preamble(outfile)

        # https://www.w3.org/TR/PNG/#11IDAT
        if self.compression is not None:
            compressor = zlib.compressobj(self.compression)
        else:
            compressor = zlib.compressobj()

        # data accumulates bytes to be compressed for the IDAT chunk;
        # it's compressed when sufficiently large.
        data = array("B")

        # raise i scope out of the for loop. set to -1, because the for loop
        irows = iter(rows)
        for i in range(self.height):
            try:
                row = next(irows)
            except StopIteration:
                raise ProtocolError("Not enough rows: %d supplied; %d required" % (i, self.height))
            # Add "None" filter type.
            # Currently, it's essential that this filter type be used
            # for every scanline as
            # we do not mark the first row of a reduced pass image;
            # that means we could accidentally compute
            # the wrong filtered scanline if we used
            # "up", "average", or "paeth" on such a line.
            data.append(0)
            data.extend(row)
            if len(data) > self.chunk_limit:
                compressed = compressor.compress(data)
                if len(compressed):
                    write_chunk(outfile, b"IDAT", compressed)
                data = bytearray()

        compressed = compressor.compress(bytes(data))
        flushed = compressor.flush()
        if len(compressed) or len(flushed):
            write_chunk(outfile, b"IDAT", compressed + flushed)
        # https://www.w3.org/TR/PNG/#11IEND
        write_chunk(outfile, b"IEND")

    def write_preamble(self, outfile):
        # https://www.w3.org/TR/PNG/#5PNG-file-signature

        # This is the first write that is made when
        # writing a PNG file.
        # This one, and only this one, is checked for TypeError,
        # which generally indicates that we are writing bytes
        # into a text stream.
        try:
            outfile.write(signature)
        except TypeError as e:
            raise ProtocolError("PNG must be written to a binary stream") from e

        # https://www.w3.org/TR/PNG/#11IHDR
        interlace = 0
        write_chunk(
            outfile,
            b"IHDR",
            struct.pack(
                "!2I5B",
                self.width,
                self.height,
                self.bitdepth,
                self.color_type,
                0,
                0,
                interlace,
            ),
        )

        # See :chunk:order
        # https://www.w3.org/TR/PNG/#11gAMA
        if self.gamma is not None:
            write_chunk(
                outfile, b"gAMA", struct.pack("!L", int(round(self.gamma * 1e5)))
            )

        # See :chunk:order
        # https://www.w3.org/TR/PNG/#11sBIT
        if self.rescale:
            write_chunk(
                outfile,
                b"sBIT",
                struct.pack("%dB" % self.planes, *[s[0] for s in self.rescale]),
            )

        # :chunk:order: Without a palette (PLTE chunk),
        # ordering is relatively relaxed.
        # With one, gAMA chunk must precede PLTE chunk
        # which must precede tRNS and bKGD.
        # See https://www.w3.org/TR/PNG/#5ChunkOrdering
        if self.palette:
            p, t = make_palette_chunks(self.palette)
            write_chunk(outfile, b"PLTE", p)
            if t:
                # tRNS chunk is optional;
                # Only needed if palette entries have alpha.
                write_chunk(outfile, b"tRNS", t)

        # https://www.w3.org/TR/PNG/#11tRNS
        if self.transparent is not None:
            if self.greyscale:
                fmt = "!1H"
            else:
                fmt = "!3H"
            write_chunk(outfile, b"tRNS", struct.pack(fmt, *self.transparent))

        # https://www.w3.org/TR/PNG/#11bKGD
        if self.background is not None:
            if self.greyscale:
                fmt = "!1H"
            else:
                fmt = "!3H"
            write_chunk(outfile, b"bKGD", struct.pack(fmt, *self.background))

        # https://www.w3.org/TR/PNG/#11pHYs
        if self.x_pixels_per_unit is not None and self.y_pixels_per_unit is not None:
            tup = (
                self.x_pixels_per_unit,
                self.y_pixels_per_unit,
                int(self.unit_is_meter),
            )
            write_chunk(outfile, b"pHYs", struct.pack("!LLB", *tup))

    def write_array(self, outfile, pixels):
        """
        Write an array that holds all the image values
        as a PNG file on the output file.
        See also :meth:`write` method.
        """

        return self.write_passes(outfile, self.array_scanlines(pixels))

    def array_scanlines(self, pixels):
        """
        Generates rows (each a sequence of values) from
        a single array of values.
        """

        # Values per row
        vpr = self.width * self.planes
        stop = 0
        for y in range(self.height):
            start = stop
            stop = start + vpr
            yield pixels[start:stop]


def write_chunk(outfile, tag, data=b""):
    """
    Write a PNG chunk to the output file, including length and
    checksum.
    """

    data = bytes(data)
    # https://www.w3.org/TR/PNG/#5Chunk-layout
    outfile.write(struct.pack("!I", len(data)))
    outfile.write(tag)
    outfile.write(data)
    checksum = zlib.crc32(tag)
    checksum = zlib.crc32(data, checksum)
    checksum &= 2 ** 32 - 1
    outfile.write(struct.pack("!I", checksum))


def write_chunks(out, chunks):
    """Create a PNG file by writing out the chunks."""

    out.write(signature)
    for chunk in chunks:
        write_chunk(out, *chunk)


def rescale_rows(rows, rescale):
    """
    Take each row in rows (an iterator) and yield
    a fresh row with the pixels scaled according to
    the rescale parameters in the list `rescale`.
    Each element of `rescale` is a tuple of
    (source_bitdepth, target_bitdepth),
    with one element per channel.
    """

    # One factor for each channel
    fs = [float(2 ** s[1] - 1) / float(2 ** s[0] - 1) for s in rescale]

    # Assume all target_bitdepths are the same
    target_bitdepths = set(s[1] for s in rescale)
    assert len(target_bitdepths) == 1
    (target_bitdepth,) = target_bitdepths
    typecode = "BH"[target_bitdepth > 8]

    # Number of channels
    n_chans = len(rescale)

    for row in rows:
        rescaled_row = array(typecode, iter(row))
        for i in range(n_chans):
            channel = array(typecode, (int(round(fs[i] * x)) for x in row[i::n_chans]))
            rescaled_row[i::n_chans] = channel
        yield rescaled_row


def pack_rows(rows, bitdepth):
    """Yield packed rows that are a byte array.
    Each byte is packed with the values from several pixels.
    """

    assert bitdepth < 8
    assert 8 % bitdepth == 0

    # samples per byte
    spb = int(8 / bitdepth)

    def make_byte(block):
        """Take a block of (2, 4, or 8) values,
        and pack them into a single byte.
        """

        res = 0
        for v in block:
            res = (res << bitdepth) + v
        return res

    for row in rows:
        a = bytearray(row)
        # Adding padding bytes so we can group into a whole
        # number of spb-tuples.
        n = float(len(a))
        extra = math.ceil(n / spb) * spb - n
        a.extend([0] * int(extra))
        # Pack into bytes.
        # Each block is the samples for one byte.
        blocks = group(a, spb)
        yield bytearray(make_byte(block) for block in blocks)


def unpack_rows(rows):
    """Unpack each row from being 16-bits per value,
    to being a sequence of bytes.
    """
    for row in rows:
        fmt = "!%dH" % len(row)
        yield bytearray(struct.pack(fmt, *row))


def make_palette_chunks(palette):
    """
    Create the byte sequences for a ``PLTE`` and
    if necessary a ``tRNS`` chunk.
    Returned as a pair (*p*, *t*).
    *t* will be ``None`` if no ``tRNS`` chunk is necessary.
    """

    p = bytearray()
    t = bytearray()

    for x in palette:
        p.extend(x[0:3])
        if len(x) > 3:
            t.append(x[3])
    if t:
        return p, t
    return p, None


def check_bitdepth_rescale(colormap, bitdepth, transparent, alpha, greyscale):
    """
    Returns (bitdepth, rescale) pair.
    """

    if colormap:
        if len(bitdepth) != 1:
            raise ProtocolError("with colormap, only a single bitdepth may be used")
        (bitdepth,) = bitdepth
        if bitdepth not in (1, 2, 4, 8):
            raise ProtocolError("with colormap, bitdepth must be 1, 2, 4, or 8")
        if transparent is not None:
            raise ProtocolError("transparent and colormap not compatible")
        if alpha:
            raise ProtocolError("alpha and colormap not compatible")
        if greyscale:
            raise ProtocolError("greyscale and colormap not compatible")
        return bitdepth, None

    # No colormap, check for sBIT chunk generation.

    if greyscale and not alpha:
        # Single channel, L.
        (bitdepth,) = bitdepth
        if bitdepth in (1, 2, 4, 8, 16):
            return bitdepth, None
        if bitdepth > 8:
            targetbitdepth = 16
        elif bitdepth == 3:
            targetbitdepth = 4
        else:
            assert bitdepth in (5, 6, 7)
            targetbitdepth = 8
        return targetbitdepth, [(bitdepth, targetbitdepth)]

    assert alpha or not greyscale

    depth_set = tuple(set(bitdepth))
    if depth_set in [(8,), (16,)]:
        # No sBIT required.
        (bitdepth,) = depth_set
        return bitdepth, None

    targetbitdepth = (8, 16)[max(bitdepth) > 8]
    return targetbitdepth, [(b, targetbitdepth) for b in bitdepth]


# Regex for decoding mode string
RegexModeDecode = re.compile("(LA?|RGBA?);?([0-9]*)", flags=re.IGNORECASE)


def from_array(a, mode=None, info={}):
    """
    Create a PNG `Image` object from a 2-dimensional array.
    One application of this function is easy PIL-style saving:
    ``png.from_array(pixels, 'L').save('foo.png')``.

    Python doesn't really have 2-dimensional arrays,
    a sequence of sequences should be supplied (list of array,
    list of list, or similar).

    Unless they are specified using the *info* parameter,
    the PNG's height and width are taken from the array size.
    The height is the length of the sequence *a*;
    the width is the length of the first row divided by the
    number of channels.

    The argument *a* is assumed to be a sequence of rows,
    each row being a sequence of values (``width*channels`` in number).
    So an RGB image that is 20 pixels high and 32 wide will
    occupy a 2-dimensional array that is 20x96
    (each row will be 32*3 = 96 sample values).

    *mode* is a string that specifies the image colour format in a
    PIL-style mode.  It can be:

    ``'L'``
      greyscale (1 channel)
    ``'LA'``
      greyscale with alpha (2 channel)
    ``'RGB'``
      colour image (3 channel)
    ``'RGBA'``
      colour image with alpha (4 channel)

    The bit depth defaults to 8, but can be changed by
    appending ``';16'`` to *mode*;
    any decimal from 1 to 16 can be used to specify the bit depth.

    *mode* determines how many channels the image has, and
    so allows the width to be derived from the row length
    (the second array dimension).

    Canonically the argument *a* is a list of lists:
    ``png.from_array([[0, 255, 0], [255, 0, 255]], 'L')``.
    Other forms may be suitable, particular if they are made
    from Python Standard Library types.
    The exact rules are: ``len(a)`` gives the first dimension, height;
    ``len(a[0])`` gives the second dimension.
    It's slightly more complicated than that because
    an iterator of rows can be used, and it all still works.
    Using an iterator allows data to be streamed efficiently.

    The *info* parameter is a dictionary that can
    be used to specify metadata (in the same style as
    the arguments to the `png.Writer` class).
    For this function the keys that are useful are:

    height
      overrides the height derived from the array dimensions and
      allows *a* to be an iterable.
    width
      overrides the width derived from the array dimensions.
    bitdepth
      select bit depth
      (must match *mode* if that also specifies a bit depth).

    Generally anything specified in the *info* dictionary will
    override any implicit choices that this function would otherwise make,
    but must match any explicit ones.
    For example, if the *info* dictionary has a ``greyscale`` key then
    this must be true when mode is ``'L'`` or ``'LA'`` and
    false when mode is ``'RGB'`` or ``'RGBA'``.
    """

    # We abuse the *info* parameter by modifying it.  Take a copy here.
    # (Also typechecks *info* to some extent).
    info = dict(info)

    # Syntax check mode string.
    match = RegexModeDecode.match(mode)
    if not match:
        raise Error("mode string should be 'RGB' or 'L;16' or similar.")

    mode, bitdepth = match.groups()
    if bitdepth:
        bitdepth = int(bitdepth)

    # Colour format.
    if "greyscale" in info:
        if bool(info["greyscale"]) != ("L" in mode):
            raise ProtocolError("info['greyscale'] should match mode.")
    info["greyscale"] = "L" in mode

    alpha = "A" in mode
    if "alpha" in info:
        if bool(info["alpha"]) != alpha:
            raise ProtocolError("info['alpha'] should match mode.")
    info["alpha"] = alpha

    # Get bitdepth from *mode* if possible.
    if bitdepth:
        if info.get("bitdepth") and bitdepth != info["bitdepth"]:
            raise ProtocolError(
                "bitdepth (%d) should match bitdepth of info (%d)."
                % (bitdepth, info["bitdepth"])
            )
        info["bitdepth"] = bitdepth

    # Fill in and/or check entries in *info*.
    # Dimensions.
    width = info.get("width")

    if "height" not in info:
        try:
            info["height"] = len(a)
        except TypeError:
            raise ProtocolError("len(a) does not work, supply info['height'] instead.")
    height = info["height"]

    planes = len(mode)
    if "planes" in info:
        if info["planes"] != planes:
            raise Error("info['planes'] should match mode.")

    # The first row is required to derive width and bitdepth.
    # Which is why we need a copy of its iterator.
    a, t = itertools.tee(a)
    row = next(t)
    del t

    if "width" not in info:
        width = len(row) // planes
        info["width"] = width

    if "bitdepth" not in info:
        bitdepth = 8
        info["bitdepth"] = bitdepth

    for thing in ["width", "height", "bitdepth", "greyscale", "alpha"]:
        assert thing in info

    return Image(a, info)


# So that refugee's from PIL feel more at home.  Not documented.
fromarray = from_array


class Image:
    """A PNG image.  You can create an :class:`Image` object from
    an array of pixels by calling :meth:`png.from_array`.  It can be
    saved to disk with the :meth:`save` method.
    """

    def __init__(self, rows, info):
        """
        .. note ::

          The constructor is not public.  Please do not call it.
        """

        self.rows = rows
        self.info = info

    def save(self, file):
        """Save the image to the named *file*.

        See `.write()` if you already have an open file object.

        In general, you can only call this method once;
        after it has been called the first time the PNG image is written,
        the source data will have been streamed, and
        cannot be streamed again.
        """

        w = Writer(**self.info)

        with open(file, "wb") as fd:
            w.write(fd, self.rows)

    def stream(self):
        """Stream the rows into a list, so that the rows object
        can be accessed multiple times, or randomly.
        """

        self.rows = list(self.rows)

    def write(self, file):
        """Write the image to the open file object.

        See `.save()` if you have a filename.

        In general, you can only call this method once;
        after it has been called the first time the PNG image is written,
        the source data will have been streamed, and
        cannot be streamed again.
        """

        w = Writer(**self.info)
        w.write(file, self.rows)


class Reader:
    """
    Pure Python PNG decoder in pure Python.
    """

    def __init__(self, _guess=None, filename=None, file=None, bytes=None):
        """
        The constructor expects exactly one keyword argument.
        If you supply a positional argument instead,
        it will guess the input type.
        Choose from the following keyword arguments:

        filename
          Name of input file (a PNG file).
        file
          A file-like object (object with a read() method).
        bytes
          ``bytes`` or ``bytearray`` with PNG data.

        """
        keywords_supplied = (
            (_guess is not None)
            + (filename is not None)
            + (file is not None)
            + (bytes is not None)
        )
        if keywords_supplied != 1:
            raise TypeError("Reader() takes exactly 1 argument")

        # Will be the first 8 bytes, later on.  See validate_signature.
        self.signature = None
        self.transparent = None
        # A pair of (len,type) if a chunk has been read but its data and
        # checksum have not (in other words the file position is just
        # past the 4 bytes that specify the chunk type).
        # See preamble method for how this is used.
        self.atchunk = None

        if _guess is not None:
            if isarray(_guess):
                bytes = _guess
            elif isinstance(_guess, str):
                filename = _guess
            elif hasattr(_guess, "read"):
                file = _guess

        if bytes is not None:
            self.file = io.BytesIO(bytes)
        elif filename is not None:
            self.file = open(filename, "rb")
        elif file is not None:
            self.file = file
        else:
            raise ProtocolError("expecting filename, file or bytes array")

    def chunk(self):
        """
        Read the next PNG chunk from the input file;
        returns a (*type*, *data*) tuple.
        *type* is the chunk's type as a byte string
        (all PNG chunk types are 4 bytes long).
        *data* is the chunk's data content, as a byte string.
        """

        self.validate_signature()

        # https://www.w3.org/TR/PNG/#5Chunk-layout
        if not self.atchunk:
            self.atchunk = self._chunk_len_type()
        if not self.atchunk:
            raise ChunkError("No more chunks.")
        length, type = self.atchunk
        self.atchunk = None

        data = self.file.read(length)
        if len(data) != length:
            raise ChunkError(
                "Chunk %s too short for required %i octets." % (type, length)
            )

        checksum = self.file.read(4)
        if len(checksum) != 4:
            raise ChunkError("Chunk %s too short for checksum." % type)
        verify = zlib.crc32(type)
        verify = zlib.crc32(data, verify)
        verify = struct.pack("!I", verify)

        if checksum != verify:
            (a,) = struct.unpack("!I", checksum)
            (b,) = struct.unpack("!I", verify)
            message = "Checksum error in %s chunk: 0x%08X != 0x%08X." % (
                type.decode("ascii"),
                a,
                b,
            )
            warnings.warn(message, RuntimeWarning)

        return type, data

    def chunks(self):
        """Return an iterator that will yield each chunk as a
        (*chunktype*, *content*) pair.
        """

        while True:
            t, v = self.chunk()
            yield t, v
            if t == b"IEND":
                break

    def chunk_of_type(self, type):
        """Return the next chunk of the given type, which is a 4
        character ASCII string.
        Raises an error if the chunk is not found.
        """

        target = bytes(type, "ascii")

        while True:
            t, v = self.chunk()
            if t == target:
                return t, v

    def undo_filter(self, filter_type, scanline, previous):
        """
        Undo the filter for a scanline.
        *scanline* is a sequence of bytes that
        does not include the initial filter type byte.
        *previous* is decoded previous scanline
        (for straightlaced images this is the previous pixel row,
        but for interlaced images, it is
        the previous scanline in the reduced image,
        which in general is not the previous pixel row in the final image).
        When there is no previous scanline
        (the first row of a straightlaced image,
        or the first row in one of the passes in an interlaced image),
        then this argument should be ``None``.

        The scanline will have the effects of filtering removed;
        the result will be returned as a fresh sequence of bytes.
        """

        # :todo: Would it be better to update scanline in place?
        result = scanline

        if filter_type == 0:
            return result

        if filter_type not in (1, 2, 3, 4):
            raise FormatError(
                "Invalid PNG Filter Type.  "
                "See https://www.w3.org/TR/2003/REC-PNG-20031110/#9Filters ."
            )

        # Filter unit.  The stride from one pixel to the corresponding
        # byte from the previous pixel.  Normally this is the pixel
        # size in bytes, but when this is smaller than 1, the previous
        # byte is used instead.
        fu = max(1, self.psize)

        # For the first line of a pass, synthesize a placeholder previous
        # line.  An alternative approach would be to observe that on the
        # first line 'up' is the same as 'null', 'paeth' is the same
        # as 'sub', with only 'average' requiring any special case.
        if not previous:
            previous = bytearray([0] * len(scanline))

        # Call appropriate filter algorithm.  Note that 0 has already
        # been dealt with.
        fn = (
            None,
            undo_filter_sub,
            undo_filter_up,
            undo_filter_average,
            undo_filter_paeth,
        )[filter_type]
        fn(fu, scanline, previous, result)
        return result

    def _deinterlace(self, raw):
        """
        Read raw pixel data, undo filters, deinterlace, and flatten.
        Return a single array of values.
        """

        # Values per row (of the target image)
        vpr = self.width * self.planes

        # Values per image
        vpi = vpr * self.height
        # Interleaving writes to the output array randomly
        # (well, not quite), so the entire output array must be in memory.
        # Make a result array, and make it big enough.
        if self.bitdepth > 8:
            a = array("H", [0] * vpi)
        else:
            a = bytearray([0] * vpi)
        source_offset = 0

        for lines in adam7_generate(self.width, self.height):
            # The previous (reconstructed) scanline.
            # `None` at the beginning of a pass
            # to indicate that there is no previous line.
            recon = None
            for x, y, xstep in lines:
                # Pixels per row (reduced pass image)
                ppr = int(math.ceil((self.width - x) / float(xstep)))
                # Row size in bytes for this pass.
                row_size = int(math.ceil(self.psize * ppr))

                filter_type = raw[source_offset]
                source_offset += 1
                scanline = raw[source_offset : source_offset + row_size]
                source_offset += row_size
                recon = self.undo_filter(filter_type, scanline, recon)
                # Convert so that there is one element per pixel value
                flat = self._bytes_to_values(recon, width=ppr)
                if xstep == 1:
                    assert x == 0
                    offset = y * vpr
                    a[offset : offset + vpr] = flat
                else:
                    offset = y * vpr + x * self.planes
                    end_offset = (y + 1) * vpr
                    skip = self.planes * xstep
                    for i in range(self.planes):
                        a[offset + i : end_offset : skip] = flat[i :: self.planes]

        return a

    def _iter_bytes_to_values(self, byte_rows):
        """
        Iterator that yields each scanline;
        each scanline being a sequence of values.
        `byte_rows` should be an iterator that yields
        the bytes of each row in turn.
        """

        for row in byte_rows:
            yield self._bytes_to_values(row)

    def _bytes_to_values(self, bs, width=None):
        """Convert a packed row of bytes into a row of values.
        Result will be a freshly allocated object,
        not shared with the argument.
        """

        if self.bitdepth == 8:
            return bytearray(bs)
        if self.bitdepth == 16:
            return array("H", struct.unpack("!%dH" % (len(bs) // 2), bs))

        assert self.bitdepth < 8
        if width is None:
            width = self.width
        # Samples per byte
        spb = 8 // self.bitdepth
        out = bytearray()
        mask = 2 ** self.bitdepth - 1
        shifts = [self.bitdepth * i for i in reversed(range(spb))]
        for o in bs:
            out.extend([mask & (o >> i) for i in shifts])
        return out[:width]

    def _iter_straight_packed(self, byte_blocks):
        """Iterator that undoes the effect of filtering;
        yields each row as a sequence of packed bytes.
        Assumes input is straightlaced.
        `byte_blocks` should be an iterable that yields the raw bytes
        in blocks of arbitrary size.
        """

        # length of row, in bytes
        rb = self.row_bytes
        a = bytearray()
        # The previous (reconstructed) scanline.
        # None indicates first line of image.
        recon = None
        for some_bytes in byte_blocks:
            a.extend(some_bytes)
            while len(a) >= rb + 1:
                filter_type = a[0]
                scanline = a[1 : rb + 1]
                del a[: rb + 1]
                recon = self.undo_filter(filter_type, scanline, recon)
                yield recon
        if len(a) != 0:
            # :file:format We get here with a file format error:
            # when the available bytes (after decompressing) do not
            # pack into exact rows.
            raise FormatError("Wrong size for decompressed IDAT chunk.")
        assert len(a) == 0

    def validate_signature(self):
        """
        If signature (header) has not been read then read and
        validate it; otherwise do nothing.
        No signature (empty read()) will raise EOFError;
        An invalid signature will raise FormatError.
        EOFError is raised to make possible the case where
        a program can read multiple PNG files from the same stream.
        The end of the stream can be distinguished from non-PNG files
        or corrupted PNG files.
        """

        if self.signature:
            return
        self.signature = self.file.read(8)
        if len(self.signature) == 0:
            raise EOFError("End of PNG stream.")
        if self.signature != signature:
            raise FormatError("PNG file has invalid signature.")

    def preamble(self):
        """
        Extract the image metadata by reading
        the initial part of the PNG file up to
        the start of the ``IDAT`` chunk.
        All the chunks that precede the ``IDAT`` chunk are
        read and either processed for metadata or discarded.
        """

        self.validate_signature()

        while True:
            if not self.atchunk:
                self.atchunk = self._chunk_len_type()
                if self.atchunk is None:
                    raise FormatError("This PNG file has no IDAT chunks.")
            if self.atchunk[1] == b"IDAT":
                return
            self.process_chunk()

    def _chunk_len_type(self):
        """
        Reads just enough of the input to
        determine the next chunk's length and type;
        return a (*length*, *type*) pair where *type* is a byte sequence.
        If there are no more chunks, ``None`` is returned.
        """

        x = self.file.read(8)
        if not x:
            return None
        if len(x) != 8:
            raise FormatError("End of file whilst reading chunk length and type.")
        length, type = struct.unpack("!I4s", x)
        if length > 2 ** 31 - 1:
            raise FormatError("Chunk %s is too large: %d." % (type, length))
        # Check that all bytes are in valid ASCII range.
        # https://www.w3.org/TR/2003/REC-PNG-20031110/#5Chunk-layout
        type_bytes = set(bytearray(type))
        if not (type_bytes <= set(range(65, 91)) | set(range(97, 123))):
            raise FormatError("Chunk %r has invalid Chunk Type." % list(type))
        return length, type

    def process_chunk(self):
        """
        Process the next chunk and its data.
        This only processes the following chunk types:
        ``IHDR``, ``PLTE``, ``bKGD``, ``tRNS``, ``gAMA``, ``sBIT``, ``pHYs``.
        All other chunk types are ignored.
        """

        type, data = self.chunk()
        method = "_process_" + type.decode("ascii")
        m = getattr(self, method, None)
        if m:
            m(data)

    def _process_IHDR(self, data):
        # https://www.w3.org/TR/PNG/#11IHDR
        if len(data) != 13:
            raise FormatError("IHDR chunk has incorrect length.")
        (
            self.width,
            self.height,
            self.bitdepth,
            self.color_type,
            self.compression,
            self.filter,
            self.interlace,
        ) = struct.unpack("!2I5B", data)

        check_bitdepth_colortype(self.bitdepth, self.color_type)

        if self.compression != 0:
            raise FormatError("Unknown compression method %d" % self.compression)
        if self.filter != 0:
            raise FormatError(
                "Unknown filter method %d,"
                " see https://www.w3.org/TR/2003/REC-PNG-20031110/#9Filters ."
                % self.filter
            )
        if self.interlace not in (0, 1):
            raise FormatError(
                "Unknown interlace method %d, see "
                "https://www.w3.org/TR/2003/REC-PNG-20031110/#8InterlaceMethods"
                " ." % self.interlace
            )

        # Derived values
        # https://www.w3.org/TR/PNG/#6Colour-values
        colormap = bool(self.color_type & 1)
        greyscale = not (self.color_type & 2)
        alpha = bool(self.color_type & 4)
        color_planes = (3, 1)[greyscale or colormap]
        planes = color_planes + alpha

        self.colormap = colormap
        self.greyscale = greyscale
        self.alpha = alpha
        self.color_planes = color_planes
        self.planes = planes
        self.psize = float(self.bitdepth) / float(8) * planes
        if int(self.psize) == self.psize:
            self.psize = int(self.psize)
        self.row_bytes = int(math.ceil(self.width * self.psize))
        # Stores PLTE chunk if present, and is used to check
        # chunk ordering constraints.
        self.plte = None
        # Stores tRNS chunk if present, and is used to check chunk
        # ordering constraints.
        self.trns = None
        # Stores sBIT chunk if present.
        self.sbit = None

    def _process_PLTE(self, data):
        # https://www.w3.org/TR/PNG/#11PLTE
        if self.plte:
            warnings.warn("Multiple PLTE chunks present.")
        self.plte = data
        if len(data) % 3 != 0:
            raise FormatError("PLTE chunk's length should be a multiple of 3.")
        if len(data) > (2 ** self.bitdepth) * 3:
            raise FormatError("PLTE chunk is too long.")
        if len(data) == 0:
            raise FormatError("Empty PLTE is not allowed.")

    def _process_bKGD(self, data):
        try:
            if self.colormap:
                if not self.plte:
                    warnings.warn("PLTE chunk is required before bKGD chunk.")
                self.background = struct.unpack("B", data)
            else:
                self.background = struct.unpack("!%dH" % self.color_planes, data)
        except struct.error:
            raise FormatError("bKGD chunk has incorrect length.")

    def _process_tRNS(self, data):
        # https://www.w3.org/TR/PNG/#11tRNS
        self.trns = data
        if self.colormap:
            if not self.plte:
                warnings.warn("PLTE chunk is required before tRNS chunk.")
            else:
                if len(data) > len(self.plte) / 3:
                    # Was warning, but promoted to Error as it
                    # would otherwise cause pain later on.
                    raise FormatError("tRNS chunk is too long.")
        else:
            if self.alpha:
                raise FormatError(
                    "tRNS chunk is not valid with colour type %d." % self.color_type
                )
            try:
                self.transparent = struct.unpack("!%dH" % self.color_planes, data)
            except struct.error:
                raise FormatError("tRNS chunk has incorrect length.")

    def _process_gAMA(self, data):
        try:
            self.gamma = struct.unpack("!L", data)[0] / 100000.0
        except struct.error:
            raise FormatError("gAMA chunk has incorrect length.")

    def _process_sBIT(self, data):
        self.sbit = data
        if (
            self.colormap
            and len(data) != 3
            or not self.colormap
            and len(data) != self.planes
        ):
            raise FormatError("sBIT chunk has incorrect length.")

    def _process_pHYs(self, data):
        # https://www.w3.org/TR/PNG/#11pHYs
        self.phys = data
        fmt = "!LLB"
        if len(data) != struct.calcsize(fmt):
            raise FormatError("pHYs chunk has incorrect length.")
        self.x_pixels_per_unit, self.y_pixels_per_unit, unit = struct.unpack(fmt, data)
        self.unit_is_meter = bool(unit)

    def read(self):
        """
        Read the PNG file and decode it.
        Returns (*width*, *height*, *rows*, *info*).

        May use excessive memory.

        *rows* is a sequence of rows;
        each row is a sequence of values.
        """

        def iteridat():
            """Iterator that yields all the ``IDAT`` chunks as strings."""
            while True:
                type, data = self.chunk()
                if type == b"IEND":
                    # https://www.w3.org/TR/PNG/#11IEND
                    break
                if type != b"IDAT":
                    continue
                # type == b'IDAT'
                # https://www.w3.org/TR/PNG/#11IDAT
                if self.colormap and not self.plte:
                    warnings.warn("PLTE chunk is required before IDAT chunk")
                yield data

        self.preamble()
        raw = decompress(iteridat())

        if self.interlace:

            def rows_from_interlace():
                """Yield each row from an interlaced PNG."""
                # It's important that this iterator doesn't read
                # IDAT chunks until it yields the first row.
                bs = bytearray(itertools.chain(*raw))
                arraycode = "BH"[self.bitdepth > 8]
                # Like :meth:`group` but
                # producing an array.array object for each row.
                values = self._deinterlace(bs)
                vpr = self.width * self.planes
                for i in range(0, len(values), vpr):
                    row = array(arraycode, values[i : i + vpr])
                    yield row

            rows = rows_from_interlace()
        else:
            rows = self._iter_bytes_to_values(self._iter_straight_packed(raw))
        info = dict()
        for attr in "greyscale alpha planes bitdepth".split():
            info[attr] = getattr(self, attr)
        info["size"] = (self.width, self.height)
        for attr in "gamma transparent background".split():
            a = getattr(self, attr, None)
            if a is not None:
                info[attr] = a
        if getattr(self, "x_pixels_per_unit", None):
            info["physical"] = Resolution(
                self.x_pixels_per_unit, self.y_pixels_per_unit, self.unit_is_meter
            )
        if self.plte:
            info["palette"] = self.palette()
        return self.width, self.height, rows, info

    def read_flat(self):
        """
        Read a PNG file and decode it into a single array of values.
        Returns (*width*, *height*, *values*, *info*).

        May use excessive memory.

        *values* is a single array.

        The `read` method is more stream-friendly than this,
        because it returns a sequence of rows.
        """

        x, y, pixel, info = self.read()
        arraycode = "BH"[info["bitdepth"] > 8]
        pixel = array(arraycode, itertools.chain(*pixel))
        return x, y, pixel, info

    def palette(self, alpha="natural"):
        """
        Returns a palette that is a sequence of 3-tuples or 4-tuples,
        synthesizing it from the ``PLTE`` and ``tRNS`` chunks.
        These chunks should have already been processed (for example,
        by calling the `preamble` method).
        All the tuples are the same size:
        3-tuples if there is no ``tRNS`` chunk,
        4-tuples when there is a ``tRNS`` chunk.

        Assumes that the image is colour type
        3 and therefore a ``PLTE`` chunk is required.

        If the *alpha* argument is ``'force'`` then an alpha channel is
        always added, forcing the result to be a sequence of 4-tuples.
        """

        if not self.plte:
            raise FormatError("Required PLTE chunk is missing in colour type 3 image.")
        plte = group(array("B", self.plte), 3)
        if self.trns or alpha == "force":
            trns = array("B", self.trns or [])
            trns.extend([255] * (len(plte) - len(trns)))
            plte = [pal + (a,) for pal, a in zip(plte, trns)]
        return plte

    def asDirect(self):
        """
        Returns the image data as a direct representation of
        an ``x * y * planes`` array.
        This removes the need for callers to deal with
        palettes and transparency themselves.
        Images with a palette (colour type 3) are converted to RGB or RGBA;
        images with transparency (a ``tRNS`` chunk) are converted to
        LA or RGBA as appropriate.
        When returned in this format the pixel values represent
        the colour value directly without needing to refer
        to palettes or transparency information.

        Like the `read` method this method returns a 4-tuple:

        (*width*, *height*, *rows*, *info*)

        This method returns pixel values with
        the bit depth they have in the source image.

        The *info* dictionary that is returned reflects
        the *direct* format and not the original source image.
        For example, an RGB source image with a ``tRNS`` chunk
        to represent a transparent colour,
        will start with ``planes=3`` and ``alpha=False`` for the
        source image,
        but the *info* dictionary returned by this method
        will have ``planes=4`` and ``alpha=True`` because
        an alpha channel is synthesized and added.

        *rows* is a sequence of rows;
        each row being a sequence of values
        (like the :meth:`read` method).

        All the other aspects of the image data are not changed.
        """

        self.preamble()

        # Simple case, no conversion necessary.
        if not self.colormap and not self.trns and not self.sbit:
            return self.read()

        x, y, pixels, info = self.read()

        if self.colormap:
            info["colormap"] = False
            info["alpha"] = bool(self.trns)
            info["bitdepth"] = 8
            info["planes"] = 3 + bool(self.trns)
            palette = self.palette()

            def iterpal(pixels):
                for row in pixels:
                    row = [palette[x] for x in row]
                    yield array("B", itertools.chain(*row))

            pixels = iterpal(pixels)
        elif self.trns:
            # It would be nice if there was some reasonable way
            # of doing this without generating a whole load of
            # intermediate tuples.  But tuples does seem like the
            # easiest way, with no other way clearly much simpler or
            # much faster.  (Actually, the L to LA conversion could
            # perhaps go faster (all those 1-tuples!), but I still
            # wonder whether the code proliferation is worth it)
            it = self.transparent
            maxval = 2 ** info["bitdepth"] - 1
            planes = info["planes"]
            info["alpha"] = True
            info["planes"] += 1
            del info["transparent"]
            typecode = "BH"[info["bitdepth"] > 8]

            def itertrns(pixels):
                for row in pixels:
                    # For each row we group it into pixels, then form a
                    # characterisation vector that says whether each
                    # pixel is opaque or not.  Then we convert
                    # True/False to 0/maxval (by multiplication),
                    # and add it as the extra channel.
                    row = group(row, planes)
                    opa = [maxval * (pix != it) for pix in row]
                    yield array(
                        typecode,
                        itertools.chain(*[pix + (a,) for pix, a in zip(row, opa)]),
                    )

            pixels = itertrns(pixels)

        return x, y, pixels, info

    def asRGB(self):
        """
        Return image as RGB pixels.
        RGB colour images are passed through unchanged;
        greyscales are expanded into RGB triplets
        (there is a small speed overhead for doing this).

        An alpha channel in the source image will raise an exception.

        The return values are as for the :meth:`read` method except that
        the *info* reflect the returned pixels, not the source image.
        In particular,
        for this method ``info['greyscale']`` will be ``False``.
        """

        width, height, pixels, info = self.asDirect()
        if info["alpha"]:
            raise Error("will not convert image with alpha channel to RGB")
        if not info["greyscale"]:
            return width, height, pixels, info
        info["greyscale"] = False
        info["planes"] = 3

        if info["bitdepth"] > 8:

            def newarray():
                return array("H", [0])

        else:

            def newarray():
                return bytearray([0])

        def iterrgb():
            for row in pixels:
                a = newarray() * 3 * width
                for i in range(3):
                    a[i::3] = row
                yield a

        return width, height, iterrgb(), info

    def asRGBA(self):
        """
        Return image as RGBA pixels.
        Greyscales are expanded into RGB triplets;
        an alpha channel is synthesized if necessary.
        The return values are as for the :meth:`read` method except that
        the *info* reflect the returned pixels, not the source image.
        In particular, for this method
        ``info['greyscale']`` will be ``False``, and
        ``info['alpha']`` will be ``True``.
        """

        width, height, pixels, info = self.asDirect()
        if info["alpha"] and not info["greyscale"]:
            return width, height, pixels, info
        typecode = "BH"[info["bitdepth"] > 8]
        maxval = 2 ** info["bitdepth"] - 1
        maxbuffer = struct.pack("=" + typecode, maxval) * 4 * width

        if info["bitdepth"] > 8:

            def newarray():
                return array("H", maxbuffer)

        else:

            def newarray():
                return bytearray(maxbuffer)

        if info["alpha"] and info["greyscale"]:
            # LA to RGBA
            def convert():
                for row in pixels:
                    # Create a fresh target row, then copy L channel
                    # into first three target channels, and A channel
                    # into fourth channel.
                    a = newarray()
                    convert_la_to_rgba(row, a)
                    yield a

        elif info["greyscale"]:
            # L to RGBA
            def convert():
                for row in pixels:
                    a = newarray()
                    convert_l_to_rgba(row, a)
                    yield a

        else:
            assert not info["alpha"] and not info["greyscale"]
            # RGB to RGBA

            def convert():
                for row in pixels:
                    a = newarray()
                    convert_rgb_to_rgba(row, a)
                    yield a

        info["alpha"] = True
        info["greyscale"] = False
        info["planes"] = 4
        return width, height, convert(), info


def decompress(data_blocks):
    """
    `data_blocks` should be an iterable that
    yields the compressed data (from the ``IDAT`` chunks).
    This yields decompressed byte strings.
    """

    # Currently, with no max_length parameter to decompress,
    # this routine will do one yield per IDAT chunk: Not very
    # incremental.
    d = zlib.decompressobj()
    # Each IDAT chunk is passed to the decompressor, then any
    # remaining state is decompressed out.
    for data in data_blocks:
        # :todo: add a max_length argument here to limit output size.
        yield bytearray(d.decompress(data))
    yield bytearray(d.flush())


def check_bitdepth_colortype(bitdepth, colortype):
    """
    Check that `bitdepth` and `colortype` are both valid,
    and specified in a valid combination.
    Returns (None) if valid, raise an Exception if not valid.
    """

    if bitdepth not in (1, 2, 4, 8, 16):
        raise FormatError("invalid bit depth %d" % bitdepth)
    if colortype not in (0, 2, 3, 4, 6):
        raise FormatError("invalid colour type %d" % colortype)
    # Check indexed (palettized) images have 8 or fewer bits
    # per pixel; check only indexed or greyscale images have
    # fewer than 8 bits per pixel.
    if colortype & 1 and bitdepth > 8:
        raise FormatError(
            "Indexed images (colour type %d) cannot"
            " have bitdepth > 8 (bit depth %d)."
            " See https://www.w3.org/TR/2003/REC-PNG-20031110/#table111 ."
            % (bitdepth, colortype)
        )
    if bitdepth < 8 and colortype not in (0, 3):
        raise FormatError(
            "Illegal combination of bit depth (%d)"
            " and colour type (%d)."
            " See https://www.w3.org/TR/2003/REC-PNG-20031110/#table111 ."
            % (bitdepth, colortype)
        )


def is_natural(x):
    """A non-negative integer."""
    try:
        is_integer = int(x) == x
    except (TypeError, ValueError):
        return False
    return is_integer and x >= 0


def undo_filter_sub(filter_unit, scanline, previous, result):
    """Undo sub filter."""

    ai = 0
    # Loops starts at index fu.  Observe that the initial part
    # of the result is already filled in correctly with
    # scanline.
    for i in range(filter_unit, len(result)):
        x = scanline[i]
        a = result[ai]
        result[i] = (x + a) & 0xFF
        ai += 1


def undo_filter_up(filter_unit, scanline, previous, result):
    """Undo up filter."""

    for i in range(len(result)):
        x = scanline[i]
        b = previous[i]
        result[i] = (x + b) & 0xFF


def undo_filter_average(filter_unit, scanline, previous, result):
    """Undo up filter."""

    ai = -filter_unit
    for i in range(len(result)):
        x = scanline[i]
        if ai < 0:
            a = 0
        else:
            a = result[ai]
        b = previous[i]
        result[i] = (x + ((a + b) >> 1)) & 0xFF
        ai += 1


def undo_filter_paeth(filter_unit, scanline, previous, result):
    """Undo Paeth filter."""

    # Also used for ci.
    ai = -filter_unit
    for i in range(len(result)):
        x = scanline[i]
        if ai < 0:
            a = c = 0
        else:
            a = result[ai]
            c = previous[ai]
        b = previous[i]
        p = a + b - c
        pa = abs(p - a)
        pb = abs(p - b)
        pc = abs(p - c)
        if pa <= pb and pa <= pc:
            pr = a
        elif pb <= pc:
            pr = b
        else:
            pr = c
        result[i] = (x + pr) & 0xFF
        ai += 1


def convert_la_to_rgba(row, result):
    for i in range(3):
        result[i::4] = row[0::2]
    result[3::4] = row[1::2]


def convert_l_to_rgba(row, result):
    """
    Convert a grayscale image to RGBA.
    This method assumes the alpha channel in result is
    already correctly initialized.
    """
    for i in range(3):
        result[i::4] = row


def convert_rgb_to_rgba(row, result):
    """
    Convert an RGB image to RGBA.
    This method assumes the alpha channel in result is
    already correctly initialized.
    """
    for i in range(3):
        result[i::4] = row[i::3]


# Only reason to include this in this module is that
# several utilities need it, and it is small.
def binary_stdin():
    """
    A sys.stdin that returns bytes.
    """

    return sys.stdin.buffer


def binary_stdout():
    """
    A sys.stdout that accepts bytes.
    """

    stdout = sys.stdout.buffer

    # On Windows the C runtime file orientation needs changing.
    if sys.platform == "win32":
        import msvcrt
        import os

        msvcrt.setmode(sys.stdout.fileno(), os.O_BINARY)

    return stdout


def cli_open(path):
    if path == "-":
        return binary_stdin()
    return open(path, "rb")


def main(argv):
    """
    Run command line PNG.
    Which reports version.
    """
    print(__version__, __file__)


if __name__ == "__main__":
    try:
        main(sys.argv)
    except Error as e:
        print(e, file=sys.stderr)
