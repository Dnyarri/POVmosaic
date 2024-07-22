# POVRay mosaic - Bitmap to 3D solid mosaic converter

Python utilities for conversion of bitmap image (in PNG format) to some sort of solid objects mosaic in [POVRay](https://www.povray.org/) format. Each source image pixel is converted to a 3D object, and objects are packed side by side, forming a grid following [Euclidean tilings](https://en.wikipedia.org/wiki/List_of_regular_polytopes#Euclidean_tilings).

![Example of 63zaika export rendering](https://dnyarri.github.io/3z/301.png)

## Brief programs description  

- **63zaika** - converts every single pixel into 3D object, by default a solid sphere. Spheres are packed into triangle/hexagone grid. Spheres may be easily replaced by other predefined objects, object positions and properties may be mapped to source image brightness and/or randomized, etc.
- **44zaika** - converts every single pixel into 3D object, by default a solid cube. Cubes are packed into square grid. Spheres may be easily replaced by other predefined objects, object positions and properties may be mapped to source image brightness and/or randomized, etc.
- **36zaika** - converts every single pixel into 3D object, by default a triangular prism. Prisms are packed into triangle grid.

![Example of 44zaika export rendering](https://dnyarri.github.io/4z/406.png)

*Dependencies:* Tkinter, [PyPNG](https://gitlab.com/drj11/pypng)

*Usage:* programs are equipped with minimal GUI for file selection. Exported scene contains enough basic stuff (globals, light, camera) to be rendered out of the box, and is well structured and commented for further editing.

[Project website](https://dnyarri.github.io/)

Project mirrors:

[github Dnyarri](https://github.com/Dnyarri/POVmosaic)

[gitflic Dnyarri](https://gitflic.ru/project/dnyarri/povmosaic)
