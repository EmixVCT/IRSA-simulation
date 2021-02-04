class Slot:
  """ A slot is a partition of a frame"""
  def __init__(self):
    self.packets = list()

  def add_packet(self, packet):
    """
    Add a packet in the slot
    @param packet: the packet to add
    """
    self.packets.append(packet)


  def contains_packet(self, packet):
    """
    Check if the slot contains the given packet
    @param packet: the packet to look for
    @return true if the packet exists in the slot,
    otherwise false
    """
    return packet in self.packets
