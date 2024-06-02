/* 
POVRay include file
Description: Dice CSG. Color of "point" spheres predefined as grey
Example object include file for 4zaika.py
https://github.com/Dnyarri/POVmosaic
Author: Ilya Razmanov
*/


#declare Hole = sphere { <0, 0, 0>, 0.2
                    pigment {rgb <0.5, 0.5, 0.5>}
				}

// CSG intersection, the common space where all the shapes meet
#declare Cube = intersection {
            difference {
                superellipsoid{<0.3, 0.3>}
                // One
                object {Hole translate -1*x}
                // Six
                object {Hole translate 1*x translate <0, 0.5, 0.5>}
                object {Hole translate 1*x translate <0, 0, 0.5>}
                object {Hole translate 1*x translate <0, -0.5, 0.5>}
                object {Hole translate 1*x translate <0, 0.5, -0.5>}
                object {Hole translate 1*x translate <0, 0, -0.5>}
                object {Hole translate 1*x translate <0, -0.5, -0.5>}
                // Four
                object {Hole translate 1*y translate <-0.5, 0, 0.5>}
                object {Hole translate 1*y translate <0.5, 0, -0.5>}
                object {Hole translate 1*y translate <-0.5, 0, -0.5>}
                object {Hole translate 1*y translate <0.5, 0, 0.5>}
                // Two
                object {Hole translate -1*y translate <0.5, 0, 0.5>}
                object {Hole translate -1*y translate <-0.5, 0, -0.5>}
                // Three
                object {Hole translate -1*z translate <-0.5, -0.5, 0>}
                object {Hole translate -1*z translate <0.5, 0.5, 0>}
                object {Hole translate -1*z}
                // Five
                object {Hole translate 1*z}
                object {Hole translate 1*z translate <0.5, 0.5, 0>}
                object {Hole translate 1*z translate <-0.5, -0.5, 0>}
                object {Hole translate 1*z translate <0.5, -0.5, 0>}
                object {Hole translate 1*z translate <-0.5, 0.5, 0>}
            scale 0.508  // Slightly larger than bounding cube to be cut off flat
		   }
            box {<-0.5, -0.5, -0.5>, <0.5, 0.5, 0.5>}
        } // end of intersection