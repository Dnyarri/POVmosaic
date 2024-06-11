# POVRay mosaic - Bitmap to 3D solid mosaic converter

Python utilities for conversion of bitmap image (in PNG format) to some sort of solid objects mosaic in [POVRay](https://www.povray.org/) format. Each source image pixel is converted to a 3D object, and objects are packed side by side, forming a grid.

![Example of p6zaika export rendering](https://dnyarri.github.io/imgzaika/640/p6zaika.png)

## Brief programs description  

- **3zaika** - converts every single pixel into 3D object, by default a solid sphere. Spheres are packed into triangle grid. Spheres may be easily replaced by other predefined objects, object positions and properties may be mapped to source image brightness and/or randomized, etc.
- **4zaika** - converts every single pixel into 3D object, by default a solid cube. Cubes are packed into square grid. Spheres may be easily replaced by other predefined objects, object positions and properties may be mapped to source image brightness and/or randomized, etc.

*Dependencies:* Tkinter, [PyPNG](https://gitlab.com/drj11/pypng)

*Usage:* programs are equipped with minimal GUI for file selection. Exported scene contains enough basic stuff (globals, light, camera) to be rendered out of the box, and is well structured and commented for further editing.

[Project website](https://dnyarri.github.io/)

Project mirrors:

[github Dnyarri](https://github.com/Dnyarri/POVmosaic)

[gitflic Dnyarri](https://gitflic.ru/project/dnyarri/povmosaic)
