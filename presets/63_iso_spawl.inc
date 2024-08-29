/* 
POVRay include file
Description: Preset file for scene generated with 63zaika.py or 44zaika.py

    Isosurface template - sphere with Perlin noise, resulting in some shapeless clump.

https://github.com/Dnyarri/POVmosaic
Read project help.html for options description.
Authors: preset file made by Ilya Razmanov.
*/

#declare yes_color = 1;

// #declare f_val = 0.5;     // when enabling, don't forget about max_trace_level

#declare rotate_rnd = <120, 120, 120>;

#include "functions.inc"

#local th_freq = 2.5;   // Sort of noise frequency
#local th_amp = 0.2;    // Noise apmlitude
#local th_rad = 0.4;    // Thingie radius. Note that th_amp and th_rad interfere

#declare thingie = isosurface{function{f_sphere(x, y, z, th_rad) - th_amp*f_noise_generator(th_freq * x,th_freq * y,th_freq * z, 3)}}