import unittest
from Organisms.Antelope import Antelope
from Organisms.Lynx import Lynx
from Position import Position

class TestAntelope(unittest.TestCase):
    def setUp(self):
        self.world = None  # Replace with an instance of your World class
        self.antelope = Antelope(position=Position(xPosition=5, yPosition=5), world=self.world)
        self.lynx = Lynx(position=Position(xPosition=6, yPosition=6), world=self.world)

    def test_fight(self):
        # Define the expected power values
        expected_antelope_power = 4
        expected_lynx_power = 6

        # Call the move method
        self.antelope.move()

        # Assert that the state of the Antelope and the Lynx are as expected
        self.assertEqual(self.antelope.power, expected_antelope_power)
        self.assertEqual(self.lynx.power, expected_lynx_power)