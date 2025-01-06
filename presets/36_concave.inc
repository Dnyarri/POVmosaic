/* 
POVRay include file
Description: Preset file for scene generated with 36zaika.py

    Prisms with concave end, gives a bit more testured impession.

https://github.com/Dnyarri/POVmosaic
Read project help.html for options description.
Author: Ilya Razmanov
 {#008800, 0} */

#declare yes_color = 1;

#declare sqrtof3 = 1.7320508075688772935274463415059;      // sqrt(3)
#declare sqrtof3div2 = 0.86602540378443864676372317075294; // sqrt(3)/2

// #declare move_rnd = <0, 0, 0.2>;

#declare thingie = difference {
    prism {
    linear_sweep
    linear_spline
    0,
    1,
    4,
    <-1.0, sqrtof3div2>, <1.0, sqrtof3div2>, <0, -sqrtof3div2>, <-1.0, sqrtof3div2>
    rotate x*90 scale z*1 translate z*-1}
    sphere {<0, 0, 6>, 7}
}

#if (substr(input_file_name, strlen(input_file_name) - 3, 4) = ".inc")
  camera{
    location <0, 0, 1>
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