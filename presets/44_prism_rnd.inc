/* 
POVRay include file
Description: Preset file for scene generated with 44zaika.py

    8-point prisms, based on square prism, with control points offset by time-dependent random,
    so object changes every time you render the scene, making every rendering truly unique.

https://github.com/Dnyarri/POVmosaic
Read project help.html for options description.
Author: Ilya Razmanov.
 {#008800, 0} */

#local time_rand = seed(int(now*100000)); // Seeding time
#local a = 2.0; // Midpoints offset factor, exceeding 2.0 may lead to shattering
#local b = 2.0; // Corner points offset factor, exceeding 2.0 may lead to shattering

#declare yes_color = 1;
#declare move_rnd = <0, 0, 0.25>;

/*  Prism corner numbering:
1  2  3
8     4
7  6  5   */

#declare off_26 = <a * (rand(time_rand) - 0.5), a * (rand(time_rand) - 0.5)>;
#declare off_48 = <a * (rand(time_rand) - 0.5), a * (rand(time_rand) - 0.5)>;
#declare off_1357 = <b * (rand(time_rand) - 0.5), b * (rand(time_rand) - 0.5)>;

#declare thingie = prism{linear_sweep linear_spline -1, 0, 9,
 <-1, -1> + off_1357, <0, -1> + off_26, <1, -1> + off_1357, 
 <1, 0> + off_48,
 <1, 1> + off_1357, <0, 1> + off_26, <-1, 1> + off_1357,
 <-1, 0> + off_48,
 <-1, -1> + off_1357
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