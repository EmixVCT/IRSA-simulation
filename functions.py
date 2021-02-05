from collections import defaultdict
import numpy
import math


from classes import *
from constants import *

def get_poisson_distribution(equipment_count, lam):
	#decide avec la loi de poisson combien de packet un equipement envoie
	packets_count = dict()

	for e in range(equipment_count):
		packets_count[e] = numpy.random.poisson(lam)

	return packets_count


def exec_strategie(n, nbEquipement, nbTrames, _lambda):
	packetEnvoyer = defaultdict(bool)
	recompences = list()

	nbPackets = get_poisson_distribution(nbEquipement, _lambda)

	#Pour chaque trame on envoi un packet et on recoit une recompense
	for i in range(nbTrames):
		trame = Trame()

		#Pour chaque equipement on envoie k copie des packets
		for equip in range(nbEquipement):
			if nbPackets[equip] != 0:
				trame.addPacket(Packet(equip, equip), n)
				nbPackets[equip] -= 1
				packetEnvoyer[equip] = True

		recompence = trame.rewardIteration()

		# Ajoute LOW REWARD pour les equipements aillant pas reçu de recompence
		for equip in range(nbEquipement):
			if packetEnvoyer[equip] and equip not in recompence:
				recompence[equip] = LOW_REWARD

		for reward in recompence.values():
			recompences.append(reward)

	if (sum(recompences) == 0):
			return 0
	else:
			return sum(recompences) / len(recompences)
		

def ucb1(nbEquipement, nbTrames, _lambda):
	#Renvoie le nombre de copie qu'un équipement envoie par trame qui MAXIMISE une formule
	
	cycles = 1000
	valeurs = [2, 3, 4]
	cyclesVal = valeurs * cycles
	recompences = defaultdict(list)

	#Execute chaque strategie
	for k in cyclesVal:
		recompences[k].append(exec_strategie(k, nbEquipement, nbTrames, _lambda))
	
	res = dict()
	for k in valeurs:
		res[k] = sum(recompences[k]) / cycles + math.sqrt(2 * (math.log(cycles*3, math.e) / cycles))

	return max(res, key=res.get)


def getvar(varname, n_equipement, n_trames, _lambda):
	var = {
		'ndevices'	: n_equipement,
		'ntrames'	: n_trames,
		'lambda'	: _lambda
	}

	return var.get(varname)