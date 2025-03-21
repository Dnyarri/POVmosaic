/* 
POVRay include file
Description: Preset file for scene generated with 44zaika.py

    Star (in most cases) prism, looking like that:

    1-2-3
    |   |
    8 9 4
    |   |
    7-6-5

nodes 2 and 6, and 4 and 8 may be offset in pairs by "of26" and "of48" vectors, correspondingly,
and, since they come in pairs, resulting shape still gives seamless pattern.
    
https://github.com/Dnyarri/POVmosaic
Read project help.html for options description.
Author: Ilya Razmanov.
 {#008800, 0} */

#declare yes_color = 1;
#declare evenodd_offset = <0, 0, 0>;

#declare move_rnd = <0, 0, 0.2>;

// All you need is here:    {#880000, 2}
#declare of26 = <-0.3, 0.5>;
#declare of48 = <-0.5, 0.7>;

#declare thingie = prism{linear_sweep linear_spline -1, 0, 9,
 <-1, -1>, <0, -1> + of26, <1, -1>, 
 <1, 0> + of48,
 <1, 1>, <0, 1> + of26, <-1, 1>,
 <-1, 0> + of48,
 <-1, -1>
 scale 0.499 rotate x*90}

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