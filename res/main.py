from src.packet import Packet
from src.station import Station
from src.frame import Frame
from src.station import Station
from src.base_station import BaseStation

global frame
frame = Frame()

station1 = Station(1)
station2 = Station(2)
station1.send_packet(frame, "a", "bonsoir", 5)
station2.send_packet(frame, 2, "bonjour", 10)


# Test
for slot in frame.slots:
  for packet in slot.packets:
    print(packet)