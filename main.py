#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import click

from classes import *
from functions import *

	# program arguments
@click.command()
@click.option("--n-equipement", type=click.INT, required=True, help="Specify number, equipements")
@click.option("--n-trames", type=click.INT, required=True, help="Specify number of trames")
@click.option("--lambda", "_lambda", type=click.INT, required=True, help="Specify the lambda value")
@click.option("--print-variable", type=click.STRING, help="Print the value of a variable as well")

def main (n_equipement, n_trames, _lambda, print_variable):

	trame = Trame()
	trame.slots[0].append(Packet('a', 'a'))
	trame.slots[1].append(Packet('a', 'a'))
	trame.slots[1].append(Packet('b', 'b'))
	trame.slots[1].append(Packet('c', 'c'))
	trame.slots[2].append(Packet('c', 'c'))

	rewards = trame.rewardIteration()

	for i in range(3):
		if (print_variable):
			print(getvar(print_variable, n_equipement, n_trames, _lambda), ucb1(n_equipement, n_trames, _lambda))
		else:
			print(ucb1(n_equipement, n_trames, _lambda))
	return 0	

if __name__ == "__main__":
	main()