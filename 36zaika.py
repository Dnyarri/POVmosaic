#!/usr/bin/env python3

'''
POV Mosaic, Triangle packing, Regular plane partition 3/6

Created by: Ilya Razmanov (mailto:ilyarazmanov@gmail.com)
            aka Ilyich the Toad (mailto:amphisoft@gmail.com)

Input: PNG
Output: POVRay

History:
2007        Initial AmphiSoft POV Sphere Mosaic, using FilterMeister https://filtermeister.com/
2023        Rewritten to Python. I/O with PyPNG from: https://gitlab.com/drj11/pypng
            s3zaika.py Initial release. Direct translation from FMML to Python.
04.04.2024  s3zaika.py final state, completely rewritten vs. first transition from FM.

0.0.0.1     Complete rewriting to more flexible project - 18 June 2024.
1.7.22.12   Bugs seem to be eliminated. Prisms changed. Ready for release.
1.9.1.0     Reworked normals, added triangle tile normal.
1.9.1.1     Gamma note was added to export. Direct gamma setting to POV file is not forced
            since some software writes wrong numbers in gAMA
            so it is left to user to decide what to do with this.

-------------------
Main site:
https://dnyarri.github.io  

Project mirrored at:  
https://github.com/Dnyarri/POVmosaic  
https://gitflic.ru/project/dnyarri/povmosaic  

'''

__author__ = "Ilya Razmanov"
__copyright__ = "(c) 2007-2024 Ilya Razmanov"
__credits__ = "Ilya Razmanov"
__license__ = "unlicense"
__version__ = "1.9.1.1"
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
sortir.title('POVRay Mosaic: 36Zaika')
sortir.geometry(f'500x16+{(sortir.winfo_screenwidth()-500)//2}+{(sortir.winfo_screenheight()-16)//2}')
sortir.resizable(width=True, height=True)
progressbar = Progressbar(sortir, orient='horizontal', mode='determinate', value=0, maximum=100, length=500)
progressbar.pack(fill=BOTH, expand=True)
sortir.overrideredirect(True)
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

# Opening image, iDAT comes to "pixels" generator, to be tuple'd later
X, Y, pixels, info = source.asRGBA()
Z = (info['planes'])        # Maximum channel number
imagedata = tuple(pixels)   # Building tuple from generator

if (info['bitdepth'] == 8):
    maxcolors = 255         # Maximal value for 8-bit channel
if (info['bitdepth'] == 16):
    maxcolors = 65535       # Maximal value for 16-bit channel

if 'gamma' in info:
    gAMA = info['gamma']
    gamma_note = f'Source PNG gAMA was {gAMA}'
else:
    gamma_note = 'Source PNG gAMA was absent'

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
    'Description: Mosaic picture consisting from solid spheres, triangle packing, Regular plane partition 3/6.\n',
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
    f'    assumed_gamma 1.0   // {gamma_note}!\n}}\n\n',
    '#include "finish.inc"\n',
    '#include "metals.inc"\n',
    '#include "golds.inc"\n',
    '#include "glass.inc"\n',
    '#include "functions.inc"\n',
    '\n',
])
#   POV header end
# --------------------------------

# --------------------------------
# Thingie element, then scene
resultfile.writelines([
    '\n// Necessary math stuff set as de facto constants to avoid imporing math\n',
    '#declare sqrtof3 = 1.7320508075688772935274463415059;      // sqrt(3)\n',
    '#declare sqrtof3div2 = 0.86602540378443864676372317075294; // sqrt(3)/2\n\n',
    '\n/*\n   -<*<* Predefined variants *>*>-\n*/\n',
    '\n//       Thingie variants\n',
    '#declare thingie_1 = prism {\n    linear_sweep\n    linear_spline\n    -1,\n    0,\n    4,\n    <-1.0, sqrtof3div2>, <1.0, sqrtof3div2>, <0, -sqrtof3div2>, <-1.0, sqrtof3div2>\n    rotate x*90 translate z\n}\n',
    '#declare thingie_2 = prism {\n    conic_sweep\n    linear_spline\n    -1,\n    0,\n    4,\n    <-1.0, sqrtof3div2>, <1.0, sqrtof3div2>, <0, -sqrtof3div2>, <-1.0, sqrtof3div2>\n    rotate x*90 translate z\n}\n',
    '#declare thingie_3 = difference {\n    object {thingie_2}\n    object {thingie_2 scale<0, 0, -1.0> translate<0, 0, 1.0>}\n}  // WARNING: CSG of two previously defined objects depends on them!\n',
    '\n//       Thingie finish variants\n',
    '#declare thingie_finish_1 = finish{ambient 0.1 diffuse 0.7 specular 0.8 reflection 0 roughness 0.005}  // Smooth plastic\n',
    '#declare thingie_finish_2 = finish{phong 0.1 phong_size 1} // Dull, good color representation\n',
    '#declare thingie_finish_3 = finish{ambient 0.1 diffuse 0.5 specular 1\n    roughness 0.01 metallic reflection {0.75 metallic}}    // Metallic example\n',
    '#declare thingie_finish_4 = finish{ambient 0.1 diffuse 0.5 reflection 0.1 specular 1 roughness 0.005\n    irid {0.5 thickness 0.9 turbulence 0.9}}    // Iridescence example\n',
    '\n//       Thingie normal variants\n',
    '#declare thingie_normal_1 = normal{function {1}}  // Constant normal placeholder, template for function\n',
    '#declare thingie_normal_2 = normal{bumps 1.0 scale<0.01, 0.01, 0.01>}\n',
    '#declare thingie_normal_3 = normal{bumps 0.05 scale<1.0, 0.05, 0.5>}\n',
    '#declare thingie_normal_4 = normal{spiral1 8 0.5 scallop_wave}\n',
    '#declare thingie_normal_5 = normal{tiling 3 scale <0.5, 5, 0.5> rotate <90, 0, 0>}\n',
    '\n//       Global modifiers for all thingies in the scene\n',
    '#declare yes_color = 1;         // Whether source per-thingie color is taken or global patten applied\n',
    '// Color-relater settings below work only for "yes_color = 1;"\n',
    '#declare cm = function(k) {k}   // Color transfer function for all channels, all thingies\n',
    '#declare f_val = 0.0;           // Filter value for all thingies\n',
    '#declare t_val = 0.0;           // Transmit value for all thingies\n',
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
    f'#declare move_map = <0, 0, 0>;    // To move thingies depending on map. Additive, no constrains on values. Source image size is {max(X, Y)}\n',
    f'#declare scale_map = <0, 0, 0>;   // To rescale thingies depending on map. Additive, no constrains on values except object overlap on x,y\n',
    '#declare rotate_map = <0, 0, 0>;  // To rotate thingies depending on map. Values in degrees\n',
    '#declare move_rnd = <0, 0, 0>;    // To move thingies randomly. No constrains on values\n',
    '#declare rotate_rnd = <0, 0, 0>;  // To rotate thingies randomly. Values in degrees\n',
    '\n//       Per-thingie normal modifiers\n',
    '#declare normal_move_rnd = <0, 0, 0>;    // Random move of finish. No constrains on values\n',
    '#declare normal_rotate_rnd = <0, 0, 0>;  // Random rotate of finish. Values in degrees\n',
    '\n//       Common interior for the whole thething, fade_distance proportional to thingie size\n',
    f'#declare thething_interior = interior {{ior 2.0 fade_power 1.5 fade_distance 1.0*{1.0/max(X, Y)} fade_color <0.0, 0.5, 1.0>}}\n',
    '\n//       Seed random\n',
    f'#declare rnd_1 = seed({int(seconds * 1000000)});\n\n',
    'background{color rgbft <0, 0, 0, 1, 1>} // Sometimes need to be redefined\n\n\n',
    '\n// -<*<* Insert preset to override setting above *>*>-\n',
    '// #include "preset_01.inc"    // Set path and name of your file related to scene file\n\n',
    # Starting scene content
    # Camera
    '\n/*\n\n# # # # # SCENE SECTION # # # # #\n\n',
    'NOTE: Coordinate system match Photoshop,\norigin is top left, z points to the viewer.\nsky vector is important!\n\n*/\n\n',
    '#declare camera_position = <0.0, 0.0, 3.0>;  // Camera position over object, used for view angle\n\n',
    'camera{\n',
    '//  orthographic\n',
    '  location camera_position\n',
    '  right x*image_width/image_height\n',
    '  up y\n',
    '  sky <0, -1, 0>\n',
    f'  direction <0, 0, vlength(camera_position - <0.0, 0.0, {1.0/max(X, Y)}>)>  // May alone work for many pictures. Otherwise fiddle with angle below\n',
    f'  angle 2.0*(degrees(atan2({0.5 * max(X+0.5, Y+0.5)/X}, vlength(camera_position - <0.0, 0.0, {1.0/max(X, Y)}>)))) // Supposed to fit object, unless thingies are too high\n',
    '  look_at<0.0, 0.0, 0.0>\n',
    '}\n\n',
    # Light
    'light_source{0*x\n  color rgb<1.1, 1.0, 1.0>\n//  area_light <1, 0, 0>, <0, 1, 0>, 5, 5 circular orient area_illumination on\n  translate<4, -2, 3>\n}\n\n',
    'light_source{0*x\n  color rgb<0.9, 1.0, 1.0>\n//  area_light <1, 0, 0>, <0, 1, 0>, 5, 5 circular orient area_illumination on\n  translate<-2, -6, 7>\n}\n\n',
    # Main object
    '\n// Object thething made out of thingies\n',
    '#declare thething = union{\n',  # Opening big thething
])

# Internal strings for packing change

'''
Below is height of triangle.
sqrt(3) = 1.732... hardcoded to remove math export
'''
triangle_height = 1.7320508075688772935274463415059

even_odd_string = ''    # mandatory shifts for Regular plane partition 3/6
even_string = 'translate <-0.5, 0, 0>'
odd_string = 'translate <0.5, 0, 0>'

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
    else:
        even_odd_string = odd_string

    for x in range(0, X, 1):
        if (((x+1) % 2) == 0):
            # Flipping thingies along the row
            flip_string = 'scale <1.0, -1.0, 1.0>'
        else:
            flip_string = ''

        # Colors normalized to 0..1
        r = float(src(x, y*triangle_height, 0))/maxcolors
        g = float(src(x, y*triangle_height, 1))/maxcolors
        b = float(src(x, y*triangle_height, 2))/maxcolors

        # Something to map something to. By default - brightness, normalized to 0..1
        # c = float(srcY(x, y*triangle_height))/maxcolors # Nearest neghbour
        c = float(srcYL(x, y*triangle_height))/maxcolors # Bilinear

        # alpha to be used for alpha dithering
        a = float(src(x, y*triangle_height, 3))/maxcolors
        # a = 0 is transparent, a = 1.0 is opaque
        tobe_or_nottobe = a > random()

        # whether to draw thingie in place of partially transparent pixel or not
        if tobe_or_nottobe:
            # Opening object "thingie" to draw
            resultfile.writelines([
                '    object{thingie\n',
                '      #if (yes_color)\n',
                f'        pigment{{rgbft<cm({r}), cm({g}), cm({b}), f_val, t_val>}}\n',
                '        finish{thingie_finish}\n',
                '        normal{thingie_normal translate(normal_move_rnd * <rand(rnd_1), rand(rnd_1), rand(rnd_1)>) rotate(normal_rotate_rnd * <rand(rnd_1), rand(rnd_1), rand(rnd_1)>)}\n',
                '      #end\n',
                f'      {flip_string}\n',
                f'      scale(<1, 1, 1> + (scale_map * <map({c}), map({c}), map({c})>))\n',
                f'      rotate(rotate_map * <map({c}), map({c}), map({c})>)\n',
                f'      rotate(rotate_rnd * <rand(rnd_1), rand(rnd_1), rand(rnd_1)>)\n',
                f'      {even_odd_string}\n',
                f'      translate(move_map * <map({c}), map({c}), map({c})>)\n',
                '      translate(move_rnd * <rand(rnd_1), rand(rnd_1), rand(rnd_1)>)\n',
                f'      translate<{x}, {y*triangle_height}, 0>\n',
                '    }\n'
            # Finished thingie
            ])

# Transform object to fit 1, 1, 1 cube at 0, 0, 0 coordinates
resultfile.writelines([
    '\n  // Object transforms to fit 1, 1, 1 cube at 0, 0, 0 coordinates\n',
    f'  translate <0.25, 1.5, 0> + <{-0.5*X}, {-0.5*Y}, 0>\n',          # centering at scene zero
    f'  scale<{1.0/(max(X, Y)-2)}, {1.0/(max(X, Y)-2)}, {1.0/(max(X, Y)-2)}>\n',    # fitting
    '} // thething closed\n\n'
    '\nobject {thething\n'  # inserting thething
    '  #if (yes_color < 1)\n',
    '    pigment {color rgb<0.5, 0.5, 0.5>}\n',
    '    finish {thingie_finish}\n',
    '  #end\n',
    '  interior {thething_interior}\n',
    '}\n',  # insertion complete
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
