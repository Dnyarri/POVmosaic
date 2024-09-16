/* 
POVRay include file
Description: Preset file for scene generated with 63zaika.py

    Isosceles trigonal prism, try conic_sweep as well.
    It is isosceles but not equilateral!

https://github.com/Dnyarri/POVmosaic
Read project help.html for options description.
Author: Ilya Razmanov
 {#008800, 0} */

#declare yes_color = 1;

#declare thingie_normal = normal{bumps 0.03 scale<1.0, 0.05, 0.5> rotate z*-30}
#declare normal_rotate_rnd = <0, 0, 10>;

#declare sqrtof3div2 = 0.86602540378443864676372317075294;  // sqrt(3)/2

// Isosceles trigonal prism below, try conic_sweep as well
#declare thingie = prism {linear_sweep linear_spline 0, 1, 4,
    <-1.0, sqrtof3div2>, <1.0, sqrtof3div2>, <0, -sqrtof3div2>, <-1.0, sqrtof3div2>
    rotate x*270 translate<0, 0.5*sqrtof3div2, 0> scale <0.5, 1, 1>}  //  This is isosceles triangle, not equilateral!

#declare evenodd_transform = transform {rotate <0.0, 0.0, 180.0>}   // for 63zaika 1.7.24.15 and above
#declare evenodd_rotate = <0.0, 0.0, 180.0>;    // for compatibility with 3zaika and 63zaika 1.7.22.12