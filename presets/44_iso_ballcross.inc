/* 
POVRay include file
Description: Preset file for scene generated with 44zaika.py
    
    Isosurface template.
    
https://github.com/Dnyarri/POVmosaic
Read project help.html for options description.
Authors: preset file made by Ilya Razmanov.
*/

#declare yes_color = 1;

#declare rotate_rnd = <90, 90, 90>;

#include "functions.inc"

#declare thingie = isosurface{function{f_cross_ellipsoids(x, y, z, 0.3, 1, 1.5, 1.35)}}