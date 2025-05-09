#!/usr/bin/env python3

"""
POV-Ray Mosaic, Regular plane partition 4/4 and related (square pattern).
---

Created by: `Ilya Razmanov <mailto:ilyarazmanov@gmail.com>`_ aka `Ilyich the Toad <mailto:amphisoft@gmail.com>`_.

History:
---

2007    Initial AmphiSoft POV Sphere Mosaic, using `FilterMeister <https://filtermeister.com/>`_

2023    Rewritten to Python. PNG import with `PyPNG <https://gitlab.com/drj11/pypng>`_

0.0.04.4    Complete rewriting 4 Apr 2024.

1.6.12.12   First Production release - 12 June 2024.

1.11.01.1   Last release as standalone 1 Nov 2024.

1.14.1.0    Rewritten as module.

---
Main site: `The Toad's Slimy Mudhole <https://dnyarri.github.io>`_

Git repositories:
`Main at Github <https://github.com/Dnyarri/POVmosaic>`_; `Gitflic mirror <https://gitflic.ru/project/dnyarri/povmosaic>`_

"""

__author__ = 'Ilya Razmanov'
__copyright__ = '(c) 2007-2025 Ilya Razmanov'
__credits__ = 'Ilya Razmanov'
__license__ = 'unlicense'
__version__ = '1.17.9.11'
__maintainer__ = 'Ilya Razmanov'
__email__ = 'ilyarazmanov@gmail.com'
__status__ = 'Production'

import random
from time import ctime, time


def zaika44(image3d: list[list[list[int]]], maxcolors: int, resultfilename: str) -> None:
    """POV Mosaic, Regular plane partition 4/4.

    `image3d` - image as list of lists of lists of int channel values.

    `maxcolors` - maximum value of int in `image3d` list.

    `resultfilename` - name of POVRay file to export.

    """

    # Determining list sizes
    Y = len(image3d)
    X = len(image3d[0])
    Z = len(image3d[0][0])

    """ ╔═══════════════╗
        ║ src functions ║
        ╚═══════════════╝ """

    def src(x: int | float, y: int | float, z: int) -> int:
        """
        Analog of src from FilterMeister, force repeat edge instead of out of range.
        Returns int channel value z for pixel x, y

        """

        cx = int(x)
        cy = int(y)  # nearest neighbor for float input
        cx = max(0, cx)
        cx = min((X - 1), cx)
        cy = max(0, cy)
        cy = min((Y - 1), cy)

        channelvalue = image3d[cy][cx][z]

        return channelvalue

    def src_lum(x: int | float, y: int | float) -> int:
        """
        Returns brightness of pixel x, y

        """

        if Z < 3:  # supposedly L and LA
            yntensity = src(x, y, 0)
        else:  # supposedly RGB and RGBA
            yntensity = int(0.298936021293775 * src(x, y, 0) + 0.587043074451121 * src(x, y, 1) + 0.114020904255103 * src(x, y, 2))

        return yntensity

    def src_lum_blin(x: float, y: float) -> int:
        """
        Analog of src_lum above, but returns bilinearly interpolated brightness of pixel x, y

        """

        fx = float(x)
        fy = float(y)  # Uses float input coordinates for interpolation

        # Neighbor pixels coordinates (square corners x0,y0; x1,y0; x0,y1; x1,y1)
        x0 = int(x)
        x1 = x0 + 1
        y0 = int(y)
        y1 = y0 + 1

        # Reading corners src_lum (see scr_lum above) and interpolating
        channelvalue = src_lum(x0, y0) * (x1 - fx) * (y1 - fy) + src_lum(x0, y1) * (x1 - fx) * (fy - y0) + src_lum(x1, y0) * (fx - x0) * (y1 - fy) + src_lum(x1, y1) * (fx - x0) * (fy - y0)

        return int(channelvalue)

    """ ╔══════════════════╗
        ║ Writing POV file ║
        ╚══════════════════╝ """

    resultfile = open(resultfilename, 'w')

    seconds = time()
    localtime = ctime(seconds)  # will be used for randomization and for debug info

    """ ┌────────────┐
        │ POV header │
        └────────────┘ """

    resultfile.writelines(
        [
            '/*\n',
            'Persistence of Vision Ray Tracer Scene Description File\n',
            'Version: 3.7\n',
            'Description: Mosaic picture consisting from solid boxes, square packing, Regular plane partition 4/4.\n',
            '             Other included objects are cylinders, spheres, etc.\n',
            '             see list "#declare thingie_1=" and below.\n',
            f'Source image properties: Width {X} px, Height {Y} px, Colors per channel: {maxcolors}\n',
            f'File automatically generated at {localtime} by {__name__} module ver. {__version__}\n',
            'developed by Ilya Razmanov aka Ilyich the Toad\n',
            '   https://dnyarri.github.io\n',
            '   mailto:ilyarazmanov@gmail.com\n*/\n\n',
        ]
    )

    """ ┌──────────────────────┐
        │ Globals and includes │
        └──────────────────────┘ """

    resultfile.writelines(
        [
            '\n',
            '#version 3.7;\n\n',
            'global_settings{\n',
            '    max_trace_level 3   // Small to speed up preview. May need to be increased for metals\n',
            '    adc_bailout 0.01    // High to speed up preview. May need to be decreased to 1/256\n',
            '    assumed_gamma 1.0\n',
            '    ambient_light <0.5, 0.5, 0.5>\n',
            '    charset utf8\n',
            '}\n\n',
            '#include "functions.inc"\n',
            '\n',
        ]
    )

    """ ┌─────────────────────┐
        │ Thingie, then scene │
        └─────────────────────┘ """

    resultfile.writelines(
        [
            '\n/*  -------------------------\n    |  Predefined variants  |\n    -------------------------  */\n',
            '\n//       Thingie variants\n',
            '#declare thingie_1 = box{<-0.5, -0.5, -0.5>, <0.5, 0.5, 0.5>};\n',
            '#declare thingie_2 = sphere{<0, 0, 0>, 0.5};\n',
            '#declare thingie_3 = cylinder{<0, 0, 0>, <0, 0, 1.0>, 0.5};\n',
            '#declare thingie_4 = superellipsoid{<0.5, 0.5> scale 0.5};\n',
            '// CSG example below, tetragonal bipyramid\n',
            '#declare thingie_5 = union{\n  prism{conic_sweep linear_spline 0.5, 1, 5, \n    <-0.5, -0.5>, <-0.5, 0.5>, <0.5, 0.5>, <0.5, -0.5>, <-0.5, -0.5> translate<0, -1, 0>}\n  prism{conic_sweep linear_spline -1, -0.5, 5,\n    <-0.5, -0.5>, <-0.5, 0.5>, <0.5, 0.5>, <0.5, -0.5>, <-0.5, -0.5> translate<0, 1, 0>}\n  rotate x*90};\n',
            '// CSG examples below, may be good for randomly rotated thingies\n',  # CSG
            '#declare thingie_6 = intersection{\n    cylinder{<0, 0, -1.0>, <0, 0, 1.0>, 0.5}\n    cylinder{<0, 0, -1.0>, <0, 0, 1.0>, 0.5 rotate x*90}\n    cylinder{<0, 0, -1.0>, <0, 0, 1.0>, 0.5 rotate y*90}\n  };  //  Cubic rounded CSG end\n',
            '#declare thingie_7 = intersection{\n    cylinder{<0, -1.0, 0>, <0, 1.0, 0>, 0.5}\n    cylinder{<0, -1.0, 0>, <0, 1.0, 0>, 0.5 rotate z*109.5}\n    cylinder{<0, -1.0, 0>, <0, 1.0, 0>, 0.5 rotate z*109.5 rotate y*109.5}\n    cylinder{<0, -1.0, 0>, <0, 1.0, 0>, 0.5 rotate z*109.5 rotate y*219.0}\n  };  //  Tetrahedral rounded CSG end\n',
            '#declare thingie_8 = isosurface{function{f_rounded_box(x, y, z, 0.11, 0.5, 0.5, 0.5)}};  // First float is roundness, three others - size\n',
            '\n//       Thingie finish variants\n',
            '#declare thingie_finish_1 = finish{ambient 0.1 diffuse 0.7 specular 0.8 reflection 0 roughness 0.005};  // Smooth plastic\n',
            '#declare thingie_finish_2 = finish{phong 0.1 phong_size 1}; // Dull, good color representation\n',
            '#declare thingie_finish_3 = finish{ambient 0.1 diffuse 0.5 specular 1\n    roughness 0.01 metallic reflection {0.75 metallic}};    // Metallic example\n',
            '#declare thingie_finish_4 = finish{ambient 0.1 diffuse 0.5 reflection 0.1 specular 1 roughness 0.005\n    irid {0.5 thickness 0.9 turbulence 0.5}};    // Iridescence example\n',
            '\n//       Thingie normal variants\n',
            '#declare thingie_normal_1 = normal{function {1}};  // Constant normal placeholder, template for function\n',
            '#declare thingie_normal_2 = normal{bumps 1.0 scale<0.01, 0.01, 0.01>};\n',
            '#declare thingie_normal_3 = normal{bumps 0.05 scale<1.0, 0.05, 0.5>};\n',
            '#declare thingie_normal_4 = normal{spiral1 8 0.5 scallop_wave};\n',
            '#declare counts = 8; #declare thingie_normal_5 = normal{function{mod(abs(cos(counts*x)+cos(-counts*y)+cos(counts*z)), 1)}};\n',
            '#declare thingie_normal_6 = normal{function{mod(8*sqrt(pow(x,2)+pow(y,2)+pow(z,2)), 1.0)}};\n',
            '\n/*  ----------------------------------------------------\n    |  Global modifiers for all thingies in the scene  |\n    ----------------------------------------------------  */\n\n',
            '#declare thingie_texture_2 = texture {  // Define transparent texture overlay here\n',
            '  pigment {gradient z colour_map {[0.0, rgbt <0,0,0,1>] [1.0, rgbt <0,0,0,1>]} scale 0.1 rotate <30, 30, 0>}};\n\n',  # Transparent texture overlay
            '#declare yes_color = 1;         // Whether source per-thingie color is taken or global patten applied\n',
            '// Color-relater settings below work only for "yes_color = 1;"\n',
            '#declare cm = function(k) {k};  // Color transfer function for all channels, all thingies\n',
            '#declare f_val = 0.0;           // Filter value for all thingies\n',
            '#declare t_val = 0.0;           // Transmit value for all thingies\n',
            '\n#declare evenodd_rotate = <0.0, 0.0, 0.0>;  // Odd lines rotate, rarely useful\n',
            '#declare evenodd_offset = <0.5, 0, 0>;      // Even lines shift for brick wall\n',
            '#declare evenodd_offset = <0.0, 0, 0>;      // Default 0 even lines shift for no brick wall\n',
            '#declare scale_all = <1, 1, 1>;             // Base scale of all thingies. 1=original\n',
            '#declare rotate_all = <0, 0, 0>;            // Base rotation of all thingies. Values in degrees\n',
            '\n/*       Map function\nMaps are transfer functions control value (i.e. source pixel brightness) is passed through.\n',
            'By default exported map is five points linear spline, control points are set in the table below,\n',
            'first column is input, first digits in second column is output for this input.\n',
            'Note that by default input=output, i.e. no changes applied to source pixel brightness. */\n\n',
            '#declare Curve = function {  // Spline curve construction begins\n',
            '  spline { linear_spline\n',
            '    0.0,   <0.0,   0>,\n',
            '    0.25,  <0.25,  0>,\n',
            '    0.5,   <0.5,   0>,\n',
            '    0.75,  <0.75,  0>,\n',
            '    1.0,   <1.0,   0>}\n  }  // Construction complete\n',
            '#declare map = function(c) {Curve(c).u};  // Spline curve assigned as map\n',
            '\n/*  -------------------------------------------\n    |  Selecting variants, configuring scene  |\n    -------------------------------------------  */\n\n',
            '#declare thingie = thingie_8;  // Default set to isosurface thingie_8 to give you favorable first impression\n',
            '#declare thingie_finish = thingie_finish_1;\n',
            '#declare thingie_normal = thingie_normal_1;\n',
            '\n//       Per-thingie modifiers\n',
            f'#declare move_map = <0, 0, 0>;    // To move thingies depending on map. Additive, no constrains on values. Source image size is {max(X, Y)}\n',
            '#declare scale_map = <0, 0, 0>;   // To rescale thingies depending on map. Additive, no constrains on values except object overlap on x,y\n',
            '#declare rotate_map = <0, 0, 0>;  // To rotate thingies depending on map. Values in degrees\n',
            '#declare move_rnd = <0, 0, 0>;    // To move thingies randomly. No constrains on values\n',
            '#declare rotate_rnd = <0, 0, 0>;  // To rotate thingies randomly. Values in degrees\n',
            '\n//       Per-thingie normal modifiers\n',
            '#declare normal_move_rnd = <0, 0, 0>;    // Random move of normal map. No constrains on values\n',
            '#declare normal_rotate_rnd = <0, 0, 0>;  // Random rotate of normal map. Values in degrees\n',
            '\n/*  --------------------------------------------------\n    |  Some properties for whole thething and scene  |\n    --------------------------------------------------  */\n\n',
            '//       Common interior for the whole thething, fade_distance set to thingie size before scale_map etc.\n',
            f'#declare thething_interior = interior {{ior 2.0 fade_power 1.5 fade_distance 1.0*{1.0 / max(X, Y)} fade_color <0.0, 0.5, 1.0>}};\n',
            '//       Common transform for the whole thething, placed here just to avoid scrolling\n',
            '#declare thething_transform = transform {\n  // You can place your global scale, rotate etc. here\n};\n',
            '\n//       Seed random\n',
            f'#declare rnd_1 = seed({int(seconds * 1000000)});\n\n',
            'background{color rgbft <0, 0, 0, 1, 1>} // Hey, Im just trying to be explicit in here!\n\n',
            # Camera
            '\n/*\n  Camera and light\n\n',
            'NOTE: Coordinate system match Photoshop,\norigin is top left, z points to the viewer.\nsky vector is important!\n\n*/\n\n',
            '#declare camera_position = <0.0, 0.0, 3.0>;  // Camera position over object, used for view angle\n\n',
            'camera{\n',
            '//  orthographic\n',
            '  location camera_position\n',
            '  right x*image_width/image_height\n',
            '  up y\n',
            '  sky <0, -1, 0>\n',
            f'  direction <0, 0, vlength(camera_position - <0.0, 0.0, {1.0 / max(X, Y)}>)>  // May alone work for many pictures. Otherwise fiddle with angle below\n',
            f'  angle 2.0*(degrees(atan2(0.5 * image_width * max({X}/image_width, {Y}/image_height) / {max(X, Y)}, vlength(camera_position - <0.0, 0.0, {1.0 / max(X, Y)}>)))) // Supposed to fit object\n',
            '  look_at<0.0, 0.0, 0.0>\n',
            '}\n\n',
            # Light
            'light_source{0*x\n  color rgb<1.1, 1.0, 1.0>\n//  area_light <1, 0, 0>, <0, 1, 0>, 5, 5 circular orient area_illumination on\n  translate<4, -2, 3>\n}\n\n',
            'light_source{0*x\n  color rgb<0.9, 1.0, 1.0>\n//  area_light <1, 0, 0>, <0, 1, 0>, 5, 5 circular orient area_illumination on\n  translate<-2, -6, 7>\n}\n\n',
            '\n/*  ----------------------------------------------\n    |  Insert preset to override settings above  |\n    ----------------------------------------------  */\n\n',
            '// #include "preset.inc"    // Set path and name of your file related to scene file\n\n',
            # Main object
            '\n// Object thething made out of thingies\n',
            '#declare thething = union{\n',  # Opening big thething
        ]
    )

    # Internal strings for packing change
    even_string_trn = 'translate evenodd_offset'
    odd_string_trn = ''
    even_string_rot = ''
    odd_string_rot = 'rotate evenodd_rotate'

    """ ┌─────────────────────────────────────────────────┐
        │ Cycling through image and building big thething │
        └─────────────────────────────────────────────────┘ """

    for y in range(0, Y, 1):
        resultfile.write(f'\n  // Row {y}\n')

        if ((y + 1) % 2) == 0:
            even_odd_string_trn = even_string_trn
            even_odd_string_rot = even_string_rot
        else:
            even_odd_string_trn = odd_string_trn
            even_odd_string_rot = odd_string_rot

        for x in range(0, X, 1):
            if Z > 2:
                # RGB(A) source, colors normalized to 0..1
                r = float(src(x, y, 0)) / maxcolors
                g = float(src(x, y, 1)) / maxcolors
                b = float(src(x, y, 2)) / maxcolors
            else:
                # L(A) source, r, g, b set to normalized grey value
                r = g = b = float(src(x, y, 0)) / maxcolors

            # Something to map something to. By default - brightness, normalized to 0..1
            c = float(src_lum(x, y)) / maxcolors

            # alpha to be used for alpha dithering
            if Z == 4 or Z == 2:
                a = 1.02 * (float(src(x, y, Z - 1)) / maxcolors) - 0.01  # Slightly extending +/- 1%
                # a = 0 is transparent, a = 1.0 is opaque
                tobe_or_nottobe = a >= random.random()
            else:  # No A
                tobe_or_nottobe = True

            # whether to draw thingie in place of partially transparent pixel or not
            if tobe_or_nottobe:
                # Opening object "thingie" to draw
                resultfile.writelines(
                    [
                        '    object{thingie\n',
                        '      #if (yes_color)\n',
                        '        texture{\n',
                        f'          pigment{{rgbft<cm({r}), cm({g}), cm({b}), f_val, t_val>}}\n',
                        '          finish{thingie_finish}\n',
                        '          normal{thingie_normal translate(normal_move_rnd * (<rand(rnd_1), rand(rnd_1), rand(rnd_1)>-0.5)) rotate(normal_rotate_rnd * (<rand(rnd_1), rand(rnd_1), rand(rnd_1)>-0.5))}',
                        '        }\n',  # closing base texture
                        '        texture{thingie_texture_2}\n'  # overlay texture
                        '      #end\n',
                        f'      scale(scale_all + (scale_map * <map({c}), map({c}), map({c})>))\n',
                        f'      {even_odd_string_rot}\n',
                        f'      rotate((rotate_map * <map({c}), map({c}), map({c})>) + rotate_all)\n',
                        '      rotate(rotate_rnd * (<rand(rnd_1), rand(rnd_1), rand(rnd_1)-0.5>))\n',
                        f'      {even_odd_string_trn}\n',
                        f'      translate(move_map * <map({c}), map({c}), map({c})>)\n',
                        '      translate(move_rnd * (<rand(rnd_1), rand(rnd_1), rand(rnd_1)>-0.5))\n',
                        f'      translate<{x}, {y}, 0>\n',
                        '    }\n',
                        # Finished thingie
                    ]
                )

    # thething built but not closed yet
    # Transform thething to fit 1, 1, 1 cube at 0, 0, 0 coordinates
    resultfile.writelines(
        [
            '\n  // Object transforms to fit 1, 1, 1 cube at 0, 0, 0 coordinates\n',
            f'  translate <0.5, 0.5, 0> + <{-0.5 * X}, {-0.5 * Y}, 0>\n',  # centering at scene zero
            f'  scale<{1.0 / max(X, Y)}, {1.0 / max(X, Y)}, {1.0 / max(X, Y)}>\n',  # fitting
            '} // thething closed\n\n'
            '\nobject {thething\n'  # inserting thething
            '  #if (yes_color < 1)\n',
            '    pigment {color rgb<0.5, 0.5, 0.5>}\n',
            '    finish {thingie_finish}\n',
            '  #end\n',
            '  interior {thething_interior}\n',
            '  transform {thething_transform}\n',
            '}\n',  # insertion complete
            '\n/*\n\nhappy rendering\n\n  0~0\n (---)\n(.>|<.)\n-------\n\n*/',
        ]
    )
    # Closed scene

    resultfile.close()

    return None


# Procedure end, main body begins
if __name__ == '__main__':
    print('Module to be imported, not run as standalone')
