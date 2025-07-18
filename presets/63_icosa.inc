/* 
POVRay include file
Description: Preset file for scene generated with 63zaika.py or 44zaika.py

    Icosahedron shapes, randomly rotated, glass-like.

    NOTE: Current .inc version edited for compatibility with
            63zaika ver. 1.19.5.19
        and is incompatible with previous versions!

https://github.com/Dnyarri/POVmosaic
Read project help.html for options description.
Authors: preset file made by Ilya Razmanov.
    Icosahedron shape mostly based on example by Paul Bourke,
    edited a bit to improve a bit. A bit improved successfully.
 {#008800, 0} */

#declare yes_color = 1;

// #undef f_val
// #declare f_val = function(Luma, Alpha) {0.5};     // when enabling, don't forget about max_trace_level

#declare thingie_finish = finish{ambient 0.1 diffuse 0.5 specular 0.9
    roughness 0.03 metallic 1.0 reflection {0.9 metallic 0.0}}

#declare rotate_rnd = <120, 120, 120>;

#local b2 = 1 / (1 + sqrt(5));
#declare thingie = mesh{
  triangle{<0, b2, -0.5>, <b2, 0.5, 0>, <-b2, 0.5, 0>}
  triangle{<0, b2, 0.5>, <-b2, 0.5, 0>, <b2, 0.5, 0>}
  triangle{<0, b2, 0.5>, <0, -b2, 0.5>, <-0.5, 0, b2>}
  triangle{<0, b2, 0.5>, <0.5, 0, b2>, <0, -b2, 0.5>}
  triangle{<0, b2, -0.5>, <0, -b2, -0.5>, <0.5, 0, -b2>}
  triangle{<0, b2, -0.5>, <-0.5, 0, -b2>, <0, -b2, -0.5>}
  triangle{<0, -b2, 0.5>, <b2, -0.5, 0>, <-b2, -0.5, 0>}
  triangle{<0, -b2, -0.5>, <-b2, -0.5, 0>, <b2, -0.5, 0>}
  triangle{<-b2, 0.5, 0>, <-0.5, 0, b2>, <-0.5, 0, -b2>}
  triangle{<-b2, -0.5, 0>, <-0.5, 0, -b2>, <-0.5, 0, b2>}
  triangle{<b2, 0.5, 0>, <0.5, 0, -b2>, <0.5, 0, b2>}
  triangle{<b2, -0.5, 0>, <0.5, 0, b2>, <0.5, 0, -b2>}
  triangle{<0, b2, 0.5>, <-0.5, 0, b2>, <-b2, 0.5, 0>}
  triangle{<0, b2, 0.5>, <b2, 0.5, 0>, <0.5, 0, b2>}
  triangle{<0, b2, -0.5>, <-b2, 0.5, 0>, <-0.5, 0, -b2>}
  triangle{<0, b2, -0.5>, <0.5, 0, -b2>, <b2, 0.5, 0>}
  triangle{<0, -b2, -0.5>, <-0.5, 0, -b2>, <-b2, -0.5, 0>}
  triangle{<0, -b2, -0.5>, <b2, -0.5, 0>, <0.5, 0, -b2>}
  triangle{<0, -b2, 0.5>, <-b2, -0.5, 0>, <-0.5, 0, b2>}
  triangle{<0, -b2, 0.5>, <0.5, 0, b2>, <b2, -0.5, 0>}
rotate <30, 0, 0>}
// rotate <45, 0, 0> for hexagon and <30, 0, 0> for roundish projection appearance

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