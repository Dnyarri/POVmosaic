**(EN)** [(RU)](README.RU.md)

# Bitmap to 3D superellipsoid mosaic converter

Python utility for conversion of bitmap image (in [PNG format](http://www.libpng.org/pub/png/)) to some sort of solid superellipsoid mosaic in [POVRay](https://www.povray.org/) format.

![Example of superzaika export rendering](https://dnyarri.github.io/imgzaika/320/superzaika.png)

*Brief program description - solid superellipsoid mosaic*

- **superzaika.py** - converts every single pixel into superellipsoid. Superellipsoids are packed into square grid (C<sub>*4*</sub> symmetry); every superellipsoid parameters are random. General effect is rather pop than artistic.

*Dependencies:* Tkinter, PyPNG

*Usage:* programs are equipped with minimal GUI, so all you have to do after starting the programs is use standard "Open..." GUI to open image file, then use standard "Save..." GUI to set POVRay scene file to be created, then wait while program does the job, then open resulting POV file with POVRay and render the scene. Scene contains enough basic stuff (globals, light, camera) to be rendered successfully right after exporting without any editing.

Project mirrors:

[github Dnyarri](https://github.com/Dnyarri/POVmosaic)

[gitflic Dnyarri](https://gitflic.ru/project/dnyarri/povmosaic)
