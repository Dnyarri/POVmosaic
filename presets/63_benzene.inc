/* 
POVRay include file
Description: Preset file for scene generated with 63zaika.py
    Elements - hexagonal blobs. Lot of room for tweaking parameters.
https://github.com/Dnyarri/POVmosaic
Read project help.html for options description.
Author: Ilya Razmanov
*/

#declare yes_color = 1;

// Necessary math stuff set as de facto constants to avoid imporing math
#declare sqrtof3 = 1.7320508075688772935274463415059;   // sqrt(3)
#declare revsqrtof3 = 1.0/sqrtof3;                      // 1.0/sqrt(3)

#declare move_map = <0, 0, 0.1>;
#declare move_rnd = <0, 0, 0.1>;

// Thingie CSG construction
#declare brad = 0.5;
#declare bstr = 1.0;
#declare net = blob {threshold 0.7
    sphere {<-0.5, 0.5*revsqrtof3, 0>, brad, bstr}    // 1
    sphere {<0, revsqrtof3, 0>, brad, bstr}           // 2
    sphere {<0.5, 0.5*revsqrtof3, 0>, brad, bstr}     // 3
    sphere {<0.5, -0.5*revsqrtof3, 0>, brad, bstr}    // 4
    sphere {<0, -revsqrtof3, 0>, brad, bstr}          // 5
    sphere {<-0.5, -0.5*revsqrtof3, 0>, brad, bstr}   // 6
scale 0.75}

#declare prizma = prism{linear_sweep linear_spline -1, 1, 7,
 <-0.5, 0.5*revsqrtof3>,
 <0,revsqrtof3>,
 <0.5, 0.5*revsqrtof3>,
 <0.5, -0.5*revsqrtof3>,
 <0,-revsqrtof3>,
 <-0.5, -0.5*revsqrtof3>,
 <-0.5, 0.5*revsqrtof3>
   rotate x*90 translate z}

#declare thingie = intersection {
    object {prizma}
    object {net}}