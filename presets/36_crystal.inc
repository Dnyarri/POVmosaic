/* 
POVRay include file
Description: Preset file for scene generated with 36zaika.py

    Prisms simulating one of non-existing crystals form.

https://github.com/Dnyarri/POVmosaic
Read project help.html for options description.
Author: Ilya Razmanov
 {#008800, 0} */

#declare yes_color = 1;

#declare sqrtof3 = 1.7320508075688772935274463415059;      // sqrt(3)
#declare sqrtof3div2 = 0.86602540378443864676372317075294; // sqrt(3)/2

#declare f_val = 0.6;

background{color rgbft<1, 1, 1, 1, 1>}

#undef map
#declare map = function(c) {abs((2.0 * c) - 1)}

#declare move_map = <0, 0, 2>;
#declare scale_map = <0, 0, 2>;

#declare thingie = merge {
    prism {
    conic_sweep
    linear_spline
    0,
    1,
    4,
    <-1.0, sqrtof3div2>, <1.0, sqrtof3div2>, <0, -sqrtof3div2>, <-1.0, sqrtof3div2>
    scale <1, -1, 1> translate y*2}

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