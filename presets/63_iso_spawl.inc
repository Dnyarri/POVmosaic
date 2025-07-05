/* 
POVRay include file
Description: Preset file for scene generated with 63zaika.py or 44zaika.py

    Isosurface template - sphere with Perlin noise, resulting in some shapeless clump.

    NOTE: Current .inc version edited for compatibility with
            63zaika ver. 1.19.5.19
        and is incompatible with previous versions!

https://github.com/Dnyarri/POVmosaic
Read project help.html for options description.
Author: Ilya Razmanov.
 {#008800, 0} */

#declare yes_color = 1;

// #undef f_val
// #declare f_val = function(Luma, Alpha) {0.7}; // when enabling, don't forget about max_trace_level

#declare rotate_rnd = <120, 120, 120>;

#include "functions.inc"

#local th_freq = 2.5;   // Sort of noise frequency
#local th_amp = 0.2;    // Noise apmlitude
#local th_rad = 0.4;    // Thingie radius. Note that th_amp and th_rad interfere

#declare thingie = isosurface{function{f_sphere(x, y, z, th_rad) - th_amp*f_noise_generator(th_freq * x,th_freq * y,th_freq * z, 3)}}

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