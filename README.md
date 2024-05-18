**(EN)** [(RU)](README.RU.md)

# Bitmap to 3D solid mosaic converter

Python utilities for conversion of bitmap image (in [PNG format](http://www.libpng.org/pub/png/)) to some sort of solid objects mosaic in [POVRay](https://www.povray.org/) format. Development is likely to be continued, program list is about to propagate.

![Example of p6zaika export rendering](https://dnyarri.github.io/imgzaika/640/p6zaika.png)

## Brief programs description - simple solid primitives  

- **s3zaika** - converts every single pixel into solid sphere. *S*pheres are packed into triangle grid (C<sub>*3*</sub> symmetry). Sphere height over source plane depends on random, adding some releif to avoid monotonous shadow pattern.
- **s4zaika** - converts every single pixel into solid sphere. *S*pheres are packed into square grid (C<sub>*4*</sub> symmetry). Sphere height over source plane depends on random.
- **c3zaika** - converts every single pixel into solid cylinder. *C*ylinders are packed into triangle grid (C<sub>*3*</sub> symmetry). Cylinder height over source plane depends on source image brightness, adding some releif (like rough heightfiled). Overall, it may be considered as hybrid of s3zaika (C<sub>*3*</sub> symmetry) and b4zaikaS (height mapped to source brightness) using cylinders.
- **b4zaikaS** - converts every single pixel into solid box. *B*oxes are packed into square grid (C<sub>*4*</sub> symmetry, regular plane partition *4<sub>4</sub>*) and *S*caled so that box height is controlled by source image brightness, adding some releif (like rough heightfiled).
- **b4zaikaR** - converts every single pixel into solid box. *B*oxes are packed into square grid (C<sub>*4*</sub> symmetry) and *R*otated randomly around x,y and according to source image brightness around z, thus providing some artistic effect.
- **p3zaika** - converts every single pixel into solid triangle prism. *P*risms are packed into triangle grid (C<sub>*3*</sub> symmetry) - *3<sub>6</sub>* regular plane partition - and scaled so that prism height is controlled by source image brightness, adding some releif (like rough heightfiled).
- **p6zaika** - converts every single pixel into solid hexagonal prism. *P*risms are packed into hexagonal grid (C<sub>*6*</sub> symmetry) - a **honey comb** regular plane partition *6<sub>3</sub>* - and scaled so that prism height is controlled by source image brightness, adding some releif (like rough heightfiled made of pencils).

## Subfolders description - solid complex objects  

- **superellipsoid/** - programs to convert every single pixel into superellipsoid. Placement similar to b4zaika(s); superellipsoid parameters are random. General effect is rather pop than artistic.

- **blob/** - programs converting every single pixel into blob component. Component (sphere) properties and blob threshold are easy to edit, resulting to quite impressive changes.

- **tori/** - programs for simulating canvas and cross-stitch.

![Example of linen export rendering](https://dnyarri.github.io/imgzaika/640/linen.png)

*Dependencies:* Tkinter, PyPNG

*Usage:* programs are equipped with minimal GUI, so all you have to do after starting the programs is use standard "Open..." GUI to open image file, then use standard "Save..." GUI to set POVRay scene file to be created, then wait while program does the job, then open resulting POV file with POVRay and render the scene. Scene contains enough basic stuff (globals, light, camera) to be rendered successfully right after exporting without any editing.

[Project website](https://dnyarri.github.io/)

Project mirrors:

[github Dnyarri](https://github.com/Dnyarri/POVmosaic)

[gitflic Dnyarri](https://gitflic.ru/project/dnyarri/povmosaic)
