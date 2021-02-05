#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import click

from classes import *
from functions import *

	# program arguments
@click.command()
@click.option("--n-equipement", type=click.INT, required=True, help="Specify equipements number")
@click.option("--n-trames", type=click.INT, required=True, help="Specify trames number")
@click.option("--lambda", "_lambda", type=click.INT, required=True, help="Specify the lambda value")

def main (n_equipement, n_trames, _lambda):

	print(n_equipement, n_trames, _lambda)

	trame = Trame()
	trame.slots[0].append(Packet('a', 'a'))
	trame.slots[1].append(Packet('a', 'a'))
	trame.slots[1].append(Packet('b', 'b'))
	trame.slots[1].append(Packet('c', 'c'))
	trame.slots[2].append(Packet('c', 'c'))

	rewards = trame.rewardIteration()
	print(rewards['a'],end=" ")
	print(HIGH_REWARD)
	print(rewards['c'],end=" ")
	print(HIGH_REWARD)
	print(rewards['b'],end=" ")
	print(MEDIUM_REWARD)

	for i in range(3):
		print(ucb1(n_equipement, n_trames, _lambda))
	return 0	

if __name__ == "__main__":
	main()





# 	trame = Trame()
# 	trame.slots[0].append(Packet('a', 'a'))
# 	trame.slots[1].append(Packet('a', 'a'))
# 	trame.slots[1].append(Packet('b', 'b'))
# 	trame.slots[1].append(Packet('c', 'c'))
# 	trame.slots[2].append(Packet('c', 'c'))

# 	rewards = trame.rewardIteration()
# 	print(rewards['a'],end=" ")
# 	print(HIGH_REWARD)
# 	print(rewards['c'],end=" ")
# 	print(HIGH_REWARD)
# 	print(rewards['b'],end=" ")
# 	print(MEDIUM_REWARD)

# 	for i in range(3):
# 		print(ucb1(n_equipement, n_trame, _lambda))

# # print(ucb1(3, 4, 3.0))
# # print(ucb1(3, 4, 3.0))
# # print(ucb1(3, 4, 3.0))

# # print(ucb1(3, 4, 2.0))
# # print(ucb1(3, 4, 2.0))
# # print(ucb1(3, 4, 2.0))

# # print(ucb1(10, 4, 3.0))
# # print(ucb1(10, 4, 3.0))
# # print(ucb1(10, 4, 3.0))

# # def main (n_equipement, n_trames, _lambda):
# # 	print(n_equipement, n_trames, _lambda)
# # 	global n_equipement
# # 	# global n_equipement = n_equipement
# # 	global n_trames
# # 	global _lambda