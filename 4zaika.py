#!/usr/bin/env python3

'''
POV Mosaic, Regular plane partition 4/4 and related (square pattern)

Created by: Ilya Razmanov (mailto:ilyarazmanov@gmail.com)
            aka Ilyich the Toad (mailto:amphisoft@gmail.com)

Input: PNG
Output: POVRay

History:
2007        Initial AmphiSoft POV Sphere Mosaic, using FilterMeister https://filtermeister.com/
2023        Rewritten to Python. I/O with PyPNG from: https://gitlab.com/drj11/pypng
            b4zaikaR.py Initial release. Boxes are rotated randomly.
04.04.2024  b4zaikaR.py final state.

0.0.0.1     Complete rewriting to more flexible project - 21 May 2024.
0.0.0.4     Position and scale mapping. More thingies.
0.0.0.6     Normal randomization. Position and rotation randomization. Unwanted commutation fixed.
            Pigment format changed to rgbft (no lgbt puns please!).
0.0.0.7     Mapping moved to POVRay user-defined functions.

    Project mirrors:
        https://github.com/Dnyarri/POVmosaic
        https://gitflic.ru/project/dnyarri/povmosaic

'''

__author__ = "Ilya Razmanov"
__copyright__ = "(c) 2007-2024 Ilya Razmanov"
__credits__ = "Ilya Razmanov"
__license__ = "unlicense"
__version__ = "0.0.0.7"
__maintainer__ = "Ilya Razmanov"
__email__ = "ilyarazmanov@gmail.com"
__status__ = "Development"

from tkinter import Tk, Label, filedialog
from time import time, ctime
from random import random

import png  # PNG reading: PyPNG from: https://gitlab.com/drj11/pypng

# --------------------------------------------------------------
# Creating dialog

sortir = Tk()
sortir.title('PNG to POV conversion')
sortir.geometry('+100+100')
zanyato = Label(sortir, text='Starting...', font=(
    "arial", 14), padx=16, pady=10, justify='center')
zanyato.pack()
sortir.withdraw()
# Main dialog created and hidden


# --------------------------------------------------------------
# Open source and export files

# Open source image, first get name
sourcefilename = filedialog.askopenfilename(
    title='Open source PNG file', filetypes=[('PNG', '.png')], defaultextension=('PNG', '.png')
)
if (sourcefilename == '') or (sourcefilename == None):
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
if (resultfilename == '') or (resultfilename == None):
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

# WRITING POV FILE

seconds = time(); localtime = ctime(seconds)    # will be used for randomization and for debug info

# --------------------------------
#   POV header start
#
resultfile.writelines([
    '/*\n',
    'Persistence of Vision Ray Tracer Scene Description File\n',
    'Version: 3.7\n',
    'Description: Mosaic picture consisting from solid boxes, C4 symmetry (square) packing.\n',
    '             Other included objects are cylinders, spheres, etc.\n',
    '             see list "#declare thingie_1=" and below.\n',
    'Author: Automatically generated by 4zaika program, based on AmphiSoft POV Sphere Mosaic plug-in, see POVRay Mosaic project at\n',
    'https://github.com/Dnyarri/POVmosaic\n',
    'https://gitflic.ru/project/dnyarri/povmosaic\n\n',
    'developed by Ilya Razmanov aka Ilyich the Toad\n',
    'https://dnyarri.github.io\n',
    'mailto:ilyarazmanov@gmail.com\n\n',
    f'Generated by: {__file__} at: {localtime}\n'
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
    '#include "colors.inc"\n',
    '#include "finish.inc"\n',
    '#include "metals.inc"\n',
    '#include "golds.inc"\n',
    '\n',
])
#   POV header end
# --------------------------------

# --------------------------------
# Thingie element, then scene
resultfile.writelines([
    '\n//       Thingie variants\n',
    '#declare thingie_1 = box{<-0.5, -0.5, 0.0>, <0.5, 0.5, 1.0>}\n',
    '#declare thingie_2 = sphere{<0, 0, 0>, 0.5}\n',
    '#declare thingie_3 = cylinder{<0, 0, 0>, <0, 0, 1.0>, 0.5}\n',
    '// CSG example below, tetragonal bipyramid\n',
    '#declare thingie_4 = union{\n  prism{conic_sweep linear_spline 0.5, 1, 5, \n    <-0.5, -0.5>, <-0.5, 0.5>, <0.5, 0.5>, <0.5, -0.5>, <-0.5, -0.5> translate<0, -1, 0>}\n  prism{conic_sweep linear_spline -1, -0.5, 5,\n    <-0.5, -0.5>, <-0.5, 0.5>, <0.5, 0.5>, <0.5, -0.5>, <-0.5, -0.5> translate<0, 1, 0>}\n  rotate x*90}\n',
    '// CSG examples below, may be good for randomly rotated thingies\n',    # CSG
    '#declare thingie_5 = intersection{\n    cylinder{<0, 0, -1.0>, <0, 0, 1.0>, 0.5}\n    cylinder{<0, 0, -1.0>, <0, 0, 1.0>, 0.5 rotate x*90}\n    cylinder{<0, 0, -1.0>, <0, 0, 1.0>, 0.5 rotate y*90}\n  }  //  Cubic rounded\n',
    '#declare thingie_6 = intersection{\n    cylinder{<0, -1.0, 0>, <0, 1.0, 0>, 0.5}\n    cylinder{<0, -1.0, 0>, <0, 1.0, 0>, 0.5 rotate z*109.5}\n    cylinder{<0, -1.0, 0>, <0, 1.0, 0>, 0.5 rotate z*109.5 rotate y*109.5}\n    cylinder{<0, -1.0, 0>, <0, 1.0, 0>, 0.5 rotate z*109.5 rotate y*219.0}\n  }  //  Tetrahedral rounded\n',
    '\n//       Thingie finish variants\n',
    '#declare thingie_finish_1 = finish{ambient 0.1 diffuse 0.7 specular 0.8 reflection 0 roughness 0.005}    // Smooth HDPE\n',
    '#declare thingie_finish_2 = finish{phong 0.1 phong_size 1}    // Dull, good color representation\n',
    '#declare thingie_finish_3 = F_MetalE    // Example of linking complex finish from golds.inc\n',
    '\n//       Thingie normal variants\n',
    '#declare thingie_normal_1 = normal{bumps 0.0}\n',
    '#declare thingie_normal_2 = normal{bumps 1.0 scale<0.01, 0.01, 0.01>}\n',
    '#declare thingie_normal_3 = normal{bumps 0.05 scale<1.0, 0.05, 0.5>}\n',
    '#declare thingie_normal_4 = normal{spiral1 16 0.5 scallop_wave rotate y*90}\n',
    '\n//       Global modifiers for all thingies in the scene\n',
    '#declare color_factor = 1.0;      // Color multiplier for all channels\n',
    '#declare f_value = 0.0;           // Filter value for all thingies\n',
    '#declare t_value = 0.0;           // Transmit value for all thingies\n',
    '#declare brickwall_offset = <0.5, 0, 0>;   // Odd lines shift for brick wall\n',
    '#declare brickwall_offset = <0.0, 0, 0>;   // Default 0 odd lines shift for no brick wall\n',
    '#declare rotate_all = <0, 0, 0>;           // Base rotation of all thingies. Values in degrees\n',
    '\n//       Map functions for all thingies in the scene\n',
    '#declare map_1 = function(c) {c}                           // Direct input\n',
    '#declare map_2 = function(c) {abs((2.0 * c) - 1.0)}        // Triangle\n',
    '#declare map_3 = function(c) {1.0 - abs((2.0 * c) - 1.0)}  // Inverse triangle\n',
    '\n/*\n   -<*<* Selecting variants, configuring scene *>*>-     */\n',
    '#declare thingie = thingie_1\n',
    '#declare thingie_finish = thingie_finish_1\n',
    '#declare thingie_normal = thingie_normal_1\n',
    '#declare map = function(c) {map_1(c)}\n',
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
    f'#declare rnd_1 = seed({int(seconds * 1000000)});\n',
    '\n',
    # Starting scene content, main object
    '\n// Object thething made out of thingies\n',
    '#declare thething = union{\n',  # Opening big thething
])

# Internal strings for packing change
even_odd_string = ''
even_string = 'translate brickwall_offset'
odd_string = '// Odd row'

# Now going to cycle through image and build big thething

for y in range(0, Y, 1):

    message = ('Processing row ' + str(y) + ' of ' + str(Y) + '...')
    sortir.deiconify()
    zanyato.config(text=message)
    sortir.update()
    sortir.update_idletasks()

    resultfile.write(f'\n  // Row {y}\n')

    if (((y+1) % 2) == 0):
        even_odd_string = even_string
    else:
        even_odd_string = odd_string

    for x in range(0, X, 1):

        # Colors normalized to 0..1
        r = float(src(x, y, 0))/maxcolors
        g = float(src(x, y, 1))/maxcolors
        b = float(src(x, y, 2))/maxcolors

        # Something to map something to. By default - brightness, normalized to 0..1
        c = float(srcY(x, y))/maxcolors

        # alpha to be used for alpha dithering
        a = float(src(x, y, 3))/maxcolors
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
                f'      rotate((rotate_map * <map({c}), map({c}), map({c})>) + rotate_all)\n',
                f'      rotate(rotate_rnd * <rand(rnd_1), rand(rnd_1), rand(rnd_1)>)\n',
                f'      {even_odd_string}\n',
                f'      translate(move_map * <map({c}), map({c}), map({c})>)\n',
                f'      translate(move_rnd * <rand(rnd_1), rand(rnd_1), rand(rnd_1)>)\n',
                f'      translate<{x}, {y}, 0>\n',
                '    }\n'
            # Finished thingie
            ])

# Transform object to fit 1, 1, 1 cube at 0, 0, 0 coordinates
resultfile.writelines([
    '\n  // Object transforms to fit 1, 1, 1 cube at 0, 0, 0 coordinates\n',
    '  translate<0.5, 0.5, 0>\n',             # compensate of thingie size around zero
    f'  translate<{-0.5*X}, {-0.5*Y}, 0>\n',  # centering at scene zero
    f'  scale<{-1.0/max(X, Y)}, {-1.0/max(X, Y)}, {1.0/max(X, Y)}>\n',    # fitting and mirroring
    '} // thething closed\n\n'
])
# closing big thething

# Inserting big thething into scene
resultfile.write('object {thething}\n\n')

# Camera
proportions = max(X,Y)/X
resultfile.writelines([
    '#declare camera_height = 3.0;\n',
    'camera{\n',
    '  // orthographic\n',
    '  location<0.0, 0.0, camera_height>\n',
    '  right x*image_width/image_height\n',
    '  up y\n',
    '  direction <0, 0, 1>\n',
    f'  angle 2.0*(degrees(atan2({0.5 * proportions}, camera_height-(1.0/{max(X, Y)})))) // Supposed to fit object\n',
    '  look_at<0.0, 0.0, 0.0>\n',
    '}\n\n',
])

# Light 1
resultfile.write('light_source {0*x\n  color rgb<1.1, 1, 1>\n  translate<4, 2, 3>\n}\n\n')
# Light 2
resultfile.write('light_source {0*x\n  color rgb<0.9, 1, 1>\n  translate<-2, 6, 7>\n}\n\n')
# Signature
resultfile.write('\n/*\n\nhappy rendering\n\n  0~0\n (---)\n(.>|<.)\n-------\n\n*/')
# Close output
resultfile.close()

# --------------------------------------------------------------
# Destroying dialog

sortir.destroy()
sortir.mainloop()
# Dialog destroyed and closed
# --------------------------------------------------------------
