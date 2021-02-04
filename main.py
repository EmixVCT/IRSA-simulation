# encoding: utf-8

from random import uniform
from collections import defaultdict
import numpy
import math


''' Variables '''

SLOTS_COUNT = 10
HIGH_REWARD = 0.9
MEDIUM_REWARD = 0.4
LOW_REWARD = 0.1


''' Classes '''

class Packet:
  def __init__(self, packetId, content):
    self.packetId = packetId
    self.content = content

  def __str__(self):
    return "packet: "+str(self.packetId)+", Message: "+str(self.content)
  



class Trame:
  """A trame is a set of sloat"""
  def __init__(self):
    self.slots = [[] for i in range(SLOTS_COUNT)]

  def addPacket(self, packet, nCopies):
    """
    Ajout a la trame un packet * nCopies
    Add multiple copies of a packet in the slots of the trame
    """
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
    """
    Calcule la reward pour l'iteration
    """

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


''' Fonctions '''

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




''' main '''

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

print(ucb1(3, 4, 3.0))
print(ucb1(3, 4, 3.0))
print(ucb1(3, 4, 3.0))

print(ucb1(3, 4, 2.0))
print(ucb1(3, 4, 2.0))
print(ucb1(3, 4, 2.0))

print(ucb1(10, 4, 3.0))
print(ucb1(10, 4, 3.0))
print(ucb1(10, 4, 3.0))