/* 
POVRay include file
Description: Preset file for scene generated with 36zaika.py
    Prisms with concave end, gives a bit more testured impession.
https://github.com/Dnyarri/POVmosaic
Read project help.html for options description.
Author: Ilya Razmanov
*/

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