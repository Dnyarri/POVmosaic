/* 
POVRay include file
Description: Preset file for scene generated with 44zaika.py
    Puzzle elements - CSG, extending thingie bounding box,
    but cutting at one side absolutely the same pin hole as pin extends to the other side,
    thus making contacting sides match each other.
https://github.com/Dnyarri/POVmosaic
Read project help.html for options description.
Author: Ilya Razmanov
*/

#declare yes_color = 1;

#declare move_rnd = <0, 0, 0.25>;

#declare pin_rad = 0.2;
#declare pin_off = 0.1;

#declare thingie = difference {
    union {
        box{
            <-0.5, -0.5, -0.5>, <0.5, 0.5, 0.5>
        }
        cylinder {
            <-0.5-pin_off, 0, -0.5>, <-0.5-pin_off, 0, 0.5>, pin_rad
        }
        cylinder {
            <0, -0.5-pin_off, -0.5>, <0, -0.5-pin_off, 0.5>, pin_rad
        }
    }
    union {
        cylinder {
            <0.5-pin_off, 0, -1>, <0.5-pin_off, 0, 1>, pin_rad
        }
        cylinder {
            <0, 0.5-pin_off, -1>, <0, 0.5-pin_off, 1>, pin_rad
        }
    }
  scale 0.99
}