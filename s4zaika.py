#!/usr/bin/env python3

'''
POV Sphere Mosaic, square pattern
Program for conversion of image into a C4 symmetry set of tightly packed spheres,
colored according to source image pixels

Created by: Ilya Razmanov (mailto:ilyarazmanov@gmail.com)
            aka Ilyich the Toad (mailto:amphisoft@gmail.com)

Input: PNG
Output: POVRay

History:
2007  Initial AmphiSoft POV Sphere Mosaic, using FilterMeister https://filtermeister.com/
2023  Rewritten to Python
2024  Replaced Pillow I/O with PyPNG from: https://gitlab.com/drj11/pypng
2024  Complete internal rewriting. Versions from now on:

01.000  s4-zaika.py Initial release
01.001  Alpha support with pseudo-dithering
01.002  Some randomization added
01.003  Bugfix; z-displacement includes both brightness and random
01.004  s4zaika.py Naming convention change. Odd shift implemented, giving C2 "pentafive" output
        similar to "brickwall" of b4-zaika.
        Default output set to C4.
01.005 Output generalization.
01.006 Normal added, per-thingie rotated based on POVRay random.
       Output generalization, POVRay 3.5 statement updated to 3.7.
01.007  GUI improved.

    Project mirrors:
        https://github.com/Dnyarri/POVmosaic
        https://gitflic.ru/project/dnyarri/povmosaic

'''

__author__ = "Ilya Razmanov"
__copyright__ = "(c) 2007-2024 Ilya Razmanov"
__credits__ = "Ilya Razmanov"
__license__ = "unlicense"
__version__ = "2024.04.04"

__maintainer__ = "Ilya Razmanov"
__email__ = "ilyarazmanov@gmail.com"
__status__ = "Production"

from tkinter import Tk, Label, filedialog
from time import time, ctime
from random import random

import png                      # PNG reading: PyPNG from: https://gitlab.com/drj11/pypng

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

# Open source image
sourcefilename = filedialog.askopenfilename(title='Open source PNG file', filetypes=[
                                            ('PNG', '.png')], defaultextension=('PNG', '.png'))
if (sourcefilename == ''):
    quit()

source = png.Reader(filename=sourcefilename)  # starting PyPNG

# Opening image, iDAT comes to "pixels" as bytearray, to be tuple'd later
X, Y, pixels, info = source.asRGBA()
Z = (info['planes'])            # Maximum CHANNEL NUMBER
imagedata = tuple((pixels))     # Attempt to fix all bytearrays as tuple

if (info['bitdepth'] == 8):
    maxcolors = 255             # Maximal value for 8-bit channel
if (info['bitdepth'] == 16):
    maxcolors = 65535           # Maximal value for 16-bit channel

# Open export file
resultfile = filedialog.asksaveasfile(mode='w', title='Save resulting POV file', filetypes=[
    ('POV-Ray scene file', '*.pov'),
    ('All Files', '*.*'),],
    defaultextension=('POV-Ray scene file', '.pov'))
if (resultfile == ''):
    quit()
# Both files opened

# src a-la FM style src(x,y,z)
# Image should be opened as "imagedata" by main program before
# Note that X, Y, Z are not determined in function, you have to determine it in main program


def src(x, y, z):  # Analog src from FM, force repeate edge instead of out of range

    cx = x
    cy = y
    cx = max(0, cx)
    cx = min((X-1), cx)
    cy = max(0, cy)
    cy = min((Y-1), cy)

    # Here is the main magic of turning two x, z into one array position
    position = (cx*Z) + z
    channelvalue = int(((imagedata[cy])[position]))

    return channelvalue
# end of src function


def srcY(x, y):  # Converting to greyscale, returns Y, force repeate edge instead of out of range

    cx = x
    cy = y
    cx = max(0, cx)
    cx = min((X-1), cx)
    cy = max(0, cy)
    cy = min((Y-1), cy)

    if (info['planes'] < 3):    # supposedly L and LA
        Yntensity = src(x, y, 0)
    else:                       # supposedly RGB and RGBA
        Yntensity = int(0.2989*src(x, y, 0) + 0.587 *
                        src(x, y, 1) + 0.114*src(x, y, 2))

    return Yntensity
# end of srcY function

# WRITING POV FILE

# --------------------------------
#   POV header start
#


resultfile.writelines(['/*\n',
                       'Persistence of Vision Ray Tracer Scene Description File\n',
                       'Version: 3.7\n',
                       'Description: Mosaic picture consisting from solid spheres, C4 symmetry (square) packing\n',
                       'Author: Automatically generated by s4zaika program, based on AmphiSoft POV Sphere Mosaic plug-in, see POVRay Mosaic project at\n',
                       'https://github.com/Dnyarri/POVmosaic\n',
                       'https://gitflic.ru/project/dnyarri/povmosaic\n',
                       'developed by Ilya Razmanov aka Ilyich the Toad\n',
                       'https://dnyarri.github.io\n',
                       'mailto:ilyarazmanov@gmail.com\n',
                       '*/\n\n'
                       ])

resultfile.write(f'// Converted from: {sourcefilename} ')
seconds = time()
localtime = ctime(seconds)
resultfile.write(f'at: {localtime}\n')
resultfile.write(f'// Source info: {info}\n\n')

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
                       '\n\n'
                       ])
#
#   POV header end
# --------------------------------

# Thingie element
resultfile.writelines(['\n// Object thingie\n',
                       '#declare thingie = sphere { <0, 0, 0>, 0.5}\n',
                       '#declare thingie_finish = finish{ambient 0.1 diffuse 0.7 specular 0.8 roughness 0.001}\n',
                       '#declare color_factor = 1.5;    // Color multiplier for all channels\n',
                       '#declare displace_factor = 0.5; // z-Displace multiplier for all thingies. 0.0 makes strict plane output; 1.0 and higher not recommended\n',
                       '#declare xyzsize = 1.0;         // x,y,z-Size value for all thingies, does not affect packing. Default 1.0\n',
                       '\n// Thingie properties - normal\n',
                       '#declare normalheight = 0.25;   // Normal intensity. Default 0.25\n',
                       '#declare normalangle = 45;      // Normal is stretched at this angle to X, deg\n',
                       '#declare normalanglerange = 45; // Normal stretching angle randomly varies within this range, deg\n\n'
                       ])

# will rotate normal randomly around z
resultfile.write(f'#declare normalrand = seed({
                 int(seconds*10000000)});  // Seeding random\n')

# Object "thething" made of thingies

resultfile.write('\n// Object thething made out of thingies\n')
resultfile.write('#declare thething = union {\n')  # Opening object "thething"

# Internal strings for packing change

translatestring = ' '
oddtranslatestring = ' '  # no offset
eventranslatestring = ' '  # no offset for kartefour packing
# Below is 0.5 offset for pentafive packing, commented out by default
# eventranslatestring = ' translate <0.5, 0, 0> ' # 0.5 offset for pentafive packing

# Now going to cycle through image and build object

for y in range(0, Y, 1):

    message = ('Processing row ' + str(y) + ' of ' + str(Y) + '...')
    sortir.deiconify()
    zanyato.config(text=message)
    sortir.update()
    sortir.update_idletasks()

    resultfile.write(f'\n\n // Row {y}\n')

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
        yarkost = float(0.2989*r)+float(0.587*g)+float(0.114*b)
        tobeornottobe = random()     # to be used for alpha dithering
        zdisplacement = 0.0                 # original thingie position
        # Three strings below may be commented out to remove brightness dependence of z-displacement but NOT scaling
        zdisplacement = random()     # to be used for thingie z-displacement
        # zdisplacement = yarkost           # alternative thingie z-displacement
        # zdisplacement = yarkost * random()     # yet alternative thingie z-displacement

        # whether to draw thingie in place of partially transparent pixel or not
        if (a > tobeornottobe):
            # Opening object "thingie" to draw
            resultfile.write(
                '  object {thingie scale <xyzsize,xyzsize,xyzsize> pigment {')
            resultfile.write(
                f'rgb <color_factor*{r}, color_factor*{g}, color_factor*{b}>')
            # per-object normal, based on POVRay rand.
            resultfile.write(
                '} finish {thingie_finish} normal {bumps normalheight scale <0.5, 0.05, 0.1> rotate z*(normalangle + normalanglerange*rand(normalrand) - 0.5*normalanglerange)}')
            # resultfile.write('} finish {thingie_finish}')    # legacy close finish without normal
            resultfile.write(translatestring)
            resultfile.write(f'translate <{x}, {
                             y}, displace_factor*{zdisplacement}>')
            # Closing object "thingie" after modifications
            resultfile.write('}\n')

# Transform object to fit 1, 1, 1 cube at 0, 0, 0 coordinates
resultfile.write(
    '\n// Object transforms to fit 1, 1, 1 cube at 0, 0, 0 coordinates. Axes are mirrored to match Photoshop system.\n')
# compensate for -0.5 extra, now object fit 0..X, 0..Y, 0..maxcolors
resultfile.write('translate <0.5, 0.5, 0>\n')
# translate to center object bottom at x = 0, y = 0, z = 0
resultfile.write(f'translate <-0.5*{X}, -0.5*{Y}, 0>\n')
# rescale, mirroring POV coordinates to match Photoshop coordinate system
resultfile.write(
    f'scale <-1.0/{max(X, Y)}, -1.0/{max(X, Y)}, 1.0/{max(X, Y)}>\n')

resultfile.write('} // thething closed\n')   # Closing object "thething"

# Insert object into scene
resultfile.write('object {thething}\n')

# Camera
proportions = max(X, Y)/X
resultfile.write('#declare camera_height = 3.0;\n\n')
resultfile.write(
    'camera {\n   // orthographic\n    location <0.0, 0.0, camera_height>\n    right x*image_width/image_height\n    up y\n    direction <0,0,1>\n    angle 2.0*(degrees(atan2(')
resultfile.write(f'{0.5 * proportions}')
resultfile.write(
    f', camera_height-(1.0/{max(X, Y)})))) // Supposed to fit object \n    look_at <0.0, 0.0, 0.0>')
resultfile.write('\n}\n\n')

# Light 1
resultfile.write(
    'light_source {0*x\n   color rgb <1.1,1,1>\n   translate <4, 2, 3>}\n\n')
# Light 2
resultfile.write(
    '/* light_source {0*x\n   color rgb <0.9,1,1>\n   translate <-2, 6, 7>} */\n\n')
resultfile.write(
    '\n/*\n\nhappy rendering\n\n  0~0\n (---)\n(.>|<.)\n-------\n\n*/')
# Close output
resultfile.close()

# --------------------------------------------------------------
# Destroying dialog

sortir.destroy()
sortir.mainloop()

# Dialog destroyed and closed
# --------------------------------------------------------------
