/* 
POVRay include file
Description: Preset file for scene generated with 44zaika.py

    Dice shapes, stepwise rotated with source brightness

https://github.com/Dnyarri/POVmosaic
Read project help.html for options description.
Author: Ilya Razmanov
 {#008800, 0} */

#declare yes_color = 1;

#undef map  // Undef global map from main scene .pov file before redefining new one below
#declare map = function(c) {int(64*c)}      // Stepwise increasing function of c (posterize 64 levels)
#declare rotate_map = <0, 90, 0>;           // Using 90 deg to switch dice precisely one facet
#declare evenodd_rotate = <90.0, 0.0, 0.0>; // Cheating - even/odd rotation adds variance to mapping
#declare evenodd_offset = <0.5, 0, 0>;      // Unnecessary, added just for fun

// Dice thingie begins
#local Hole = sphere {<0, 0, 0>, 0.2
                    pigment {rgb <0.5, 0.5, 0.5>}  // Hole color independent from main scene, edit it here
}

// CSG intersection, the common space where all the shapes meet
#local Cube = intersection {
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
    }  // end of difference
    box {<-0.5, -0.5, -0.5>, <0.5, 0.5, 0.5>}
}  // end of intersection

#declare thingie = Cube

#if (substr(input_file_name, strlen(input_file_name) - 3, 4) = ".inc")
  camera{
    location <1, 1, 1>
    right x*image_width/image_height
    up y
    sky <0, -1, 0>
    look_at<0.0, 0.0, 0.0>
  }
  light_source{<-2, -3, 4>
    color rgb<1.1, 1.0, 1.0>
  }
  object{thingie pigment {color rgb <1, 1, 1>}}
#end