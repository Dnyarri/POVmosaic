/* 
POVRay include file
Description: Preset file for scene generated with 3zaika.py or 4zaika.py
    Icosahedron shapes, randomply rotated, glass-like
https://github.com/Dnyarri/POVmosaic
Read project help.html for options description.
Authors: preset file made by Ilya Razmanov.
    Icosahedron shape mostly based on example by Paul Bourke,
    edited a bit to improve results.
*/

#declare thingie_finish = thingie_finish_3
#declare f_value = 0.5;
#declare rotate_rnd = <90, 90, 90>;

#local b2 = 1 / (1 + sqrt(5));
#declare thingie = mesh{
  triangle{<0, b2, -0.5>, <b2, 0.5, 0>, <-b2, 0.5, 0>}
  triangle{<0, b2, 0.5>, <-b2, 0.5, 0>, <b2, 0.5, 0>}
  triangle{<0, b2, 0.5>, <0, -b2, 0.5>, <-0.5, 0, b2>}
  triangle{<0, b2, 0.5>, <0.5, 0, b2>, <0, -b2, 0.5>}
  triangle{<0, b2, -0.5>, <0, -b2, -0.5>, <0.5, 0, -b2>}
  triangle{<0, b2, -0.5>, <-0.5, 0, -b2>, <0, -b2, -0.5>}
  triangle{<0, -b2, 0.5>, <b2, -0.5, 0>, <-b2, -0.5, 0>}
  triangle{<0, -b2, -0.5>, <-b2, -0.5, 0>, <b2, -0.5, 0>}
  triangle{<-b2, 0.5, 0>, <-0.5, 0, b2>, <-0.5, 0, -b2>}
  triangle{<-b2, -0.5, 0>, <-0.5, 0, -b2>, <-0.5, 0, b2>}
  triangle{<b2, 0.5, 0>, <0.5, 0, -b2>, <0.5, 0, b2>}
  triangle{<b2, -0.5, 0>, <0.5, 0, b2>, <0.5, 0, -b2>}
  triangle{<0, b2, 0.5>, <-0.5, 0, b2>, <-b2, 0.5, 0>}
  triangle{<0, b2, 0.5>, <b2, 0.5, 0>, <0.5, 0, b2>}
  triangle{<0, b2, -0.5>, <-b2, 0.5, 0>, <-0.5, 0, -b2>}
  triangle{<0, b2, -0.5>, <0.5, 0, -b2>, <b2, 0.5, 0>}
  triangle{<0, -b2, -0.5>, <-0.5, 0, -b2>, <-b2, -0.5, 0>}
  triangle{<0, -b2, -0.5>, <b2, -0.5, 0>, <0.5, 0, -b2>}
  triangle{<0, -b2, 0.5>, <-b2, -0.5, 0>, <-0.5, 0, b2>}
  triangle{<0, -b2, 0.5>, <0.5, 0, b2>, <b2, -0.5, 0>}
rotate <30, 0, 0>}
// rotate <45, 0, 0> for hexagon and <30, 0, 0> for roundish projection appearance