/* 
POVRay include file
Description: Preset file for scene generated with 44zaika.py
    
    Isosurface template "В тазу лежат четыре зуба"
    
https://github.com/Dnyarri/POVmosaic
Read project help.html for options description.
Authors: preset file made by Ilya Razmanov,
    based on "Isosurface Tutorial" by Mike Williams 
    https://povlab.online/isotutorial/
 {#008800, 0} */

#declare yes_color = 1;

#declare rotate_map = <360, 360, 360>;

#include "functions.inc"

#declare thingie = isosurface{function{f_pillow(x,y,z,1)} max_gradient 8 contained_by {box {<-1.5,-1.5,-1.5>, <1.5, 1.5, 1.5>}} scale 0.4}