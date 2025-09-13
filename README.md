# POV-Ray Mosaic - Bitmap to 3D solid mosaic converter

Python utilities for conversion of bitmap image (in PNG or PPM format) to some sort of solid objects mosaic in [POV-Ray](https://www.povray.org/) format. Each source image pixel is converted to a 3D object, and objects are packed side by side, forming a grid following [Euclidean tilings](https://en.wikipedia.org/wiki/List_of_regular_polytopes#Euclidean_tilings).

[![Example of 63zaika export rendering](https://dnyarri.github.io/3z/301.png "Example of 6/3 POV-Ray Mosaic export rendering")](https://dnyarri.github.io/pov3zaika.html)

## Brief programs description

Current version of POV-Ray Mosaic consist of several parts:

- [**POVRayMosaic.py**](https://github.com/Dnyarri/POVmosaic/blob/main/POVRayMosaic.py) - Main program GUI, joining all components together;

- **povzaika** module, including:

  - [**zaika63.py**](https://github.com/Dnyarri/POVmosaic/blob/main/export/zaika63.py) - converts every single pixel into 3D object, by default a solid sphere. Spheres are packed into triangle/hexagon grid. Spheres may be easily replaced by other predefined objects, object positions and properties may be mapped to source image brightness and/or randomized, etc.
  - [**zaika44.py**](https://github.com/Dnyarri/POVmosaic/blob/main/export/zaika44.py) - converts every single pixel into 3D object, by default an isosurface looking like cube with rounded corners (well, it would be logical to use cube by default but cubes are flat and boring). Cubes are packed into square grid. Cubes may be easily replaced by other predefined objects, object positions and properties may be mapped to source image brightness and/or randomized, etc.
  - [**zaika36.py**](https://github.com/Dnyarri/POVmosaic/blob/main/export/zaika36.py) - converts every single pixel into 3D object, by default a triangular prism. Prisms are packed into triangle grid.

- **pypng** and **pypnm** modules contain components providing PNG and PPM image files reading, correspondingly.

[![Example of 44zaika export rendering](https://dnyarri.github.io/4z/406.png "Example of 4/4 POV-Ray Mosaic export rendering")](https://dnyarri.github.io/pov4zaika.html)

## Prerequisite and Dependencies

1. [Python](https://www.python.org/) 3.11 or above.
2. [PyPNG](https://gitlab.com/drj11/pypng). Copy included into current POV-Ray Mosaic distribution.
3. [PyPNM](https://pypi.org/project/PyPNM/). Copy included into current POV-Ray Mosaic distribution.
4. Tkinter. Normally included into standard CPython distribution.

> [!NOTE]
> Since POVRayMosaic 1.21.2.2 PyPNM version included into distribution updated to [PyPNM "Victory 2" main](https://github.com/Dnyarri/PyPNM), intended to be used with Python 3.11 and above. The only actual limitation is that main version does not have a workaround for displaying 16 bpc images necessary for old Tkinter included into old CPython distributions. If you want bringing old Tkinter compatibility back, download [PyPNM extended compatibility version](https://github.com/Dnyarri/PyPNM/tree/py34) and plug it in manually.

## Usage

Program is equipped with simple GUI for file browsing and selection. Exported scene contains enough basic stuff (globals, light, camera) to be rendered out of the box, and is well structured and commented for further editing. For detail on scene structure and editing refer to *help.html* included in current distribution.

### Related

[Dnyarri website - other Python freeware](https://dnyarri.github.io) by the same author.

[POV‑Ray Mosaic page with illustrations](https://dnyarri.github.io/povzaika.html), explanations etc.

[POV‑Ray Mosaic source at github](https://github.com/Dnyarri/POVmosaic)

[POV‑Ray Mosaic source at gitflic mirror](https://gitflic.ru/project/dnyarri/povmosaic)
