
set term png size 1900,1000 enhanced font "Arial,18"

set grid
set auto x

set yrange [0:5]

set key left top

set title "Stratégie optimale trouvée en fonction de la variation de ".xlabel_." avec l'algorithme UCB1"

set xlabel xlabel_
set ylabel ylabel_

set style data linespoints 
set style fill solid border -1

set boxwidth 0.9

set xtic rotate by -45 scale 0

plot for [COL=2:2] file u COL:xtic(1) title columnheader

