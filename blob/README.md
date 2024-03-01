**(EN)** [(RU)](README.RU.md)

# Bitmap to 3D blob mosaic converter

Python utility for conversion of bitmap image (in [PNG format](http://www.libpng.org/pub/png/)) to some sort of solid blob mosaic in [POVRay](https://www.povray.org/) format.

*Brief program description - solid blob mosaic*

- **blob-s3zaika.py** - converts every single pixel into sphere blob componet. Spheres are packed into triangle grid (C<sub>*3*</sub> symmetry).

- **blob-s4zaika.py** - converts every single pixel into sphere blob componet. Spheres are packed into square grid (C<sub>*4*</sub> symmetry).

*Dependencies:* Tkinter, PyPNG

*Usage:* programs are equipped with minimal GUI, so all you have to do after starting the programs is use standard "Open..." GUI to open image file, then use standard "Save..." GUI to set POVRay scene file to be created, then wait while program does the job, then open resulting POV file with POVRay and render the scene. Scene contains enough basic stuff (globals, light, camera) to be rendered successfully right after exporting without any editing.

![Example of blob-s3zaika export rendering](https://dnyarri.github.io/imgzaika/640/blob-s3zaika.png)

Project mirrors:

[github Dnyarri](https://github.com/Dnyarri/POVmosaic)

[gitflic Dnyarri](https://gitflic.ru/project/dnyarri/povmosaic)
