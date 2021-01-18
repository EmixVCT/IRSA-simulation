#include <stdio.h>
#include <stdlib.h>
#include <time.h>

#include "headers/simulation.h"

int main(void) {
	time_t t;
	srand((unsigned) time(&t));

	Simulation simulation;
	initialize(&simulation);
	run(&simulation);
	printResults(&simulation);
}
