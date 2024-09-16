/* 
POVRay include file
Description: Preset file for scene generated with 44zaika.py

    Star (in most cases) prism, looking like that:
    
    1-2-3
    |   |
    8 9 4
    |   |
    7-6-5

nodes 2 and 6, and 4 and 8 may be offset in pairs by "of26" and "of48" vectors, correspondingly,
and, since they come in pairs, resulting shape still gives seamless pattern.
    
https://github.com/Dnyarri/POVmosaic
Read project help.html for options description.
Authors: preset file made by Ilya Razmanov.
 {#008800, 0} */

#local timerand = seed(int(now*10000));

#declare yes_color = 1;
#declare move_rnd = <0, 0, 0.2>;

#declare of26 = <rand(timerand)-0.5, rand(timerand)-0.5>;
#declare of48 = <rand(timerand)-0.5, rand(timerand)-0.5>;

#declare thingie = prism{linear_sweep linear_spline -1, 0, 9,
 <-1, -1>, <0, -1>+of26, <1, -1>, 
 <1, 0>+of48,
 <1, 1>, <0, 1>+of26, <-1, 1>,
 <-1, 0>+of48,
 <-1, -1>
 scale 0.49 rotate x*90}
