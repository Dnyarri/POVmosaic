#!/usr/bin/env python3

'''
POV Mosaic, Triangle packing, Regular plane partition 6/3

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
1.7.9.10    Bilinear interpolation added to map. Not used for coloring since results are too smooth.
1.7.16.17   Coordinate system match Photoshop, origin is top left, z points to the viewer.
            Camera improved. Global color modifier changed to transfer function. Scaling changed from subtractive to additive, be careful with old presets if they include scaling!
1.7.17.1    Global/individual texture switch added for pseudo-heightmap effects.
1.7.22.12   Renamed to 63zaika to reflect regular plane partition class 6/3. Prisms changed.
            Ready for release.
1.7.24.15   Changed even/odd rotate to even/odd transform. Updated presets for compatibility.
1.9.1.0     Reworked normals.
1.9.16.2    Added global transform, changed randoms in normal and move from + to +/-,
            changed globals in export to UTF-8, added gamma note etc.
1.11.1.1    Per thingie texture overlay.

-------------------
Main site:
https://dnyarri.github.io

Project mirrored at:
https://github.com/Dnyarri/POVmosaic
https://gitflic.ru/project/dnyarri/povmosaic

'''

__author__ = 'Ilya Razmanov'
__copyright__ = '(c) 2007-2024 Ilya Razmanov'
__credits__ = 'Ilya Razmanov'
__license__ = 'unlicense'
__version__ = '1.11.1.1'
__maintainer__ = 'Ilya Razmanov'
__email__ = 'ilyarazmanov@gmail.com'
__status__ = 'Production'

import random
from time import ctime, time
from tkinter import BOTH, PhotoImage, Tk, filedialog
from tkinter.ttk import Progressbar

import png  # PNG reading: PyPNG from: https://gitlab.com/drj11/pypng

# Creating dialog {#888888, 9}
sortir = Tk()
sortir.title('POVRay Mosaic: 63Zaika')
sortir.geometry(f'500x16+{(sortir.winfo_screenwidth()-500)//2}+{(sortir.winfo_screenheight()-16)//2}')
sortir.resizable(width=True, height=True)
sortir.iconphoto(True, PhotoImage(data='P6\n4 4\n255\n'.encode() + random.randbytes(48)))
progressbar = Progressbar(sortir, orient='horizontal', mode='determinate', value=0, maximum=100, length=500)
progressbar.pack(fill=BOTH, expand=True)
sortir.overrideredirect(True)
sortir.withdraw()
# Main dialog created and hidden

# Open source image, first get name {#6666ff, 4}
sourcefilename = filedialog.askopenfilename(title='63zaika: Open source PNG file', filetypes=[('PNG', '.png')], defaultextension=('PNG', '.png'))
if sourcefilename == '':
    sortir.destroy()
    quit()

# open PNG file {#6666ff, 16}
source = png.Reader(filename=sourcefilename)  # starting PyPNG

# Opening image, iDAT comes to "pixels" generator, to be tuple'd later
X, Y, pixels, info = source.asRGBA()
Z = info['planes']  # Maximum channel number
imagedata = tuple(pixels)  # Building tuple from generator

if info['bitdepth'] == 8:
    maxcolors = 255  # Maximal value for 8-bit channel
if info['bitdepth'] == 16:
    maxcolors = 65535  # Maximal value for 16-bit channel

if 'gamma' in info:
    gamma_note = f'Source PNG gAMA value is {info['gamma']}'
else:
    gamma_note = 'Source PNG gAMA was absent'

# opening result file, first get name  {#6666ff, 14}
resultfilename = filedialog.asksaveasfilename(
    title='63zaika: Save POVRay scene file',
    filetypes=[
        ('POV-Ray scene file', '*.pov'),
        ('All Files', '*.*'),
    ],
    defaultextension=('POV-Ray scene file', '.pov'),
)
if (resultfilename == '') or (sourcefilename is None):
    sortir.destroy()
    quit()

# open POV file
resultfile = open(resultfilename, 'w')


def src(x, y, z):  # {#884400, 19}
    '''
    Analog of src from FM, force repeat edge instead of out of range.
    Returns int channel value z for pixel x, y

    '''

    cx = int(x)
    cy = int(y)
    cx = max(0, cx)
    cx = min((X - 1), cx)
    cy = max(0, cy)
    cy = min((Y - 1), cy)

    # Here is the main magic of turning two x, z into one array position
    position = (cx * Z) + z
    channelvalue = int((imagedata[cy])[position])

    return channelvalue


# end of src function


def src_lum(x, y):  # {#884400, 19}
    '''
    Returns brightness of pixel x, y

    '''

    if info['planes'] < 3:  # supposedly L and LA
        yntensity = src(x, y, 0)
    else:  # supposedly RGB and RGBA
        yntensity = int(0.2989 * src(x, y, 0) + 0.587 * src(x, y, 1) + 0.114 * src(x, y, 2))

    return yntensity


# end of src_lum function


def src_lum_blin(x, y):  # {#884400, 25}
    '''
    Analog of src_lum above, but returns bilinearly interpolated brightness of pixel x, y

    '''

    fx = float(x)
    fy = float(y)  # Uses float input coordinates for interpolation

    # Neighbor pixels coordinates (square corners x0,y0; x1,y0; x0,y1; x1,y1)
    x0 = int(x)
    x1 = x0 + 1
    y0 = int(y)
    y1 = y0 + 1

    # Reading corners src (see scr above) and interpolating    # {#880000, 3}
    channelvalue = (
        src_lum(x0, y0) * (x1 - fx) * (y1 - fy) + src_lum(x0, y1) * (x1 - fx) * (fy - y0) + src_lum(x1, y0) * (fx - x0) * (y1 - fy) + src_lum(x1, y1) * (fx - x0) * (fy - y0)
    )

    return int(channelvalue)


# end of src_lum_blin function

# WRITING POV FILE  # {#ff0000}

seconds = time()
localtime = ctime(seconds)  # will be used for randomization and for debug info

resultfile.writelines(  # POV header start {#660000}
    [
        '/*\n',
        'Persistence of Vision Ray Tracer Scene Description File\n',
        'Version: 3.7\n',
        'Description: Mosaic picture consisting from solid spheres, triangle packing, Regular plane partition 6/3.\n',
        '             Other included objects are hexagonal prisms (honeycomb packing), cylinders,\n',
        '             etc., see list "#declare thingie_1=" below.\n',
        'Author: Automatically generated by 63zaika program, based on AmphiSoft POV Sphere Mosaic plug-in, see POVRay Mosaic project at\n',
        'https://github.com/Dnyarri/POVmosaic\n',
        'https://gitflic.ru/project/dnyarri/povmosaic\n\n',
        'developed by Ilya Razmanov aka Ilyich the Toad\n',
        'https://dnyarri.github.io\n',
        'mailto:ilyarazmanov@gmail.com\n\n',
        f'Generated by: {__file__} ver: {__version__} at: {localtime}\n'
        f'Converted from: {sourcefilename}\n'
        f'Source info: {info}\n'
        '*/\n\n',
    ]
)

resultfile.writelines(  # Globals {#660000}
    [
        '\n',
        '#version 3.7;\n\n',
        'global_settings{\n',
        '    max_trace_level 3   // Small to speed up preview. May need to be increased for metals\n',
        '    adc_bailout 0.01    // High to speed up preview. May need to be decreased to 1/256\n',
        f'    assumed_gamma 1.0   // {gamma_note}, that may or may not be of value.\n',
        '    ambient_light <0.5, 0.5, 0.5>\n',
        '    charset utf8\n',
        '}\n\n',
        '#include "finish.inc"\n',
        '#include "metals.inc"\n',
        '#include "golds.inc"\n',
        '#include "glass.inc"\n',
        '#include "functions.inc"\n',
        '\n',
    ]
)
#   POV header end

# --------------------------------
# Thingie element, then scene
resultfile.writelines(
    [
        '\n// Necessary math stuff set as de facto constants to avoid importing math\n',
        '#declare sqrtof3 = 1.7320508075688772935274463415059;   // sqrt(3)\n',
        '#declare revsqrtof3 = 1.0/sqrtof3;                      // 1.0/sqrt(3)\n\n',
        '\n/*  -------------------------\n    |  Predefined variants  |\n    -------------------------  */\n',
        '\n//       Thingie variants\n',
        '#declare thingie_1 = sphere{<0, 0, 0>, 0.5}\n',
        '#declare thingie_2 = cylinder{<0, 0, 0>, <0, 0, 1.0>, 0.5}\n',
        '#declare thingie_3 = cone{<0, 0, 0>, 0.5, <0, 0, 1.0>, 0.0}\n',
        '// Hexagonal prism below, like pencils in honeycomb pack. Try conic_sweep as well\n',
        '#declare thingie_4 = prism{linear_sweep linear_spline -1, 0, 7,\n <-0.5, 0.5*revsqrtof3>, <0,revsqrtof3>, <0.5, 0.5*revsqrtof3>,\n <0.5,- 0.5*revsqrtof3>, <0,-revsqrtof3>, <-0.5,- 0.5*revsqrtof3>,\n <-0.5, 0.5*revsqrtof3> rotate x*90 translate z}\n',
        '// Rhomb prism below. Try conic_sweep as well\n',
        '#declare thingie_5 = prism{linear_sweep linear_spline -1, 0, 5, <-1.0, 0>,\n <0, sqrtof3>, <1, 0>, <0, -sqrtof3>, <-1.0, 0> rotate x*90 scale 0.5 translate z}\n',
        '// CSG examples below, may be good for randomly rotated thingies\n',
        '#declare thingie_6 = intersection{\n    cylinder{<0, 0, -1.0>, <0, 0, 1.0>, 0.5}\n    cylinder{<0, 0, -1.0>, <0, 0, 1.0>, 0.5 rotate x*90}\n    cylinder{<0, 0, -1.0>, <0, 0, 1.0>, 0.5 rotate y*90}\n  }  //  Cubic rounded CSG end\n',
        '#declare thingie_7 = intersection{\n    cylinder{<0, -1.0, 0>, <0, 1.0, 0>, 0.5}\n    cylinder{<0, -1.0, 0>, <0, 1.0, 0>, 0.5 rotate z*109.5}\n    cylinder{<0, -1.0, 0>, <0, 1.0, 0>, 0.5 rotate z*109.5 rotate y*109.5}\n    cylinder{<0, -1.0, 0>, <0, 1.0, 0>, 0.5 rotate z*109.5 rotate y*219.0}\n  }  //  Tetrahedral rounded CSG end\n',
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
        '#declare counts = 8; #declare thingie_normal_5 = normal{function{mod(abs(cos(counts*x)+cos(-counts*y)+cos(counts*z)), 1)}}  // Typically counts 4-16 is acceptable\n',
        '#declare thingie_normal_6 = normal{function{64*abs(x*y*z)}}\n',
        '\n/*  ----------------------------------------------------\n    |  Global modifiers for all thingies in the scene  |\n    ----------------------------------------------------  */\n\n',
        '#declare thingie_texture_2 = texture {  // Define transparent texture overlay here\n',
        '  pigment {gradient z colour_map {[0.0, rgbt <0,0,0,1>] [1.0, rgbt <0,0,0,1>]} scale 0.1 rotate <30, 30, 0>}};\n\n',  # Transparent texture overlay
        '#declare yes_color = 1;         // Whether source per-thingie color is taken or global patten applied\n',
        '// Color-relater settings below work only for "yes_color = 1;"\n',
        '#declare cm = function(k) {k}   // Color transfer function for all channels, all thingies\n',
        '#declare f_val = 0.0;           // Filter value for all thingies\n',
        '#declare t_val = 0.0;           // Transmit value for all thingies\n',
        '\n#declare evenodd_transform = transform {rotate <0.0, 0.0, 0.0>}  // Odd lines rotate, rarely useful\n',
        '\n/*       Map function\nMaps are transfer functions control value (i.e. source pixel brightness) is passed through.\n',
        'By default exported map is five points linear spline, control points are set in the table below,\n',
        'first column is input, first digits in second column is output for this input.\n',
        'Note that by default input=output, i.e. no changes applied to source pixel brightness. */\n\n',
        '#declare Curve = function {  // Spline curve construction begins\n',
        '  spline { linear_spline\n',
        '    0.0,   <0.0,   0>\n',
        '    0.25,  <0.25,  0>\n',
        '    0.5,   <0.5,   0>\n',
        '    0.75,  <0.75,  0>\n',
        '    1.0,   <1.0,   0>}\n  }  // Construction complete\n',
        '#declare map = function(c) {Curve(c).u}  // Spline curve assigned as map\n',
        '\n/*  -------------------------------------------\n    |  Selecting variants, configuring scene  |\n    -------------------------------------------  */\n\n',
        '#declare thingie = thingie_1\n',
        '#declare thingie_finish = thingie_finish_1\n',
        '#declare thingie_normal = thingie_normal_1\n',
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
        f'#declare thething_interior = interior {{ior 2.0 fade_power 1.5 fade_distance 1.0*{1.0/max(X, Y)} fade_color <0.0, 0.5, 1.0>}}\n',
        '//       Common transform for the whole thething, placed here just to avoid scrolling\n',
        '#declare thething_transform = transform {\n  // You can place your global scale, rotate etc. here\n}\n',
        '\n//       Seed random\n',
        f'#declare rnd_1 = seed({int(seconds * 1000000)});\n\n',
        'background{color rgbft <0, 0, 0, 1, 1>} // Hey, I' 'm just trying to be explicit in here!\n\n',
        # Camera {#ff0000, 0}
        '\n/*\n  Camera and light\n\n',
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
        # Light {#ff0000, 0}
        'light_source{0*x\n  color rgb<1.1, 1.0, 1.0>\n//  area_light <1, 0, 0>, <0, 1, 0>, 5, 5 circular orient area_illumination on\n  translate<4, -2, 3>\n}\n\n',
        'light_source{0*x\n  color rgb<0.9, 1.0, 1.0>\n//  area_light <1, 0, 0>, <0, 1, 0>, 5, 5 circular orient area_illumination on\n  translate<-2, -6, 7>\n}\n\n',
        '\n/*  ----------------------------------------------\n    |  Insert preset to override settings above  |\n    ----------------------------------------------  */\n\n',
        '// #include "preset.inc"    // Set path and name of your file related to scene file\n\n',
        # Main object
        '\n// Object thething made out of thingies\n',
        '#declare thething = union{\n',  # Opening big thething
    ]
)

# Internal strings for packing change {#ff0000, 0}

'''
Below is height of triangle with 2*0.5 sides, that is vertical distance between two 0.5 radius spheres as defined by thingie.
sqrt(3) = 1.732... hardcoded to remove math export
'''
triangle_height = 0.5 * 1.7320508075688772935274463415059

even_odd_string = ''
even_string = 'translate<0.5, 0, 0>'  # mandatory shift for triangle pattern, uneditable
odd_string = 'transform {evenodd_transform}'  # consider 'rotate<0.0, 0.0, 180.0>' or scale <1.0, -1.0, 1.0>

# Now going to cycle through image and build big thething
Ycount = int(Y / triangle_height)
progressbar.config(maximum=Ycount)

for y in range(0, Ycount, 1):
    sortir.deiconify()  # {#888888, 3}
    progressbar.config(value=y)
    sortir.update()
    sortir.update_idletasks()

    resultfile.write(f'\n  // Row {y}\n')

    if ((y + 1) % 2) == 0:
        even_odd_string = even_string
        even_odd_trans = 0.5
    else:
        even_odd_string = odd_string
        even_odd_trans = 0.0

    for x in range(0, X, 1):
        # Colors normalized to 0..1
        r = float(src(x, y * triangle_height, 0)) / maxcolors
        g = float(src(x, y * triangle_height, 1)) / maxcolors
        b = float(src(x, y * triangle_height, 2)) / maxcolors

        # Something to map something to. By default - brightness, normalized to 0..1
        # c = float(src_lum(x, y*triangle_height))/maxcolors # Nearest neighbor
        c = float(src_lum_blin(x + even_odd_trans, y * triangle_height)) / maxcolors  # Bilinear

        # alpha to be used for alpha dithering
        a = float(src(x, y * triangle_height, 3)) / maxcolors
        # a = 0 is transparent, a = 1.0 is opaque
        tobe_or_nottobe = a > random.random()

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
                    f'      scale(<1, 1, 1> + (scale_map * <map({c}), map({c}), map({c})>))\n',
                    f'      rotate(rotate_map * <map({c}), map({c}), map({c})>)\n',
                    '      rotate(rotate_rnd * (<rand(rnd_1), rand(rnd_1), rand(rnd_1)-0.5>))\n',
                    f'      {even_odd_string}\n',
                    f'      translate(move_map * <map({c}), map({c}), map({c})>)\n',
                    '      translate(move_rnd * (<rand(rnd_1), rand(rnd_1), rand(rnd_1)>-0.5))\n',
                    f'      translate<{x}, {y*triangle_height}, 0>\n',
                    '    }\n',
                    # Finished thingie
                ]
            )

# Transform object to fit 1, 1, 1 cube at 0, 0, 0 coordinates
resultfile.writelines(
    [
        '\n  // Object transforms to fit 1, 1, 1 cube at 0, 0, 0 coordinates\n',
        f'  translate <0.25, 0.5, 0> + <{-0.5*X}, {-0.5*Y}, 0>\n',  # centering at scene zero
        f'  scale<{1.0/max(X, Y)}, {1.0/max(X, Y)}, {1.0/max(X, Y)}>\n',  # fitting
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

# Close output {#ff0000}
resultfile.close()

# --------------------------------------------------------------  {#888888, 3}
sortir.destroy()
sortir.mainloop()
# Dialog destroyed and closed
