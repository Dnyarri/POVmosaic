/* 
POVRay include file
Description: Preset file for scene generated with 63zaika.py

    Prisms simulating one of quarz crystals form.

https://github.com/Dnyarri/POVmosaic
Read project help.html for options description.
Author: Ilya Razmanov
 {#008800, 0} */

#declare sqrtof3 = 1.7320508075688772935274463415059;   // sqrt(3)
#declare revsqrtof3 = 1.0/sqrtof3;                      // 1.0/sqrt(3)

#declare yes_color = 1;

#declare f_val = 0.6;

background{color rgbft<1, 1, 1, 1, 1>}

#undef map
#declare map = function(c) {abs((2.0 * c) - 1)}

#declare scale_map = <0, 0, 1.5>;

#declare thingie = merge {
    prism{linear_sweep linear_spline 0, 1, 7, <-0.5, 0.5*revsqrtof3>, <0,revsqrtof3>, <0.5, 0.5*revsqrtof3>, <0.5,- 0.5*revsqrtof3>, <0,-revsqrtof3>, <-0.5,- 0.5*revsqrtof3>, <-0.5, 0.5*revsqrtof3> rotate x*90 scale z*3 translate z*-3.9999}
    prism{conic_sweep linear_spline 0, 1, 7, <-0.5, 0.5*revsqrtof3>, <0,revsqrtof3>, <0.5, 0.5*revsqrtof3>, <0.5,- 0.5*revsqrtof3>, <0,-revsqrtof3>, <-0.5,- 0.5*revsqrtof3>, <-0.5, 0.5*revsqrtof3> rotate x*270}
    prism{conic_sweep linear_spline 0, 1, 7, <-0.5, 0.5*revsqrtof3>, <0,revsqrtof3>, <0.5, 0.5*revsqrtof3>, <0.5,- 0.5*revsqrtof3>, <0,-revsqrtof3>, <-0.5,- 0.5*revsqrtof3>, <-0.5, 0.5*revsqrtof3> rotate x*90  translate z*-4.9998}
translate z*4}