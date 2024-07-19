/* 
POVRay include file
Description: Preset file for scene generated with 63zaika.py
    Prisms with concave end, gives a bit more testured impession.
https://github.com/Dnyarri/POVmosaic
Read project help.html for options description.
Author: Ilya Razmanov
*/

#declare sqrtof3 = 1.7320508075688772935274463415059;   // sqrt(3)
#declare revsqrtof3 = 1.0/sqrtof3;                      // 1.0/sqrt(3)

#undef map
#declare map = function(c) {1.0-c}

#declare scale_map = <0, 0, 5>;
#declare move_rnd = <0, 0, 0.1>;

#declare thingie = difference {
    prism{linear_sweep linear_spline 0, 1, 7, <-0.5, 0.5*revsqrtof3>, <0,revsqrtof3>, <0.5, 0.5*revsqrtof3>, <0.5,- 0.5*revsqrtof3>, <0,-revsqrtof3>, <-0.5,- 0.5*revsqrtof3>, <-0.5, 0.5*revsqrtof3> rotate x*90}
    sphere {<0, 0, 9>, 9}
}