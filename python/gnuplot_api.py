#!/usr/bin/env python

from os import popen

class gnuplot_api:
# Author : Leon  Email: yangli0534@gmail.com
# a gnuplot api of python

    def __init__(self):
        self.gnuplot = popen('gnuplot','w')
        self.write = self.gnuplot.write
        self.flush = self.gnuplot.flush
        self.close = self.gnuplot.close
        #return gp

    def set_plot_size(self,x=0.85,y=0.85):
        self.write(''.join(['set  size ',str(x),' ,',str(y),'\n']))
        #self.write(''.join(['set term png size ',str(x),' ',str(y),'\n']))
        #self.flush()

    def set_canvas_size(self,x=600,y=400):
        #self.write('set size 0.85, 0.85\n')
        self.write(''.join(['set term png size ',str(x),' ',str(y),'\n']))


    def set_title(self,title='gnuplot'):
        self.write(''.join(['set title "{/Times:Italic ',str(title), '}"\n']))
        self.write('set title  font ",10"  norotate tc rgb "white"\n')

    def set_gif(self):
        self.write('set terminal gif animate\n')

    def set_png(self):
        self.write('set terminal png\n')
    
    def set_file_name(self,filename='gnuplot.gif'):
        self.write(''.join(['set output ', '"',str(filename) ,'"','\n']))

    def set_tics_color(self,color='orange'):
        self.write(''.join(['set tics textcolor rgb ','"',str(color),'"','\n']))

    def set_border_color(self,color='orange'):
        self.write(''.join(['set border lc rgb ','"',str(color),'"','\n']))

    def set_grid_color(self,color='orange'):
        self.write(''.join(['set grid lc rgb ','"',str(color),'"','\n']))
    
    def set_bkgr_color(self,color='orange'):
        self.write(''.join(['set object 1 rectangle from screen 0,0 to screen 1,1 fc rgb ','"',str(color),'"',' behind\n']))

    def set_xlabel(self,text='x',color='white'):
        self.write(''.join(['set xlabel " {/Times:Italic distance: ', str(text) ,' } " tc rgb ','"',str(color),'"',' \n']))

    def set_ylabel(self,text='x',color='white'):
        self.write(''.join(['set ylabel " {/Times:Italic distance: ', str(text) ,' } " tc rgb ','"',str(color),'"',' \n']))

    def auto_scale_enable(self):
        self.write('set autoscale\n')

    def set_key(self,onoff='off ',text='gnuplot',color='white'):
        self.write('unset key\n')
        self.write(''.join(['set key ',str(onoff),' title "',str(text),'" textcolor rgbcolor "',str(color),'"\n']))
        #self.write('show key\n')

    def set_x_range(self,start,end):
        self.write(''.join(['set xrange [ ',str(start),':',str(end),']\n']))

    def set_y_range(self,start,end):
        self.write(''.join(['set yrange [ ',str(start),':',str(end),']\n']))

    def set_frame_start(self,linestype = 'l',linewidth=3,l_color='green,'):
        #self.write('plot "-" w l  lw 1.5 lc rgb "green"\n')
        self.write(''.join(['plot "-"  notitle w ',str(linestype),' lw ', str(linewidth), ' lc rgb ', '"', str(l_color),'" \n'])) 

    def update_point(self,x,y):
        self.write(''.join([str(x),' ',str(y),'\n']))

    def set_frame_end(self):
        self.write('e\n')

    def set_output_valid(self):
        self.write('set output\n')
    
    def close(self):
        self.close()