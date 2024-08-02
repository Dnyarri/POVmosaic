/* 
POVRay include file
Description: Preset file for scene generated with 44zaika.py
    Cube (box) sheared using matrix. Note this is not 4/4 symmetry anymore!
https://github.com/Dnyarri/POVmosaic
Read project help.html for options description.
Author: Ilya Razmanov
*/

#declare yes_color = 1;

#declare move_rnd = <0, 0, 0.1>;

#declare thingie = box{<-0.5, -0.5, -0.5>, <0.5, 0.5, 0.5>
    matrix <1, 0, 0,
            0.5, 1, 0,
            0, 0, 1,
            0, 0, 0>
  }