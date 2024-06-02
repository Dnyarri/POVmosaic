/* 
POVRay include file
Description: Preset file for scene generated with 4zaika.py
    Dice shapes, stepwise rotated with source brightness
https://github.com/Dnyarri/POVmosaic
Read project help.html for options description.
*/

#include "dice.inc"     // Verify .inc file path for your system
#declare thingie = Cube // Adds non-standard object from external file "dice.inc"
#undef map              // Undef global map from main scene file defore redefining new one
#declare map = function(c) {int(64*c)}  // Stepwise increasing function of c (posterize 64 levels)
#declare rotate_map = <90, 0, 0>;