from src.packet import Packet

class Station:
  """
  A station is en equipment that is able
  to send packets on a frame
  """
  def __init__(self, id):
    self.id = id

  @staticmethod
  def send_packet(frame, id, message, copies_count):
    """
    Send a packet multiple times on the given frame
    @param frame: the frame on which the packet has to be sent
    @param id: the id of the packet
    @param message: the message of the packet
    @param copies_count: the number of copies to send
    """
    frame.add_packet(Packet(id, message), copies_count)
