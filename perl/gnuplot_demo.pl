# 9月13日 于成都黄龙溪
#!/usr/bin/perl

# Author : Leon  Email: yangli0534@gmail.com
# fdtd simulation , plotting with gnuplot, writting in perl  
# perl and gnuplot software packages should be installed before running this program

#use Time::HiRes qw(sleep);
#use autodie qw(:all);
print "\@\n";
my $terminal = "";
    open GNUPLOT_TERM, "echo 'show terminal;' | gnuplot 2>&1 |";
    while (<GNUPLOT_TERM>) {
    if (m/terminal type is (\w+)/) {
        $terminal=$1;
    }
    }
    close GNUPLOT_TERM;

    # unfortunately, the wxt terminal type does not support positioning. 
    # hardcode it...
    $terminal  = "x11";

open my $PIPE ,"| gnuplot " || die "Can't initialize gnuplot number \n";

print $PIPE "set size 0.85, 0.85\n";
print $PIPE "set term png size 600, 400\n";

my $title = "fdtd simulation by leon,yangli0534\\\\@"."gmail.com";
print $PIPE "set terminal gif animate\n";# terminal type: png
print $PIPE "set output \"fdtd_simulation_v0.1.gif\"\n";#output file name 
print $PIPE  "set title \"{/Times:Italic $title}\"\n";# title name and font
#print $PIPE  "set title  \"fdtd simulation by leon,yangli0534\\\\@ gmail.com\"\n";# title name and font
print $PIPE  "set title  font \",15\"  norotate tc rgb \"white\"\n";
print $PIPE "unset key\n";
print $PIPE "set tics textcolor rgb \"white\"\n";# text color
print $PIPE "set border lc rgb \"orange\"\n";
print $PIPE "set grid lc rgb\"orange\"\n";
print $PIPE "set object 1 rectangle from screen 0,0 to screen 1,1 fc rgb \"gray10\" behind\n";#background color
print $PIPE "set xlabel\" {/Times:Italic distance: wave length}\" tc rgb \"white\" \n";# xlabel
print $PIPE "set ylabel\"{/Times:Italic amplitude: v}\" tc rgb \"white\"\n";#ylabel
print $PIPE "set autoscale\n"; 

my $size = 400;#physical distance
my @ez;#electric field
my @hy;#magnetic field
 
my $imp0 = 377.0;
#initalization
for (my $i = 0; $i < $size; $i++){
    $ez[$i] = 0;
    $hy[$i] = 0;
     
} 
my $qTime;
my $MaxTime = 1850;
my $pi = 3.141592563589793;
print $PIPE "set xrange [0:$size-1]\n";
my $mm = 0;

#do time stepping
for($qTime = 0; $qTime < $MaxTime; $qTime+=5){

    # update magnetic field
    for( $mm = 0; $mm < $size - 1; $mm++){
        $hy[$mm] = $hy[$mm] + ($ez[$mm+1] - $ez[$mm])/$imp0;
    }

    # update electric field
    for( $mm = 1; $mm < $size ; $mm++){
        $ez[$mm] = $ez[$mm] + ($hy[$mm] - $hy[$mm-1])*$imp0;
    }
    
    if($qTime % 10 == 0){

        print $PIPE "plot \"-\" w l  lw 3 lc rgb \"green\"\n";
        my $cnt = 0;
        for my $elem ( @ez) {
        #print " ".$elem;
            print $PIPE $cnt." ".$elem."\n";
            $cnt += 1;
        }
        print $PIPE "e\n";
    } 
    #hardwire a source
    $ez[0] = exp(-($qTime - 30.0)*($qTime - 30.0)/100);
}

#print $PIPE "set terminal x11\n";

print $PIPE "set output\n";

close($PIPE);