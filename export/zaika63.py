#!/usr/bin/env python3

"""
POV-Ray Mosaic, Regular plane partition 6/3.
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

1.19.1.7    Autofocus fixed, some calculations moved to POV-Ray to improve scene legibility, etc.

1.19.5.19   Filter and transmit turned from constants to function. WARNING: old presets may need editing!

---
Main site: `The Toad's Slimy Mudhole <https://dnyarri.github.io>`_

Git repositories:
`Main at Github <https://github.com/Dnyarri/POVmosaic>`_; `Gitflic mirror <https://gitflic.ru/project/dnyarri/povmosaic>`_

"""

__author__ = 'Ilya Razmanov'
__copyright__ = '(c) 2007-2025 Ilya Razmanov'
__credits__ = 'Ilya Razmanov'
__license__ = 'unlicense'
__version__ = '1.19.5.19'
__maintainer__ = 'Ilya Razmanov'
__email__ = 'ilyarazmanov@gmail.com'
__status__ = 'Production'

import random
from time import ctime, time


def zaika63(image3d: list[list[list[int]]], maxcolors: int, resultfilename: str) -> None:
    """POV-Ray Mosaic, Regular plane partition 6/3.

    `image3d` - image as list of lists of lists of int channel values.

    `maxcolors` - maximum value of int in `image3d` list, either 255 or 65535.

    `resultfilename` - name of POV-Ray file to export.

    """

    Y = len(image3d)
    X = len(image3d[0])
    Z = len(image3d[0][0])

    """ ╔═══════════════╗
        ║ src functions ║
        ╚═══════════════╝ """

    def src(x: int | float, y: int | float, z: int) -> int:
        """
        Analog of src from FilterMeister, force repeat edge instead of out of range.
        Returns channel z value for pixel x, y.

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
        """Returns brightness of pixel x, y."""

        if Z < 3:  # supposedly L and LA
            yntensity = src(x, y, 0)
        else:  # supposedly RGB and RGBA
            yntensity = int(0.298936021293775 * src(x, y, 0) + 0.587043074451121 * src(x, y, 1) + 0.114020904255103 * src(x, y, 2))

        return yntensity

    def src_lum_blin(x: float, y: float) -> int:
        """Analog of src_lum above, but returns bilinearly interpolated brightness of pixel x, y."""

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
            'Description: Mosaic picture consisting from solid spheres, triangle packing, Regular plane partition 6/3.\n',
            '             Other included objects are hexagonal prisms (honeycomb packing), cylinders,\n',
            '             etc., see list "#declare thingie_1=" below.\n',
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
            '\n// Necessary math stuff set as de facto constants to avoid importing math\n',
            '#declare sqrtof3 = 1.7320508075688772935274463415059;   // sqrt(3)\n',
            '#declare revsqrtof3 = 1.0/sqrtof3;                      // 1.0/sqrt(3)\n\n',
            '\n/*  -------------------------\n    |  Predefined variants  |\n    -------------------------  */\n',
            '\n//       Thingie variants\n',
            '#declare thingie_1 = sphere{<0, 0, 0>, 0.5};\n',
            '#declare thingie_2 = cylinder{<0, 0, 0>, <0, 0, 1.0>, 0.5};\n',
            '#declare thingie_3 = cone{<0, 0, 0>, 0.5, <0, 0, 1.0>, 0.0};\n',
            '// Hexagonal prism below, like pencils in honeycomb pack. Try conic_sweep as well\n',
            '#declare thingie_4 = prism{linear_sweep linear_spline -1, 0, 7,\n <-0.5, 0.5*revsqrtof3>, <0,revsqrtof3>, <0.5, 0.5*revsqrtof3>,\n <0.5, -0.5*revsqrtof3>, <0,-revsqrtof3>, <-0.5, -0.5*revsqrtof3>,\n <-0.5, 0.5*revsqrtof3> rotate x*90 translate z};\n',
            '// Rhomb prism below. Try conic_sweep as well\n',
            '#declare thingie_5 = prism{linear_sweep linear_spline -1, 0, 5, <-1.0, 0>,\n <0, sqrtof3>, <1, 0>, <0, -sqrtof3>, <-1.0, 0> rotate x*90 scale 0.5 translate z};\n',
            '// CSG examples below, may be good for randomly rotated thingies\n',
            '#declare thingie_6 = intersection{\n    cylinder{<0, 0, -1.0>, <0, 0, 1.0>, 0.5}\n    cylinder{<0, 0, -1.0>, <0, 0, 1.0>, 0.5 rotate x*90}\n    cylinder{<0, 0, -1.0>, <0, 0, 1.0>, 0.5 rotate y*90}\n  };  //  Cubic rounded CSG end\n',
            '#declare thingie_7 = intersection{\n    cylinder{<0, -1.0, 0>, <0, 1.0, 0>, 0.5}\n    cylinder{<0, -1.0, 0>, <0, 1.0, 0>, 0.5 rotate z*109.5}\n    cylinder{<0, -1.0, 0>, <0, 1.0, 0>, 0.5 rotate z*109.5 rotate y*109.5}\n    cylinder{<0, -1.0, 0>, <0, 1.0, 0>, 0.5 rotate z*109.5 rotate y*219.0}\n  };  //  Tetrahedral rounded CSG end\n',
            '\n//       Thingie finish variants\n',
            '#declare thingie_finish_1 = finish{ambient 0.1 diffuse 0.7 specular 0.8 reflection 0 roughness 0.005};  // Smooth plastic\n',
            '#declare thingie_finish_2 = finish{phong 0.1 phong_size 1}; // Dull, good color representation\n',
            '#declare thingie_finish_3 = finish{ambient 0.1 diffuse 0.5 specular 1\n    roughness 0.01 metallic reflection {0.75 metallic}};    // Metallic example\n',
            '#declare thingie_finish_4 = finish{ambient 0.1 diffuse 0.5 reflection 0.1 specular 1 roughness 0.005\n    irid {0.5 thickness 0.9 turbulence 0.9}};    // Iridescence example\n',
            '\n//       Thingie normal variants\n',
            '#declare thingie_normal_1 = normal{function {1}};  // Constant normal placeholder, template for function\n',
            '#declare thingie_normal_2 = normal{bumps 1.0 scale<0.01, 0.01, 0.01>};\n',
            '#declare thingie_normal_3 = normal{bumps 0.05 scale<1.0, 0.05, 0.5>};\n',
            '#declare thingie_normal_4 = normal{spiral1 8 0.5 scallop_wave};\n',
            '#declare counts = 8; #declare thingie_normal_5 = normal{function{mod(abs(cos(counts*x)+cos(-counts*y)+cos(counts*z)), 1)}};  // Typically counts 4-16 is acceptable\n',
            '#declare thingie_normal_6 = normal{function{64*abs(x*y*z)}};\n',
            '\n/*  ----------------------------------------------------\n    |  Global modifiers for all thingies in the scene  |\n    ----------------------------------------------------  */\n\n',
            '#declare thingie_texture_2 = texture {  // Define transparent texture overlay here\n',
            '  pigment {gradient z colour_map {[0.0, rgbt <0,0,0,1>] [1.0, rgbt <0,0,0,1>]} scale 0.1 rotate <30, 30, 0>}};\n\n',  # Transparent texture overlay
            '#declare yes_color = 1;         // Whether source per-thingie color is taken or global patten applied\n',
            '// Color-relater settings below work only for "yes_color = 1;"\n',
            # Color, filter and transmit functions
            '#declare cm = function(Channel) {Channel};   // Color transfer function for RGB channels, all thingies\n',
            '#declare f_val = function(Luma, Alpha) {0.0};  // Filter value for all thingies. 0 means opaque.\n',
            '#declare t_val = function(Luma, Alpha) {0.0};  // Transmit value for all thingies. Note that for Alpha = transparency you need inversion (1 - Alpha)!\n',
            '\n#declare evenodd_transform = transform { };  // You may put odd lines transform here, rarely useful\n',
            # Map
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
            '    1.0,   <1.0,   0>}\n  };  // Construction complete\n',
            '#declare map = function(c) {Curve(c).u};  // Spline curve assigned as map\n',
            '\n/*  -------------------------------------------\n    |  Selecting variants, configuring scene  |\n    -------------------------------------------  */\n\n',
            # Switches
            '#declare thingie = thingie_1;\n',
            '#declare thingie_finish = thingie_finish_1;\n',
            '#declare thingie_normal = thingie_normal_1;\n',
            '\n//       Per-thingie modifiers\n',
            f'#declare move_map = <0, 0, 0>;    // To move thingies depending on map. Additive, no constrains on values. Maximum source image size is {max(X, Y)}\n',
            '#declare scale_map = <0, 0, 0>;   // To rescale thingies depending on map. Additive, no constrains on values except object overlap on x,y\n',
            '#declare rotate_map = <0, 0, 0>;  // To rotate thingies depending on map. Values in degrees\n',
            '#declare move_rnd = <0, 0, 0>;    // To move thingies randomly. No constrains on values\n',
            '#declare rotate_rnd = <0, 0, 0>;  // To rotate thingies randomly. Values in degrees\n',
            '\n//       Per-thingie normal modifiers\n',
            '#declare normal_move_rnd = <0, 0, 0>;    // Random move of normal map. No constrains on values\n',
            '#declare normal_rotate_rnd = <0, 0, 0>;  // Random rotate of normal map. Values in degrees\n',
            '\n//       Seed random\n',
            f'#declare rnd_1 = seed({int(seconds * 1000000)});\n\n',
            'background{color rgbft <0, 0, 0, 1, 1>} // Hey, I am just trying to be explicit in here!\n\n\n',
            '/*  -----------------------------------------\n    |  Source image width and height.       |\n    |  Necessary for further calculations.  |\n    -----------------------------------------  */\n\n',
            f'#declare X = {X};  // Source image width, px\n',
            f'#declare Y = {Y};  // Source image height, px\n\n',
            '\n/*  --------------------------------------------------\n    |  Some properties for whole thething and scene  |\n    --------------------------------------------------  */\n\n',
            '//       Common interior for the whole thething, fade_distance set to thingie size before scale_map etc.\n',
            '#declare thething_interior = interior {ior 2.5 fade_power 1.5 fade_distance (1.0 / max(X, Y)) fade_color <0.0, 0.5, 1.0>};\n',
            '//       Common transform for the whole thething, placed here just to avoid scrolling\n',
            '#declare thething_transform = transform {\n  // You can place your global scale, rotate etc. here\n};\n',
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
            '  direction <0, 0, vlength(camera_position - <0.0, 0.0, 1.0 / max(X, Y)>)>  // May alone work for many pictures. Otherwise fiddle with angle below\n',
            '  angle 2.0*(degrees(atan2(0.5 * image_width * max((X + 0.5)/image_width, (Y + 0.5)/image_height) / max(X + 0.5, Y + 0.5), vlength(camera_position - <0.0, 0.0, 1.0 / max(X, Y)>)))) // Supposed to fit object\n',
            '  look_at<0.0, 0.0, 0.0>\n',
            '}\n\n',
            # Light
            'light_source{0*x\n  color rgb<1.1, 1.0, 1.0>\n//  area_light <1, 0, 0>, <0, 1, 0>, 5, 5 circular orient area_illumination on\n  translate<4, -2, 3>\n}\n\n',
            'light_source{0*x\n  color rgb<0.9, 1.0, 1.0>\n//  area_light <1, 0, 0>, <0, 1, 0>, 5, 5 circular orient area_illumination on\n  translate<-2, -6, 7>\n}\n\n',
            '\n/*  ----------------------------------------------\n    |  Insert preset to override settings above  |\n    ----------------------------------------------  */\n\n',
            '// #include "preset.inc"    // Set path and name of your file related to scene file\n\n\n',
            # Main object
            '// Object thething made out of thingies\n\n',
            '#declare thething = union{\n',  # Opening big thething
        ]
    )

    """
    Below is height of triangle with 2*0.5 sides, that is vertical distance between two 0.5 radius spheres as defined by thingie.
    sqrt(3) = 1.732... hardcoded to remove math export
    """
    triangle_height = 0.5 * 1.7320508075688772935274463415059

    even_odd_string = ''
    even_string = 'translate<0.5, 0, 0>'  # mandatory shift for triangle pattern, uneditable
    odd_string = 'transform {evenodd_transform}'  # consider 'rotate<0.0, 0.0, 180.0>' or scale <1.0, -1.0, 1.0>

    """ ┌─────────────────────────────────────────────────┐
        │ Cycling through image and building big thething │
        └─────────────────────────────────────────────────┘ """

    Ycount = int(Y / triangle_height)

    for y in range(0, Ycount, 1):
        resultfile.write(f'\n  // Row {y}\n')

        if ((y + 1) % 2) == 0:
            even_odd_string = even_string
            even_odd_trans = 0.5
        else:
            even_odd_string = odd_string
            even_odd_trans = 0.0

        for x in range(0, X, 1):
            if Z > 2:
                # RGB(A) source, colors normalized to 0..1
                r = float(src(x, y * triangle_height, 0)) / maxcolors
                g = float(src(x, y * triangle_height, 1)) / maxcolors
                b = float(src(x, y * triangle_height, 2)) / maxcolors
            else:
                # L(A) source, r, g, b set to normalized grey value
                r = g = b = float(src(x, y * triangle_height, 0)) / maxcolors

            # Something to map something to. By default - brightness, normalized to 0..1
            # c = float(src_lum(x, y*triangle_height))/maxcolors # Nearest neighbor
            c = float(src_lum_blin(x + even_odd_trans, y * triangle_height)) / maxcolors  # Bilinear

            # alpha to be used for alpha dithering
            if Z == 4 or Z == 2: # RGBA or LA
                a = 1.02 * (float(src(x, y * triangle_height, Z - 1)) / maxcolors) - 0.01
                # Slightly extending +/- 1%
                tobe_or_nottobe = a >= random.random()
                # a = 0 is transparent, a = 1.0 is opaque
            else:  # No alpha
                a = 1.0
                tobe_or_nottobe = True

            # whether to draw thingie in place of partially transparent pixel or not
            if tobe_or_nottobe:
                # Opening object "thingie" to draw
                resultfile.writelines(
                    [
                        '    object{thingie\n',
                        '      #if (yes_color)\n',
                        '        texture{\n',
                        f'          pigment{{rgbft<cm({r}), cm({g}), cm({b}), f_val({c}, {a}), t_val({c}, {a})>}}\n',
                        '          finish{thingie_finish}\n',
                        '          normal{thingie_normal translate(normal_move_rnd * (<rand(rnd_1), rand(rnd_1), rand(rnd_1)>-0.5)) rotate(normal_rotate_rnd * (<rand(rnd_1), rand(rnd_1), rand(rnd_1)>-0.5))}',
                        '        }\n',  # closing base texture
                        '        texture{thingie_texture_2}\n'  # overlay texture
                        '      #end\n',
                        f'      scale(<1, 1, 1> + (scale_map * <map({c}), map({c}), map({c})>))\n',
                        f'      rotate(rotate_map * <map({c}), map({c}), map({c})>)\n',
                        '      rotate(rotate_rnd * (<rand(rnd_1), rand(rnd_1), rand(rnd_1)-0.5>))\n',
                        f'      {even_odd_string}\n',
                        f'      translate(move_map * <map({c}), map({c}), map({c})>)\n',
                        '      translate(move_rnd * (<rand(rnd_1), rand(rnd_1), rand(rnd_1)>-0.5))\n',
                        f'      translate<{x}, {y * triangle_height}, 0>\n',
                        '    }\n',
                        # Finished thingie
                    ]
                )
    # thething built but not closed yet
    # Transform thething to fit 1, 1, 1 cube at 0, 0, 0 coordinates
    resultfile.writelines(
        [
            '\n  // Object transforms to fit 1, 1, 1 cube at 0, 0, 0 coordinates\n',
            '  translate <0.25, 0.5, 0> + <-0.5 * X, -0.5 * Y, 0>\n',  # centering at scene zero
            '  scale<1.0 / max(X, Y), 1.0 / max(X, Y), 1.0 / max(X, Y)>\n',  # fitting
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
