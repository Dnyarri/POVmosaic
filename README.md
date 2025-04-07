# POV-Ray mosaic - Bitmap to 3D solid mosaic converter

Python utilities for conversion of bitmap image (in PNG format) to some sort of solid objects mosaic in [POV-Ray](https://www.povray.org/) format. Each source image pixel is converted to a 3D object, and objects are packed side by side, forming a grid following [Euclidean tilings](https://en.wikipedia.org/wiki/List_of_regular_polytopes#Euclidean_tilings).

[![Example of 63zaika export rendering](https://dnyarri.github.io/3z/301.png)](https://dnyarri.github.io/pov3zaika.html)

## Brief programs description

Current version of POV-Ray Mosaic consist of several parts:

- **POVRayMosaic** - Main program GUI, joining all components together;

- **povzaika** module, including:

  - **zaika63** - converts every single pixel into 3D object, by default a solid sphere. Spheres are packed into triangle/hexagon grid. Spheres may be easily replaced by other predefined objects, object positions and properties may be mapped to source image brightness and/or randomized, etc.
  - **zaika44** - converts every single pixel into 3D object, by default a solid cube. Cubes are packed into square grid. Spheres may be easily replaced by other predefined objects, object positions and properties may be mapped to source image brightness and/or randomized, etc.
  - **zaika36** - converts every single pixel into 3D object, by default a triangular prism. Prisms are packed into triangle grid.

- **pypng** and **pypnm** modules contain components providing PNG and PPM image files reading.

[![Example of 44zaika export rendering](https://dnyarri.github.io/4z/406.png)](https://dnyarri.github.io/pov4zaika.html)

## Dependencies

1. [PyPNG](https://gitlab.com/drj11/pypng). Copy included into current ScaleNx distribution.
2. [PyPNM](https://pypi.org/project/PyPNM/). Copy included into current ScaleNx distribution.
3. Tkinter. Included into standard CPython distribution.

## Usage

Program is equipped with simple GUI for file browsing and selection. Exported scene contains enough basic stuff (globals, light, camera) to be rendered out of the box, and is well structured and commented for further editing. For detail on scene structure and editing refer to help.html included in distribution.

## References

1. [POV-Ray Mosaic](https://dnyarri.github.io/povzaika.html) rendered examples and description.

2. [github POV-Ray Mosaic](https://github.com/Dnyarri/POVmosaic) repository.

3. [gitflic POV-Ray Mosaic](https://gitflic.ru/project/dnyarri/povmosaic) repository mirror.

4. [Dnyarri website](https://dnyarri.github.io/) - other Python programs by Ilyich the Toad.
