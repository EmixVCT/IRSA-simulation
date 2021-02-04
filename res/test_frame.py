import unittest
from src.frame import Frame
from src.packet import Packet
from src.consts import *

class TestFrame(unittest.TestCase):
    def test_self_interference_cancellation(self):
        frame = Frame()
        frame.slots[0].packets.append(Packet('a', 'a'))
        frame.slots[1].packets.append(Packet('a', 'a'))
        frame.slots[1].packets.append(Packet('b', 'b'))
        frame.slots[1].packets.append(Packet('c', 'c'))
        frame.slots[2].packets.append(Packet('c', 'c'))

        rewards = frame.self_interference_cancellation()
        self.assertEqual(rewards['a'], HIGH_REWARD)
        self.assertEqual(rewards['c'], HIGH_REWARD)
        self.assertEqual(rewards['b'], MEDIUM_REWARD)

    def test_ucb1(self):
        print(Frame.ucb1(3, 4, 3.0))
        print(Frame.ucb1(3, 4, 3.0))
        print(Frame.ucb1(3, 4, 3.0))

        print(Frame.ucb1(3, 4, 2.0))
        print(Frame.ucb1(3, 4, 2.0))
        print(Frame.ucb1(3, 4, 2.0))

        print(Frame.ucb1(10, 4, 3.0))
        print(Frame.ucb1(10, 4, 3.0))
        print(Frame.ucb1(10, 4, 3.0))



unittest.main()
