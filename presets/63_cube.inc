/* 
POVRay include file
Description: Preset file for scene generated with 63zaika.py

    Rotated cubes that, from vertical view point, look like hexagones.

https://github.com/Dnyarri/POVmosaic
Read project help.html for options description.
Author: Ilya Razmanov
 {#008800, 0} */

#declare yes_color = 1;

#declare thingie = box{<-0.5, -0.5, -0.5>, <0.5, 0.5, 0.5>
    rotate <45, 45, 0> scale 0.86
  }

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