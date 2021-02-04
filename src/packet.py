class Packet:
  """
  A packet is a data that is sent
  on a frame
  """
  def __init__(self, id, message):
    self.id = id
    self.message = message

  def __str__(self):
    """
    Print packet data
    """
    return f"ID: {self.id} | Message: \"{self.message}\""

  def __eq__(self, other):
    if isinstance(other, Packet):
      return self.id == other.id and self.message == other.message
    else:
      return False