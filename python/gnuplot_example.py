#!/usr/bin/env python

import sys
import math
import os
from gnuplot_api import *

# Author : Leon  Email: yangli0534@gmail.com
# fdtd simulation , plotting with gnuplot, writting in python  
# perl and gnuplot software packages should be installed before running this program
# 1d fdtd with absorbing boundary and TFSF boundary between [49] and [50]
# lossy dielectric material localted at > ez[150]

gp = gnuplot_api()

gp.set_plot_size(1,1)
gp.set_canvas_size(600,800)
gp.set_title('fdtd simulation by leon : gnuplot class test')
title = 'gnuplot example by leon,yangli0534\\\\@gmail.com'
#gp.write('set terminal gif animate\n')
gp.set_title(title)
#gp.set_gif()
gp.set_png()
gp.set_file_name('gnuplot_example.png')
gp.set_tics_color('white')
gp.set_border_color('orange')
gp.set_grid_color('orange')
gp.set_bkgr_color('gray10')
gp.set_xlabel('length','white')
gp.set_ylabel('amplitude','white')
gp.auto_scale_enable()
gp.set_key('off','sin(x)','white')

size = 400#physical distance

sinwave=size * [0.00]# 

cnt = 0
elem = 0.00000
pi = 3.14159265358979323846
#gp.write(''.join(['set xrange [0:',str(size),'-1]\n']));
gp.set_x_range(0,size-1)
#for i in range(0,size):
#    sinwave[i] = 0.0
    

for mm in range(0, size-1):    
    sinwave[mm] = math.sin(2*pi*mm/size)
    
gp.set_frame_start('l', 3, 'green')
cnt = 0    
for elem in sinwave:
    gp.update_point(cnt,elem)
    #print ''.join([str(cnt),':',str(elem),'\n'])            
    cnt +=  1        
gp.set_frame_end()    
gp.set_key('off','sin(x)','white')
gp.set_output_valid()
gp.close()
