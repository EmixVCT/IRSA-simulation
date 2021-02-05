from collections import defaultdict
from random import uniform

from constants import *


class Packet:
	def __init__(self, packetId, content):
		self.packetId = packetId
		self.content = content

	def __str__(self):
		return "packet: "+str(self.packetId)+", Message: "+str(self.content)
	



class Trame:
	#Un trame est une liste de slots
	def __init__(self):
		self.slots = [[] for i in range(SLOTS_COUNT)]

	def addPacket(self, packet, nCopies):
		#Ajout a la trame un packet * nCopies

		if (nCopies <= SLOTS_COUNT):
			for i in range(0, nCopies):          
				slotID = int(uniform(0, SLOTS_COUNT))
				while (packet in self.slots[slotID]):
					slotID = int(uniform(0, SLOTS_COUNT))  # Get randomly a slot index
				self.slots[slotID].append(packet)
		else:
			print("Err Trame.addPacket : nCopies trop grand")

	def __str__(self):
		s = ""
		for i in range(SLOTS_COUNT):
			s += str(i) + " : { "
			for j in self.slots[i].packets:
				s += f"{j} "
			s += "}\n"
		return s


	def rewardIteration(self):
		#Calcule la recompence pour l'iteration


		equipementRewards = defaultdict(float)
		duplicatas = []
		newSlots = list()

		for i in range(0, SLOTS_COUNT):
			newSlots.append(list())

		# packet unique => HIGHT REWARD
		for i in range(SLOTS_COUNT):
			if len(self.slots[i]) == 1:
				packet = self.slots[i][0]
				if packet not in duplicatas:
					equipementRewards[packet.packetId] = HIGH_REWARD
					self.slots[i].remove(packet)
					newSlots[i].append(packet)

		i = 0

		# On cherche les packets a MEDIUM REWARD
		while i != len(self.slots):
			if len(self.slots[i]) == 1:
				packet = self.slots[i][0]
				equipementRewards[packet.packetId] = MEDIUM_REWARD
				newSlots[i].append(packet)

				for j in range(len(self.slots)):
					if packet in self.slots[j]:
						self.slots[j].remove(packet)
						# en supprimant un packet on peut creer des conflits
						# => on recommence à 0
						i = 0
			i += 1

		self.slots = newSlots

		return equipementRewards