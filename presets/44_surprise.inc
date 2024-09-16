/* 
POVRay include file
Description: Preset file for scene generated with 44zaika.py

    Press Alt+R two-three times to make a conclusion regarding scene appearance.
    
https://github.com/Dnyarri/POVmosaic
Read project help.html for options description.
Author: Ilya Razmanov.
 {#008800, 0} */

#local timerand = seed(int(now*100000));

#declare yes_color = 1;
#declare move_rnd = <0, 0, 0.2>;

// Critical part:                                   {#880000, 2}
#declare of26 = <rand(timerand) - 0.5, rand(timerand) - 0.5>;
#declare of48 = <rand(timerand) - 0.5, rand(timerand) - 0.5>;

#declare thingie = prism{linear_sweep linear_spline -1, 0, 9,
 <-1, -1>, <0, -1> + of26, <1, -1>, 
 <1, 0> + of48,
 <1, 1>, <0, 1> + of26, <-1, 1>,
 <-1, 0> + of48,
 <-1, -1>
 scale 0.499 rotate x*90}
