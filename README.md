**(EN)** [(RU)](README.RU.md)

# Bitmap to 3D solid mosaic converter

Python utilities for conversion of bitmap image (in [PNG format](http://www.libpng.org/pub/png/)) to some sort of solid objects mosaic in [POVRay](https://www.povray.org/) format. Development is likely to be continued, program list is about to propagate.

*Brief programs description*

- **s4-zaika** - converts every single pixel into solid sphere. Spheres packed into square grid. Sphere height over source plane depends on source brightness and random, adding some releif.
- **b4-zaika** - converts every single pixel into solid box. Boxes packed into square grid. Box height is controlled by source brightness, adding some releif (like rough heightfiled).

*Dependencies:* Tkinter, PyPNG

*Usage:* programs are equipped with minimal GUI, so all you have to do after starting the programs is use standard "Open..." GUI to open image file, then use standard "Save..." GUI to set POVRay scene file to be created, then wait while program does the job, then open resulting POV file with POVRay and render the scene. Scene contains enough basic stuff (globals, light, camera) to be rendered successfully right after exporting without any editing.

Project mirrors:

[github Dnyarri](https://github.com/Dnyarri/POVmosaic)

[gitflic Dnyarri](https://gitflic.ru/project/dnyarri/povmosaic)
