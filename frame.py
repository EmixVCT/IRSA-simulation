from src.consts import *
from src.slot import Slot
from src.packet import Packet
from random import uniform, shuffle
from collections import defaultdict
import numpy as np
import math

class Frame:
  """A frame is a set of sloat"""
  def __init__(self):
    self.slots = list()
    for i in range(0, SLOTS_COUNT):
      self.slots.append(Slot())

  def add_packet(self, packet, copies_count):
    """
    Add multiple copies of a packet in the slots of the frame
    @param packet: the packet to add
    @param copies_count: the number of copies to add
    """
    # Check if copies count is not upper than slots count
    if (copies_count <= SLOTS_COUNT):
      for i in range(0, copies_count):
        while 1:
          # Get randomly a slot index
          slot_index = int(uniform(0, SLOTS_COUNT))
          # Check that the packet isn't already in the selected slot
          if (not self.slots[slot_index].contains_packet(packet)):
            self.slots[slot_index].add_packet(packet)
            break
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

  @staticmethod
  def poisson_process(equipment_count: int, lam: float) -> dict:
    # decide with poisson distribution how many packets an equipment is going
    # to send
    packets_count = dict()

    for e in range(equipment_count):
      packets_count[e] = np.random.poisson(lam)

    return packets_count

  @staticmethod
  def play_machine(n: int, equipment_count: int, frame_count: int, lam: float):
    packet_send = defaultdict(bool)
    all_rewards = list()

    #repetitions = 4

    #for r in range(repetitions):
    packets_count = Frame.poisson_process(equipment_count, lam)

    # For each frame we'll send packets, and receive rewards
    for f in range(frame_count):
      frame = Frame()

      # For each equipment we send k copies of packets
      for e in range(equipment_count):
        if packets_count[e] != 0:
          frame.add_packet(Packet(e, e), n)
          packets_count[e] -= 1
          packet_send[e] = True

      rewards = frame.self_interference_cancellation()

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

  @staticmethod
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
      rewards_per_play[k].append(Frame.play_machine(k, equipment_count, frame_count, lam))

    for k in [2, 3, 4]:
      to_maximise[k] = sum(rewards_per_play[k]) / repeat + math.sqrt(2 * (math.log(plays, math.e) / repeat))

    return max(to_maximise, key=to_maximise.get)



  def self_interference_cancellation(self) -> dict:
    """
    Removes duplicated packets and deduce rewards
    Check consts.py for rewards values
    """

    equipments_rewards = defaultdict(float)
    first_packets_known = []
    new_slots = list()

    for i in range(0, SLOTS_COUNT):
      new_slots.append(Slot())

    # Check which packets have high rewards
    # those packets are alone in a slot
    for i in range(SLOTS_COUNT):
      if len(self.slots[i].packets) == 1:
        packet = self.slots[i].packets[0]
        if packet not in first_packets_known:
          equipments_rewards[packet.id] = HIGH_REWARD
          first_packets_known.append(packet)
          new_slots[i].packets.append(packet)

    # delete the packets with high rewards
    for j in range(len(self.slots)):
      for packet in first_packets_known:
        if packet in self.slots[j].packets:
          self.slots[j].packets.remove(packet)

    i = 0

    # check which packets have medium rewards
    # each time we remove a packet, there's probably another collision
    # that's been removed, thus we restart from 0
    while i != len(self.slots):
      if len(self.slots[i].packets) == 1:
        packet = self.slots[i].packets[0]
        equipments_rewards[packet.id] = MEDIUM_REWARD
        new_slots[i].packets.append(packet)

        for j in range(len(self.slots)):
          if packet in self.slots[j].packets:
            self.slots[j].packets.remove(packet)
            i = 0
      i += 1

    self.slots = new_slots

    return equipments_rewards
