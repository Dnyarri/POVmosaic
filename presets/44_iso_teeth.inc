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

#if (substr(input_file_name, strlen(input_file_name) - 3, 4) = ".inc")
  camera{
    location <1, 1, 1>
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