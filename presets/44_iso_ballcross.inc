/* 
POVRay include file
Description: Preset file for scene generated with 44zaika.py
    
    Isosurface template.
    
https://github.com/Dnyarri/POVmosaic
Read project help.html for options description.
Authors: preset file made by Ilya Razmanov,
    based on "Isosurface Tutorial" by Mike Williams 
    https://povlab.online/isotutorial/
 {#008800, 0} */

#declare yes_color = 1;

#declare rotate_rnd = <90, 90, 90>;

#include "functions.inc"

#declare thingie = isosurface{function{f_cross_ellipsoids(x, y, z, 0.3, 1, 1.5, 1.35)}}

#if (substr(input_file_name, strlen(input_file_name) - 3, 4) = ".inc")
  camera{
    location <0, 0, 2>
    right x*image_width/image_height
    up y
    sky <0, -1, 0>
    look_at<0.0, 0.0, 0.0>
  }
  light_source{<-2, -3, 4>
    color rgb<1.1, 1.0, 1.0>
  }
  object{thingie pigment {color rgb <1, 1, 1>}}
#end