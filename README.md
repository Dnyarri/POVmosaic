# POV-Ray Mosaic - Bitmap to 3D solid mosaic converter

Python utilities for conversion of bitmap image (in PNG or PPM format) to some sort of solid objects mosaic in [POV-Ray](https://www.povray.org/ "Persistence of Vision Raytracer") format. Each source image pixel is converted to a 3D object, and objects are packed side by side, forming a grid following [Euclidean tilings](https://en.wikipedia.org/wiki/List_of_regular_polytopes#Euclidean_tilings "Brief Euclidean tilings explanation").

[![Example of 63zaika export rendering](https://dnyarri.github.io/3z/301.png "Example of 6/3 POV-Ray Mosaic export rendering")](https://dnyarri.github.io/pov3zaika.html)

## Brief programs description

Current version of POV-Ray Mosaic consist of several parts:

- [**POVRayMosaic.py**](https://github.com/Dnyarri/POVmosaic/blob/main/POVRayMosaic.py) - Main program GUI, joining all components together;

- **povzaika** export module, including:

  - [**zaika63.py**](https://github.com/Dnyarri/POVmosaic/blob/main/export/zaika63.py) - converts every single pixel into 3D object, by default a solid sphere. Spheres are packed into triangle/hexagon grid. Spheres may be easily replaced by other predefined objects, object positions and properties may be mapped to source image brightness and/or randomized, etc.
  - [**zaika44.py**](https://github.com/Dnyarri/POVmosaic/blob/main/export/zaika44.py) - converts every single pixel into 3D object, by default an isosurface looking like cube with rounded corners (well, it would be logical to use cube by default but cubes are flat and boring). Cubes are packed into square grid. Cubes may be easily replaced by other predefined objects, object positions and properties may be mapped to source image brightness and/or randomized, etc.
  - [**zaika36.py**](https://github.com/Dnyarri/POVmosaic/blob/main/export/zaika36.py) - converts every single pixel into 3D object, by default a triangular prism. Prisms are packed into triangle grid.

- **pypng** and **pypnm** folders comprise:

  - [PyPNM module, providing image data preview, as well as PPM ang PGM files support](https://dnyarri.github.io/pypnm.html "Pure Python PNM image support module");

  - [PyPNG module, providing PNG files support](https://gitlab.com/drj11/pypng "Pure Python PNG format module").

[![Example of 44zaika export rendering](https://dnyarri.github.io/4z/406.png "Example of 4/4 POV-Ray Mosaic export rendering")](https://dnyarri.github.io/pov4zaika.html)

## Prerequisite and Dependencies

1. [Python](https://www.python.org/ "CPython") 3.11 or above.
2. [PyPNG](https://gitlab.com/drj11/pypng "PyPNG module for reading and writing PNG image files"). Copy included into current POV-Ray Mosaic distribution.
3. [PyPNM](https://pypi.org/project/PyPNM/ "PyPNM module for displaying pictures and reading and writing PNM image files"). Copy included into current POV-Ray Mosaic distribution.
4. Tkinter. Normally included into standard CPython distribution.

## Usage

Program is equipped with simple GUI for file browsing and selection. Exported scene contains enough basic stuff (globals, light, camera) to be rendered out of the box, and is well structured and commented for further editing. For detail on scene structure and editing refer to *help.html* included in current distribution.

### Related

[Dnyarri website - more Python freeware for image processing, 3D, and batch automation](https://dnyarri.github.io "The Toad's Slimy Mudhole - Python freeware for POV-Ray and other 3D, Scale2x, Scale3x, Scale2xSFX, Scale3xSFX, PPM and PGM image support, bilinear and barycentric image interpolation, and batch processing") by the same author.

[POV‑Ray Mosaic general information](https://dnyarri.github.io/povzaika.html "POV‑Ray Mosaic general and updates info"), explanations etc.;

- [POV-Ray Mosaic 6³ examples](https://dnyarri.github.io/pov3zaika.html "POV-Ray Mosaic 6³ renderings and scene options explanation")
- [POV-Ray Mosaic 4⁴ examples](https://dnyarri.github.io/pov4zaika.html "POV-Ray Mosaic 4⁴ renderings and scene options explanation")
- [POV-Ray Mosaic 3⁶ examples](https://dnyarri.github.io/pov36zaika.html "POV-Ray Mosaic 3⁶ renderings and scene options explanation")

[POV‑Ray Mosaic source at Github](https://github.com/Dnyarri/POVmosaic "POV‑Ray Mosaic source at Github")

[POV‑Ray Mosaic source at Gitflic mirror](https://gitflic.ru/project/dnyarri/povmosaic "POV‑Ray Mosaic source at Gitflic mirror")
