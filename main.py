from random import uniform, shuffle
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
    self.slots = list()
    for i in range(0, SLOTS_COUNT):
      self.slots.append(list())

  def add_packet(self, packet, copies_count):
    """
    Add multiple copies of a packet in the slots of the trame
    @param packet: the packet to add
    @param copies_count: the number of copies to add
    """
    # Check if copies count is not upper than slots count
    if (copies_count <= SLOTS_COUNT):
      for i in range(0, copies_count):          
        slot_index = int(uniform(0, SLOTS_COUNT))
        while (packet in self.slots[slot_index]):
          slot_index = int(uniform(0, SLOTS_COUNT))  # Get randomly a slot index
        self.slots[slot_index].append(packet)
    else:
      print("Too much copies.")

  def __str__(self):
    s = ""
    for i in range(SLOTS_COUNT):
      s += str(i) + " : { "
      for j in self.slots[i].packets:
        s += f"{j} "
      s += "}\n"
    return s


  def self_interference_cancellation(self):
    """
    Removes duplicated packets and deduce rewards
    Check consts.py for rewards values
    """

    equipments_rewards = defaultdict(float)
    first_packets_known = []
    new_slots = list()

    for i in range(0, SLOTS_COUNT):
      new_slots.append(list())

    # Check which packets have high rewards
    # those packets are alone in a slot
    for i in range(SLOTS_COUNT):
      if len(self.slots[i]) == 1:
        packet = self.slots[i][0]
        if packet not in first_packets_known:
          equipments_rewards[packet.packetId] = HIGH_REWARD
          first_packets_known.append(packet)
          new_slots[i].append(packet)

    # delete the packets with high rewards
    for j in range(len(self.slots)):
      for packet in first_packets_known:
        if packet in self.slots[j]:
          self.slots[j].remove(packet)

    i = 0

    # check which packets have medium rewards
    # each time we remove a packet, there's probably another collision
    # that's been removed, thus we restart from 0
    while i != len(self.slots):
      if len(self.slots[i]) == 1:
        packet = self.slots[i][0]
        equipments_rewards[packet.packetId] = MEDIUM_REWARD
        new_slots[i].append(packet)

        for j in range(len(self.slots)):
          if packet in self.slots[j]:
            self.slots[j].remove(packet)
            i = 0
      i += 1

    self.slots = new_slots

    return equipments_rewards


''' Fonctions '''

def get_poisson_distribution(equipment_count: int, lam: float):
  #decide with poisson distribution how many packets an equipment is going to send
  packets_count = dict()

  for e in range(equipment_count):
    packets_count[e] = numpy.random.poisson(lam)

  return packets_count


def play_strategie(n: int, equipment_count: int, frame_count: int, lam: float):
  packet_send = defaultdict(bool)
  all_rewards = list()

  packets_count = get_poisson_distribution(equipment_count, lam)

  # For each trame we'll send packets, and receive rewards
  for f in range(frame_count):
    trame = Trame()

    # For each equipment we send k copies of packets
    for e in range(equipment_count):
      if packets_count[e] != 0:
        trame.add_packet(Packet(e, e), n)
        packets_count[e] -= 1
        packet_send[e] = True

    rewards = trame.self_interference_cancellation()

    # Add the LOW REWARD for the equipments who did not receive their
    # rewards
    for e in range(equipment_count):
      if packet_send[e] and e not in rewards:
        rewards[e] = LOW_REWARD

    for reward in rewards.values():
      all_rewards.append(reward)

  if (sum(all_rewards) == 0):
      return 0
  else:
      return sum(all_rewards) / len(all_rewards)# + math.sqrt(2 * (math.log(n, math.e) / repetitions))


def ucb1(equipment_count: int, frame_count: int, lam: float):
  """
  Returns the strategy which maximises a certain formulae
  """
  repeat = 1000
  values = [2, 3, 4] * repeat
  plays = repeat * 3
  shuffle(values)
  rewards_per_play = defaultdict(list)
  to_maximise = dict()

  # Play each strategy
  for k in values:
    rewards_per_play[k].append(play_strategie(k, equipment_count, frame_count, lam))

  for k in [2, 3, 4]:
    to_maximise[k] = sum(rewards_per_play[k]) / repeat + math.sqrt(2 * (math.log(plays, math.e) / repeat))

  return max(to_maximise, key=to_maximise.get)



''' main '''

'''
#pas besoin de station
id_packet = 'b'
content = "u"
copies_count=3
trame.add_packet(Packet(id_packet, content), copies_count)
'''

trame = Trame()
trame.slots[0].append(Packet('a', 'a'))
trame.slots[1].append(Packet('a', 'a'))
trame.slots[1].append(Packet('b', 'b'))
trame.slots[1].append(Packet('c', 'c'))
trame.slots[2].append(Packet('c', 'c'))

rewards = trame.self_interference_cancellation()
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