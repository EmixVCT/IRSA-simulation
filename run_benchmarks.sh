#!/usr/bin/env bash
source colors.sh

BENCH_ITERATIONS=("ndevices" "ntrames" "lambda")

val_ndevices=(1 2 3 4 5 6 7 8 9 10)
val_ntrames=(1 2 3 4 5 6 7 8 9 10)
val_lambda=(1 2 3 4 5 6 7 8 9 10)

# main 
echo -e "${GREEN} Running full tests ${NOCOLOR}"

for loop in ${BENCH_ITERATIONS[*]}; do

  echo "$loop strategie" > $loop.dat

  for i in $( eval echo \${val_${loop}[*]}); do

    ndevices=${val_ndevices[ $(( ${#val_ndevices[*]} / 2 )) ]}
    ntrames=${val_ntrames[ $(( ${#val_ntrames[*]} / 2 )) ]}
    lambda=${val_lambda[ $(( ${#val_lambda[*]} / 2 )) ]}

    eval "$loop"=$i

    echo -e "  ${YELLOW}$ndevices equipements, $ntrames trames, lambda = $lambda ${NOCOLOR}"

    ./main.py --n-equipement $ndevices --n-trames $ntrames --lambda $lambda --print-variable=$loop >> $loop.dat
  done


  gnuplot -e "file='./$loop.dat' ; xlabel_='$loop' ; ylabel_='nombre de copies de packet optimal par trame (stratégie)" script_plot.gp > $loop.png

done
