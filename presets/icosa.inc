/* 
POVRay include file
Description: Icosahedron triangle mesh
Example object include file for
https://github.com/Dnyarri/POVmosaic
*/

#local b2 = 1 / (1 + sqrt(5));
#declare icosa = mesh{
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