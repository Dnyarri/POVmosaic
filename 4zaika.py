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

0.0.01      Complete rewriting to more flexible project - 21 May 2024.

    Project mirrors:
        https://github.com/Dnyarri/POVmosaic
        https://gitflic.ru/project/dnyarri/povmosaic

'''

__author__ = "Ilya Razmanov"
__copyright__ = "(c) 2007-2024 Ilya Razmanov"
__credits__ = "Ilya Razmanov"
__license__ = "unlicense"
__version__ = "0.0.01"
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

# WRITING POV FILE

seconds = time(); localtime = ctime(seconds)    # will be used for randomization and for debug info

# --------------------------------
#   POV header start
#
resultfile.writelines(['/*\n',
    'Persistence of Vision Ray Tracer Scene Description File\n',
    'Version: 3.7\n',
    'Description: Mosaic picture consisting from solid boxes, C4 symmetry (square) packing.\n',
    'Author: Automatically generated by 4zaika program, based on AmphiSoft POV Sphere Mosaic plug-in, see POVRay Mosaic project at\n',
    'https://github.com/Dnyarri/POVmosaic\n',
    'https://gitflic.ru/project/dnyarri/povmosaic\n',
    'developed by Ilya Razmanov aka Ilyich the Toad\n',
    'https://dnyarri.github.io\n',
    'mailto:ilyarazmanov@gmail.com\n',
    f'Converted from: {sourcefilename} at: {localtime}\n'
    f'Source info: {info}\n'
    '*/\n\n',
])

#   Globals
resultfile.writelines(['\n',
                       '#version 3.7;\n\n',
                       'global_settings{\n',
                       '    max_trace_level 3   // Small to speed up preview. May need to be increased for metals\n',
                       '    adc_bailout 0.01    // High to speed up preview. May need to be decreased to 1/256\n',
                       '    ambient_light <0.5,0.5,0.5>\n',
                       '    assumed_gamma 1.0\n}\n\n',
                       '#include "colors.inc"\n',
                       '#include "finish.inc"\n',
                       '#include "metals.inc"\n',
                       '#include "golds.inc"\n',
                       '\n'
                       ])
#   POV header end
# --------------------------------

# --------------------------------
# Thingie element, then scene
resultfile.writelines([
        '\n// Thingie variants\n',
        '#declare thingie1 = box{<-0.5, -0.5, 0.0>, <0.5, 0.5, 1.0>}\n',
        '#declare thingie2 = sphere{<0, 0, 0>, 0.5}\n',
        '#declare thingie3 = cylinder{<0, 0, 0>, <0, 0, 1.0>, 0.5}\n',
        '\n// Thingie finish variants\n',
        '#declare thingie_finish1 = finish{ambient 0.1 diffuse 0.7 specular 0.8 roughness 0.001}\n',
        '#declare thingie_finish2 = Dull  // Example of using simple finish from finish.inc\n',
        '#declare thingie_finish3 = F_MetalE  // Example of using complex finish from golds.inc\n',
        '\n// Thingie normal variants\n',
        '#declare thingie_normal1 = normal{bumps 0.0}\n',
        '#declare thingie_normal2 = normal{bumps 1.0 scale<0.01, 0.01, 0.01>}\n',
        '#declare thingie_normal3 = normal{bumps 1.0 scale<0.5, 0.05, 0.05> rotate<0, 0, 30>}\n',
        '\n// Global modifiers for all thingies in the scene\n',
        '#declare color_factor = 1.0;    // Color multiplier for all channels\n',
        '\n// Selecting from variants\n',
        '#declare thingie = thingie1\n',
        '#declare thingie_finish = thingie_finish1\n',
        '#declare thingie_normal = thingie_normal1\n',
        '\n',
        # Starting scene content
        '\n// Object thething made out of thingies\n',
        '#declare thething = union{\n',  # Opening big thething
])


# Internal strings for packing change
translatestring = ''
oddtranslatestring = ''     # no offset
eventranslatestring = ''    # no offset for square packing
# Below is 0.5 offset for "brick" packing, commented out by default
# eventranslatestring = ' translate <0.5, 0, 0> ' # 0.5 offset for "brick" packing

# Now going to cycle through image and build object

for y in range(0, Y, 1):

    message = ('Processing row ' + str(y) + ' of ' + str(Y) + '...')
    sortir.deiconify()
    zanyato.config(text=message)
    sortir.update()
    sortir.update_idletasks()

    resultfile.write(f'\n  // Row {y}\n')

    if (((y+1) % 2) == 0):
        translatestring = eventranslatestring
    else:
        translatestring = oddtranslatestring

    for x in range(0, X, 1):

        r = float(src(x, y, 0))/maxcolors
        g = float(src(x, y, 1))/maxcolors
        b = float(src(x, y, 2))/maxcolors    # Normalize colors to 0..1.0
        # a = 0 - transparent, a = 1.0 - opaque
        a = float(src(x, y, 3))/maxcolors
        tobeornottobe = random()     # to be used for alpha dithering
        yarkost = srcY(x,y)  # brightness

        # whether to draw thingie in place of partially transparent pixel or not
        if (a > tobeornottobe):
            # Opening object "thingie" to draw
            resultfile.writelines([
                '    object{thingie\n',
                f'      pigment{{rgb<color_factor*{r}, color_factor*{g}, color_factor*{b}>}}\n',
                '      finish{thingie_finish}\n',
                '      normal{thingie_normal}\n',
                f'      translate<{x}, {y}, 0>\n',
                '    }\n'
            # Finished thingie
            ])

# Transform object to fit 1, 1, 1 cube at 0, 0, 0 coordinates
resultfile.writelines([
    '\n  // Object transforms to fit 1, 1, 1 cube at 0, 0, 0 coordinates\n',
    '  translate<0.5, 0.5, 0>\n',             # compensate of thingie size around zero
    f'  translate<-0.5*{X}, -0.5*{Y}, 0>\n',  # centering at scene zero
    f'  scale<-1.0/{max(X, Y)}, -1.0/{max(X, Y)}, 1.0/{max(X, Y)}>\n',    # fitting and mirroring
    '} // thething closed\n\n'
])

# Insert object into scene
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
    '  direction <0,0,1>\n',
    f'  angle 2.0*(degrees(atan2({0.5 * proportions}, camera_height-(1.0/{max(X, Y)})))) // Supposed to fit object\n',
    '  look_at<0.0, 0.0, 0.0>\n',
    '}\n\n',
])

# Light 1
resultfile.write('light_source {0*x\n  color rgb<1.1,1,1>\n  translate<4, 2, 3>\n}\n\n')
# Light 2
resultfile.write('light_source {0*x\n  color rgb<0.9,1,1>\n  translate<-2, 6, 7>\n}\n\n')
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