/* 
POVRay include file
Description: Preset file for scene generated with 63zaika.py

    Key elements - hexagonal blobs. Lot of room for tweaking parameters.

https://github.com/Dnyarri/POVmosaic
Read project help.html for options description.
Author: Ilya Razmanov
 {#008800, 0} */

#declare yes_color = 1;

// Necessary math stuff set as de facto constants to avoid imporing math
#declare sqrtof3 = 1.7320508075688772935274463415059;   // sqrt(3)
#declare revsqrtof3 = 1.0/sqrtof3;                      // 1.0/sqrt(3)

#declare move_map = <0, 0, 0.7>;
#declare move_rnd = <0, 0, 0.3>;

// Thingie CSG construction
#declare bradius = 0.75;
#declare bstrength = 0.75;
#declare net = blob {threshold 0.9
    sphere {<-0.5, 0.5*revsqrtof3, 0>, bradius, bstrength}    // 1
    sphere {<0, revsqrtof3, 0>, bradius, bstrength}           // 2
    sphere {<0.5, 0.5*revsqrtof3, 0>, bradius, bstrength}     // 3
    sphere {<0.5, -0.5*revsqrtof3, 0>, bradius, bstrength}    // 4
    sphere {<0, -revsqrtof3, 0>, bradius, bstrength}          // 5
    sphere {<-0.5, -0.5*revsqrtof3, 0>, bradius, bstrength}   // 6
  }

#declare prizma = prism{linear_sweep linear_spline -0.5, 0.5, 7,
    <-0.5, 0.5*revsqrtof3>,
    <0, revsqrtof3>,
    <0.5, 0.5*revsqrtof3>,
    <0.5, -0.5*revsqrtof3>,
    <0, -revsqrtof3>,
    <-0.5, -0.5*revsqrtof3>,
    <-0.5, 0.5*revsqrtof3>
  rotate x*90 translate z}

#declare thingie = union {
    difference {
      object {prizma}
      object {net scale <0.65, 0.65, 0.3> translate z*1.5}
    }
    object {net scale <0.5, 0.5, 0.2> translate z*1.6}
  }