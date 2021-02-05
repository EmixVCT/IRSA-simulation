var=""                                  # sets default value
if ("$#" eq sprintf("%d",1)) var="$0"   # if using call with 1 parameter: $#=1
if (exist("bpar")) var=bpar

set term png size 1900,1000 enhanced font "Arial,18"

set grid
set auto x
set auto y

set key left top

set title "Titre du graph"

set xlabel "LABEL X"
set ylabel "LABEL Y"

set style data linespoints 
set style fill solid border -1

set boxwidth 0.9

set xtic rotate by -45 scale 0

plot for [COL=2:2] file.dat u COL:xtic(1) title columnheader

