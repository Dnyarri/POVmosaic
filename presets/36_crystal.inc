/* 
POVRay include file
Description: Preset file for scene generated with 36zaika.py

    Prisms simulating one of non-existing crystals form.

    NOTE: Current .inc version edited for compatibility with
            36zaika ver. 1.19.5.19
        and is incompatible with previous versions!

https://github.com/Dnyarri/POVmosaic
Read project help.html for options description.
Author: Ilya Razmanov
 {#008800, 0} */

#declare yes_color = 1;

background{color rgbft <1, 1, 1, 1, 1>}

#declare sqrtof3 = 1.7320508075688772935274463415059;      // sqrt(3)
#declare sqrtof3div2 = 0.86602540378443864676372317075294; // sqrt(3)/2

#undef f_val
#declare f_val = function(Luma, Alpha) {0.6};

#undef map
#declare map = function(c) {abs((2.0 * c) - 1)}

#declare move_map = <0, 0, 2>;

#declare thingie = merge {
    prism {
    conic_sweep
    linear_spline
    0,
    1,
    4,
    <-1.0, sqrtof3div2>, <1.0, sqrtof3div2>, <0, -sqrtof3div2>, <-1.0, sqrtof3div2>
    scale <1, -1, 1> translate y*1.9999}

    prism {
    linear_sweep
    linear_spline
    0,
    1,
    4,
    <-1.0, sqrtof3div2>, <1.0, sqrtof3div2>, <0, -sqrtof3div2>, <-1.0, sqrtof3div2>
    }
  rotate x*90
}

#if (substr(input_file_name, strlen(input_file_name) - 3, 4) = ".inc")
  camera{
    location <1, 1, 4>
    right x*image_width/image_height
    up y
    sky <0, -1, 0>
    look_at<0.0, 0.0, 0.0>
  }
  light_source{<0, 0, 4>
    color rgb<1.1, 1.0, 1.0>
  }
  object{thingie pigment {color rgb <1, 1, 1>}}
#end