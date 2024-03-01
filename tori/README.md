**(EN)** [(RU)](README.RU.md)

# Bitmap to textile simulation converters

Python utilities for conversion of bitmap image (in [PNG format](http://www.libpng.org/pub/png/)) to some sort of complex scene in [POVRay](https://www.povray.org/) format.

*Brief program description*

- **linen.py** - reads source PNG file and convert it into POVRay scene, simulating canvas of linen or tabby weave type (gros de Naples), having nodes colored after source image pixels, looking like print on canvas.  

- **stitch.py** - reads source PNG file and convert it into POVRay scene, simulating counted cross stitch, with each stitch 3D object colored after source image pixel.  

Thread normal texture is somewhat randomized on per-stitch basis to make embroidery rendering more realistic.

![Example of stitch export rendering](https://dnyarri.github.io/imgzaika/640/stitch.png)

*Dependencies:* Tkinter, PyPNG

*Usage:* programs are equipped with minimal GUI, so all you have to do after starting the programs is use standard "Open..." GUI to open image file, then use standard "Save..." GUI to set POVRay scene file to be created, then wait while program does the job, then open resulting POV file with POVRay and render the scene. Scene contains enough basic stuff (globals, light, camera) to be rendered successfully right after exporting without any editing.

![Example of linen export rendering](https://dnyarri.github.io/imgzaika/640/linen.png)

[Project website](https://dnyarri.github.io/)

Project mirrors:

[github Dnyarri](https://github.com/Dnyarri/POVmosaic)

[gitflic Dnyarri](https://gitflic.ru/project/dnyarri/povmosaic)
