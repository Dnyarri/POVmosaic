/* 
POVRay include file
Description: Preset file for scene generated with 63zaika.py

    Puzzle elements - hexagonal CSG, extending thingie bounding box,
    but cutting at two corners absolutely the same pin holes as pin extends to a different corner,
    thus making contacting sides and corners match each other.
    Yes, this is HEXAGONAL pattern, therefore at one point 3 corners meet,
    and there must be 2 holes per 1 pin.

https://github.com/Dnyarri/POVmosaic
Read project help.html for options description.
Author: Ilya Razmanov
*/

#declare yes_color = 1;

// Necessary math stuff set as de facto constants to avoid imporing math
#declare sqrtof3 = 1.7320508075688772935274463415059;   // sqrt(3)
#declare revsqrtof3 = 1.0/sqrtof3;                      // 1.0/sqrt(3)

#declare move_map = <0, 0, 0.2>;
#declare move_rnd = <0, 0, 0.1>;

// Thingie CSG construction
#declare pinsize = 0.1;
#declare plus = union {
    cylinder {<-0.5, 0.5*revsqrtof3, 0>, <-0.5, 0.5*revsqrtof3, 1.0>, pinsize}  // 1
    cylinder {<0.5, -0.5*revsqrtof3, 0>, <0.5, -0.5*revsqrtof3, 1.0>, pinsize}  // 4
}   // Beside 1 & 4 combo, 1 & 2 should also work.
#declare minus = union {
    cylinder {<0, revsqrtof3, -1>, <0, revsqrtof3, 2>, pinsize}                 // 2
    cylinder {<0.5, 0.5*revsqrtof3, -1>, <0.5, 0.5*revsqrtof3, 2>, pinsize}     // 3
    cylinder {<0, -revsqrtof3, -1>, <0, -revsqrtof3, 2>, pinsize}               // 5
    cylinder {<-0.5, -0.5*revsqrtof3, -1>, <-0.5, -0.5*revsqrtof3, 2>, pinsize} // 6
}
#declare prizma = prism{linear_sweep linear_spline -1, 0, 7,
 <-0.5, 0.5*revsqrtof3>,
 <0, revsqrtof3>,
 <0.5, 0.5*revsqrtof3>,
 <0.5, -0.5*revsqrtof3>,
 <0, -revsqrtof3>,
 <-0.5, -0.5*revsqrtof3>,
 <-0.5, 0.5*revsqrtof3>
   rotate x*90 translate z}

#declare thingie = difference {
    union {
        object {prizma}
        object {plus}
    }
    object {minus}
scale 0.999}