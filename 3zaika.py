#!/usr/bin/env python3

'''
POV Mosaic, Triangle packing

Created by: Ilya Razmanov (mailto:ilyarazmanov@gmail.com)
            aka Ilyich the Toad (mailto:amphisoft@gmail.com)

Input: PNG
Output: POVRay

History:
2007        Initial AmphiSoft POV Sphere Mosaic, using FilterMeister https://filtermeister.com/
2023        Rewritten to Python. I/O with PyPNG from: https://gitlab.com/drj11/pypng
            s3zaika.py Initial release. Direct translation from FMML to Python.
04.04.2024  s3zaika.py final state, completely rewritten vs. first transition from FM.

0.0.0.1     Complete rewriting to more flexible project - 22 May 2024.
0.0.0.12    3zaika ready to release - 10 June 2024.
1.6.12.12   First Production release - 12 June 2024.
1.7.5.14    Bilinear interpolation added to map. Not used for coloring since results are unnecessary smooth.

    Project mirrors:
        https://github.com/Dnyarri/POVmosaic
        https://gitflic.ru/project/dnyarri/povmosaic

'''

__author__ = "Ilya Razmanov"
__copyright__ = "(c) 2007-2024 Ilya Razmanov"
__credits__ = "Ilya Razmanov"
__license__ = "unlicense"
__version__ = "1.7.5.14"
__maintainer__ = "Ilya Razmanov"
__email__ = "ilyarazmanov@gmail.com"
__status__ = "Production"

from tkinter import Tk, filedialog, BOTH
from tkinter.ttk import Progressbar
from time import time, ctime
from random import random

import png  # PNG reading: PyPNG from: https://gitlab.com/drj11/pypng

# --------------------------------------------------------------
# Creating dialog

sortir = Tk()
sortir.title('POVRay Mosaic: 3Zaika')
sortir.geometry('+100+100')
sortir.overrideredirect(True)
progressbar =  Progressbar(sortir, orient='horizontal', mode='determinate', value=0, maximum=100, length=500)
progressbar.pack(fill=BOTH, expand=True)
sortir.withdraw()
# Main dialog created and hidden


# --------------------------------------------------------------
# Open source and export files

# Open source image, first get name
sourcefilename = filedialog.askopenfilename(
    title='Open source PNG file', filetypes=[('PNG', '.png')], defaultextension=('PNG', '.png')
)
if sourcefilename == '':
    sortir.destroy()
    quit()

# open PNG file
source = png.Reader(filename=sourcefilename)  # starting PyPNG

# Opening image, iDAT comes to "pixels" as bytearray, to be tuple'd later
X, Y, pixels, info = source.asRGBA()
Z = (info['planes'])            # Maximum CHANNEL NUMBER
imagedata = tuple((pixels))     # Attempt to fix all bytearrays as tuple

if (info['bitdepth'] == 8):
    maxcolors = 255             # Maximal value for 8-bit channel
if (info['bitdepth'] == 16):
    maxcolors = 65535           # Maximal value for 16-bit channel

# opening result file, first get name
resultfilename = filedialog.asksaveasfilename(
    title='Save POVRay scene file',
    filetypes=[
        ('POV-Ray scene file', '*.pov'),
        ('All Files', '*.*'),
    ],
    defaultextension=('POV-Ray scene file', '.pov'),
)
if (resultfilename == '') or (sourcefilename == None):
    sortir.destroy()
    quit()

# open POV file
resultfile = open(resultfilename, 'w')

# Both files opened

def src(x, y, z):
    '''
    Analog of src from FM, force repeate edge instead of out of range.
    Returns int channel value z for pixel x, y

    '''

    cx = int(x); cy = int(y)    # nearest neighbour for float input
    cx = max(0, cx); cx = min((X-1), cx)
    cy = max(0, cy); cy = min((Y-1), cy)

    # Here is the main magic of turning two x, z into one array position
    position = (cx*Z) + z
    channelvalue = int(((imagedata[cy])[position]))

    return channelvalue
# end of src function

def srcY(x, y):
    '''
    Returns brightness of pixel x, y
    
    '''

    cx = int(x); cy = int(y)    # nearest neighbour for float input
    cx = max(0, cx); cx = min((X-1), cx)
    cy = max(0, cy); cy = min((Y-1), cy)

    if (info['planes'] < 3):    # supposedly L and LA
        Yntensity = src(x, y, 0)
    else:                       # supposedly RGB and RGBA
        Yntensity = int(0.2989*src(x, y, 0) + 0.587 *
                        src(x, y, 1) + 0.114*src(x, y, 2))

    return Yntensity
# end of srcY function

def srcYL(x, y):
    """
    Analog of srcY above, but returns bilinearly interpolated brightness of pixel x, y

    """

    fx = float(x); fy = float(y)        # Uses float input coordinates for interpolation
    fx = max(0,fx); fx = min((X-1),fx)
    fy = max(0,fy); fy = min((Y-1),fy)

    # Neighbour pixels coordinates (square corners x0,y0; x1,y0; x0,y1; x1,y1)
    x0 = int(x); x1 = x0 + 1
    y0 = int(y); y1 = y0 + 1

    # Reading corners src (see scr above) and interpolating
    channelvalue = (
        srcY(x0, y0) * (x1 - fx) * (y1 - fy) +
        srcY(x0, y1) * (x1 - fx) * (fy - y0) +
        srcY(x1, y0) * (fx - x0) * (y1 - fy) +
        srcY(x1, y1) * (fx - x0) * (fy - y0)
    )

    return int(channelvalue)
# end of srcYL function

# WRITING POV FILE

seconds = time(); localtime = ctime(seconds)    # will be used for randomization and for debug info

# --------------------------------
#   POV header start
#
resultfile.writelines([
    '/*\n',
    'Persistence of Vision Ray Tracer Scene Description File\n',
    'Version: 3.7\n',
    'Description: Mosaic picture consisting from solid spheres, triangle packing.\n',
    '             Other included objects are hexagonal prisms (honeycomb packing), cylinders,\n',
    '             etc., see list "#declare thingie_1=" below.\n',
    'Author: Automatically generated by 3zaika program, based on AmphiSoft POV Sphere Mosaic plug-in, see POVRay Mosaic project at\n',
    'https://github.com/Dnyarri/POVmosaic\n',
    'https://gitflic.ru/project/dnyarri/povmosaic\n\n',
    'developed by Ilya Razmanov aka Ilyich the Toad\n',
    'https://dnyarri.github.io\n',
    'mailto:ilyarazmanov@gmail.com\n\n',
    f'Generated by: {__file__} ver: {__version__} at: {localtime}\n'
    f'Converted from: {sourcefilename}\n'
    f'Source info: {info}\n'
    '*/\n\n',
])

#   Globals
resultfile.writelines([
    '\n',
    '#version 3.7;\n\n',
    'global_settings{\n',
    '    max_trace_level 3   // Small to speed up preview. May need to be increased for metals\n',
    '    adc_bailout 0.01    // High to speed up preview. May need to be decreased to 1/256\n',
    '    ambient_light <0.5, 0.5, 0.5>\n',
    '    assumed_gamma 1.0\n}\n\n',
    '#include "finish.inc"\n',
    '#include "metals.inc"\n',
    '#include "golds.inc"\n',
    '#include "glass.inc"\n',
    '\n',
])
#   POV header end
# --------------------------------

# --------------------------------
# Thingie element, then scene
resultfile.writelines([
    '\n// Necessary math stuff set as de facto constants to avoid imporing math\n',
    '#declare sqrtof3 = 1.7320508075688772935274463415059;   // sqrt(3)\n',
    '#declare revsqrtof3 = 1.0/sqrtof3;                      // 1.0/sqrt(3)\n\n',
    '\n/*\n   -<*<* Predefined variants *>*>-\n*/\n',
    '\n//       Thingie variants\n',
    '#declare thingie_1 = sphere{<0, 0, 0>, 0.5}\n',
    '#declare thingie_2 = cylinder{<0, 0, 0>, <0, 0, 1.0>, 0.5}\n',
    '#declare thingie_3 = cone{<0, 0, 0>, 0.5, <0, 0, 1.0>, 0.0}\n',
    '// Hexagonal prism below, like pencils in honeycomb pack, try conic_sweep as well\n',
    '#declare thingie_4 = prism{linear_sweep linear_spline 0, 1, 7,\n <-0.5, 0.5*revsqrtof3>, <0,revsqrtof3>, <0.5, 0.5*revsqrtof3>,\n <0.5,- 0.5*revsqrtof3>, <0,-revsqrtof3>, <-0.5,- 0.5*revsqrtof3>,\n <-0.5, 0.5*revsqrtof3> rotate x*270}\n',
    '// Rhomb prism below, try conic_sweep as well\n',
    '#declare thingie_5 = prism{linear_sweep linear_spline 0, 1, 5, <-1.0, 0>,\n <0, sqrtof3>, <1, 0>, <0, -sqrtof3>, <-1.0, 0> rotate x*270 scale 0.5}\n',
    '// CSG examples below, may be good for randomly rotated thingies\n',
    '#declare thingie_6 = intersection{\n    cylinder{<0, 0, -1.0>, <0, 0, 1.0>, 0.5}\n    cylinder{<0, 0, -1.0>, <0, 0, 1.0>, 0.5 rotate x*90}\n    cylinder{<0, 0, -1.0>, <0, 0, 1.0>, 0.5 rotate y*90}\n  }  //  Cubic rounded CSG end\n',
    '#declare thingie_7 = intersection{\n    cylinder{<0, -1.0, 0>, <0, 1.0, 0>, 0.5}\n    cylinder{<0, -1.0, 0>, <0, 1.0, 0>, 0.5 rotate z*109.5}\n    cylinder{<0, -1.0, 0>, <0, 1.0, 0>, 0.5 rotate z*109.5 rotate y*109.5}\n    cylinder{<0, -1.0, 0>, <0, 1.0, 0>, 0.5 rotate z*109.5 rotate y*219.0}\n  }  //  Tetrahedral rounded CSG end\n',
    '\n//       Thingie finish variants\n',
    '#declare thingie_finish_1 = finish{ambient 0.1 diffuse 0.7 specular 0.8 reflection 0 roughness 0.005}    // Smooth plastic\n',
    '#declare thingie_finish_2 = finish{phong 0.1 phong_size 1}    // Dull, good color representation\n',
    '#declare thingie_finish_3 = finish{ambient 0.1 diffuse 0.5 specular 1\n    roughness 0.01 metallic reflection {0.75 metallic}}    // Metallic example\n',
    '#declare thingie_finish_4 = finish{ambient 0.1 diffuse 0.5 reflection 0.1 specular 1 roughness 0.005\n    irid {0.5 thickness 0.9 turbulence 0.9}}    // Iridescence example\n',
    '\n//       Thingie normal variants\n',
    '#declare thingie_normal_1 = normal{bumps 0.0}  // Null normal placeholder\n',
    '#declare thingie_normal_2 = normal{bumps 1.0 scale<0.01, 0.01, 0.01>}\n',
    '#declare thingie_normal_3 = normal{bumps 0.05 scale<1.0, 0.05, 0.5>}\n',
    '#declare thingie_normal_4 = normal{spiral1 16 0.5 scallop_wave rotate y*90}\n',
    '\n//       Global modifiers for all thingies in the scene\n',
    '#declare color_factor = 1.0;      // Color multiplier for all channels\n',
    '#declare f_value = 0.0;           // Filter value for all thingies\n',
    '#declare t_value = 0.0;           // Transmit value for all thingies\n',
    '#declare evenodd_rotate = <0.0, 0.0, 0.0>;  // Odd lines rotate, rarely useful\n',
    '\n/*       Map function\nMaps are transfer functions control value (i.e. source pixel brightness) is passed through.\nBy default exported map is five points linear spline, control points are set in the table below,\nfirst column is input, first digits in second column is output for this input.\nNote that by default input=output, i.e. no changes applied to source pixel brightness. */\n\n',
    '#declare Curve = function {  // Spline curve construction begins\n',
    '  spline { linear_spline\n',
    '    0.0,   <0.0,   0>\n',
    '    0.25,  <0.25,  0>\n',
    '    0.5,   <0.5,   0>\n',
    '    0.75,  <0.75,  0>\n',
    '    1.0,   <1.0,   0>}\n  }  // Construction complete\n',
    '#declare map = function(c) {Curve(c).u}  // Spline curve assigned as map\n',
    '\n/*\n   -<*<* Selecting variants, configuring scene *>*>-\n*/\n\n',
    '#declare thingie = thingie_1\n',
    '#declare thingie_finish = thingie_finish_1\n',
    '#declare thingie_normal = thingie_normal_1\n',
    '\n//       Per-thingie modifiers\n',
    '#declare move_map = <0, 0, 0>;    // To move thingies depending on map. No constrains on values\n',
    '#declare scale_map = <0, 0, 0>;   // To rescale thingies depending on map. Expected values 0..1\n',
    '#declare rotate_map = <0, 0, 0>;  // To rotate thingies depending on map. Values in degrees\n',
    '#declare move_rnd = <0, 0, 0>;    // To move thingies randomly. No constrains on values\n',
    '#declare rotate_rnd = <0, 0, 0>;  // To rotate thingies randomly. Values in degrees\n',
    '\n//       Per-thingie normal modifiers\n',
    '#declare normal_move_rnd = <0, 0, 0>;    // Random move of finish. No constrains on values\n',
    '#declare normal_rotate_rnd = <0, 0, 0>;  // Random rotate of finish. Values in degrees\n',
    '\n//       Seed random\n',
    f'#declare rnd_1 = seed({int(seconds * 1000000)});\n\n',
    '\n// -<*<* Insert preset to override setting above *>*>-\n',
    '// #include "preset_01.inc"    // Set path and name of your file related to scene file\n\n',
    # Starting scene content
    # Camera
    '\n// # # # # # SCENE SECTION # # # # #\n\n',
    '#declare camera_height = 3.0;  // Camera height over object, used for view angle\n\n',
    'camera{\n',
    '  // orthographic\n',
    '  location<0.0, 0.0, camera_height>\n',
    '  right x*image_width/image_height\n',
    '  up y\n',
    '  direction <0, 0, 1>\n',
    f'  angle 2.0*(degrees(atan2({0.5 * max(X,Y)/X}, camera_height-({1.0/max(X,Y)})))) // Supposed to fit object\n',
    '  look_at<0.0, 0.0, 0.0>\n',
    '}\n\n',
    # Light
    'light_source{0*x\n  color rgb<1.1, 1.0, 1.0>\n  translate<4, 2, 3>\n}\n\n',
    'light_source{0*x\n  color rgb<0.9, 1.0, 1.0>\n  translate<-2, 6, 7>\n}\n\n',
    'background{color rgbft<0, 0, 0, 1, 1>}\n\n',
    # Main object
    '\n// Object thething made out of thingies\n',
    '#declare thething = union{\n',  # Opening big thething
])

# Internal strings for packing change

'''
Below is height of triangle with 2*0.5 sides, that is vertical distance
between two 0.5 radius spheres as defined by thingie.
sqrt(3) = 1.732... hardcoded to remove math export
'''
triangle_height = 0.5 * 1.7320508075688772935274463415059

even_odd_string = ''
even_string = 'translate<0.5, 0, 0>'    # mandatory shift for triangle pattern, uneditable
odd_string = 'rotate evenodd_rotate'    # consider 'rotate<0.0, 0.0, 180.0>' or scale <1.0, -1.0, 1.0>

# Now going to cycle through image and build big thething
Ycount = int(Y/triangle_height)
progressbar.config(maximum=Ycount)

for y in range(0, Ycount, 1):

    sortir.deiconify()
    progressbar.config(value=y)
    sortir.update()
    sortir.update_idletasks()

    resultfile.write(f'\n  // Row {y}\n')

    if (((y+1) % 2) == 0):
        even_odd_string = even_string
        even_odd_trans = 0.5
    else:
        even_odd_string = odd_string
        even_odd_trans = 0.0

    for x in range(0, X, 1):

        # Colors normalized to 0..1
        r = float(src(x, y*triangle_height, 0))/maxcolors
        g = float(src(x, y*triangle_height, 1))/maxcolors
        b = float(src(x, y*triangle_height, 2))/maxcolors

        # Something to map something to. By default - brightness, normalized to 0..1
        # c = float(srcY(x, y*triangle_height))/maxcolors # Nearest neghbour
        c = float(srcYL(x+even_odd_trans, y*triangle_height))/maxcolors # Bilinear

        # alpha to be used for alpha dithering
        a = float(src(x, y*triangle_height, 3))/maxcolors
        # a = 0 is transparent, a = 1.0 is opaque
        tobe_or_nottobe = a > random()

        # whether to draw thingie in place of partially transparent pixel or not
        if tobe_or_nottobe:
            # Opening object "thingie" to draw
            resultfile.writelines([
                '    object{thingie\n',
                f'      pigment{{rgbft<color_factor*{r}, color_factor*{g}, color_factor*{b}, f_value, t_value>}}\n',
                '      finish{thingie_finish}\n',
                '      normal{thingie_normal translate(normal_move_rnd * <rand(rnd_1), rand(rnd_1), rand(rnd_1)>) rotate(normal_rotate_rnd * <rand(rnd_1), rand(rnd_1), rand(rnd_1)>)}\n',
                f'      scale(<1, 1, 1> - (scale_map * <map({c}), map({c}), map({c})>))\n',
                f'      rotate(rotate_map * <map({c}), map({c}), map({c})>)\n',
                f'      rotate(rotate_rnd * <rand(rnd_1), rand(rnd_1), rand(rnd_1)>)\n',
                f'      {even_odd_string}\n',
                f'      translate(move_map * <map({c}), map({c}), map({c})>)\n',
                f'      translate(move_rnd * <rand(rnd_1), rand(rnd_1), rand(rnd_1)>)\n',
                f'      translate<{x}, {y*triangle_height}, 0>\n',
                '    }\n'
            # Finished thingie
            ])

# Transform object to fit 1, 1, 1 cube at 0, 0, 0 coordinates
resultfile.writelines([
    '\n  // Object transforms to fit 1, 1, 1 cube at 0, 0, 0 coordinates\n',
    '  translate<0.25, 0.5, 0>\n',            # compensate of thingie size around zero
    f'  translate<{-0.5*X}, {-0.5*Y}, 0>\n',  # centering at scene zero
    f'  scale<{-1.0/max(X, Y)}, {-1.0/max(X, Y)}, {1.0/max(X, Y)}>\n',    # fitting and mirroring
    '} // thething closed\n\n'
    '\nobject {thething\n'
    f'//  interior {{ior 2.0 fade_power 1.5 fade_distance 1.0*{1.0/max(X, Y)} fade_color<0.95, 0.95, 0.95>}}\n',
    '}\n',
    '\n/*\n\nhappy rendering\n\n  0~0\n (---)\n(.>|<.)\n-------\n\n*/'
])
# Closed scene

# Close output
resultfile.close()

# --------------------------------------------------------------
# Destroying dialog

sortir.destroy()
sortir.mainloop()
# Dialog destroyed and closed
# --------------------------------------------------------------
