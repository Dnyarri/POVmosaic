**(EN)** [(RU)](README.RU.md)

# Bitmap to 3D solid mosaic converter

Python utilities for conversion of bitmap image (in [PNG format](http://www.libpng.org/pub/png/)) to some sort of solid objects mosaic in [POVRay](https://www.povray.org/) format. Development is likely to be continued, program list is about to propagate.

*Brief programs description*

- **s3zaika** - converts every single pixel into solid sphere. *S*pheres are packed into triangle grid (C<sub>*3*</sub> symmetry). Sphere height over source plane depends on random, adding some releif to avoid monotonous shadow pattern.
- **s4zaika** - converts every single pixel into solid sphere. *S*pheres are packed into square grid (C<sub>*4*</sub> symmetry). Sphere height over source plane depends on random.
- **c3zaika** - converts every single pixel into solid cylinder. *C*ylinders are packed into triangle grid (C<sub>*3*</sub> symmetry). Cylinder height over source plane depends on source brightness, adding some releif (like rough heightfiled). Overall, consider it as hybrid of s3zaika (C<sub>*3*</sub> symmetry) and b4zaikaS (height according to source) using cylinders.
- **b4zaikaS** - converts every single pixel into solid box. *B*oxes are packed into square grid (C<sub>*4*</sub> symmetry) and *S*caled so that box height is controlled by source brightness, adding some releif (like rough heightfiled).
- **b4zaikaR** - converts every single pixel into solid box. *B*oxes are packed into square grid (C<sub>*4*</sub> symmetry) and *R*otated randomly around x,y and according to source image brightess around z, that provides some artistic effect.

*Dependencies:* Tkinter, PyPNG

*Usage:* programs are equipped with minimal GUI, so all you have to do after starting the programs is use standard "Open..." GUI to open image file, then use standard "Save..." GUI to set POVRay scene file to be created, then wait while program does the job, then open resulting POV file with POVRay and render the scene. Scene contains enough basic stuff (globals, light, camera) to be rendered successfully right after exporting without any editing.

Project mirrors:

[github Dnyarri](https://github.com/Dnyarri/POVmosaic)

[gitflic Dnyarri](https://gitflic.ru/project/dnyarri/povmosaic)
