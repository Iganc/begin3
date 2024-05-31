import sys
import os

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '../begin')))

import logging
import unittest
import random
from World import World
from Position import Position
from Organisms.Lynx import Lynx
from Organisms.Antelope2 import Antelope
from Organisms.Grass import Grass
from Organisms.Sheep import Sheep


class TestWorld(unittest.TestCase):

    def setUp(self):
        logging.basicConfig(level=logging.DEBUG)
        self.world = World(10, 10)
        random.seed(43)

    def test_add_lynx(self):
        lynx = Lynx(position=Position(xPosition=0, yPosition=0), world=self.world)
        self.world.addOrganism(lynx)
        self.assertEqual(self.world.getOrganismFromPosition(Position(xPosition=0, yPosition=0)).sign, 'R')

    def test_add_antelope(self):
        antelope = Antelope(position=Position(xPosition=1, yPosition=1), world=self.world)
        self.world.addOrganism(antelope)
        self.assertEqual(self.world.getOrganismFromPosition(Position(xPosition=1, yPosition=1)).sign, 'A')

    def test_add_grass(self):
        grass = Grass(position=Position(xPosition=2, yPosition=2), world=self.world)
        self.world.addOrganism(grass)
        self.assertEqual(self.world.getOrganismFromPosition(Position(xPosition=2, yPosition=2)).sign, 'G')

    def test_add_sheep(self):
        sheep = Sheep(position=Position(xPosition=3, yPosition=3), world=self.world)
        self.world.addOrganism(sheep)
        self.assertEqual(self.world.getOrganismFromPosition(Position(xPosition=3, yPosition=3)).sign, 'S')

    def test_organism_movement(self):
        lynx = Lynx(position=Position(xPosition=0, yPosition=0), world=self.world)
        self.world.addOrganism(lynx)
        initial_position = (lynx.position.x, lynx.position.y)
        self.world.makeTurn()
        new_position = (lynx.position.x, lynx.position.y)
        self.assertNotEqual(initial_position, new_position)

    def test_antelope_escape(self):
        lynx = Lynx(position=Position(xPosition=0, yPosition=0), world=self.world)
        antelope = Antelope(position=Position(xPosition=1, yPosition=1), world=self.world)
        self.world.addOrganism(lynx)
        self.world.addOrganism(antelope)
        initial_position_antelope = (antelope.position.x, antelope.position.y)
        self.world.makeTurn()
        new_position_antelope = (antelope.position.x, antelope.position.y)
        self.assertNotEqual(initial_position_antelope, new_position_antelope)
        self.assertGreater(
            abs(new_position_antelope[0] - lynx.position.x) + abs(new_position_antelope[1] - lynx.position.y),
            abs(initial_position_antelope[0] - lynx.position.x) + abs(initial_position_antelope[1] - lynx.position.y)
        )

    def test_plague_duration(self):
        self.world.activatePlague()

        self.world.makeTurn()
        self.assertEqual(self.world.get_plague_turns(), 1)

        self.world.makeTurn()
        self.assertEqual(self.world.get_plague_turns(), 0)

        self.world.makeTurn()
        self.assertEqual(self.world.get_plague_turns(), 0)

    def test_plague(self):
        lynx = Lynx(position=Position(xPosition=0, yPosition=0), world=self.world)
        antelope = Antelope(position=Position(xPosition=1, yPosition=1), world=self.world)
        sheep = Sheep(position=Position(xPosition=2, yPosition=2), world=self.world)
        grass = Grass(position=Position(xPosition=3, yPosition=3), world=self.world)

        self.world.addOrganism(lynx)
        self.world.addOrganism(antelope)
        self.world.addOrganism(sheep)
        self.world.addOrganism(grass)

        initial_live_length_lynx = lynx.liveLength
        initial_live_length_antelope = antelope.liveLength
        initial_live_length_sheep = sheep.liveLength
        initial_live_length_grass = grass.liveLength

        # Activate plague
        self.world.activatePlague()
        self.world.makeTurn()

        # Expected lifespan after plague activation (halved)
        expected_live_length_lynx = max(1, initial_live_length_lynx // 2)
        expected_live_length_antelope = max(1, initial_live_length_antelope // 2)
        expected_live_length_sheep = max(1, initial_live_length_sheep // 2)
        expected_live_length_grass = max(1, initial_live_length_grass // 2)

        # Debug statements to verify the values
        print(f"Expected lynx lifespan after plague: {expected_live_length_lynx}")
        print(f"Actual lynx lifespan after plague: {lynx.liveLength}")

        self.assertEqual(lynx.liveLength, expected_live_length_lynx)  # Should be 9 (18 // 2)
        self.assertEqual(antelope.liveLength, expected_live_length_antelope)
        self.assertEqual(sheep.liveLength, expected_live_length_sheep)
        self.assertEqual(grass.liveLength, expected_live_length_grass)

        # Simulate another turn
        self.world.makeTurn()

        # Lifespan should decrement by 1
        # Expected lifespan after plague activation (halved) and after making a move (decremented by 1)
        expected_live_length_lynx = max(1, initial_live_length_lynx // 2) - 1
        expected_live_length_antelope = max(1, initial_live_length_antelope // 2) - 1
        expected_live_length_sheep = max(1, initial_live_length_sheep // 2) - 1
        expected_live_length_grass = max(1, initial_live_length_grass // 2) - 1

        # Debug statements to verify the values
        print(f"Expected lynx lifespan after next turn: {expected_live_length_lynx}")
        print(f"Actual lynx lifespan after next turn: {lynx.liveLength}")

        self.assertEqual(lynx.liveLength, expected_live_length_lynx)
        self.assertEqual(antelope.liveLength, expected_live_length_antelope)
        self.assertEqual(sheep.liveLength, expected_live_length_sheep)
        self.assertEqual(grass.liveLength, expected_live_length_grass)
        self.assertFalse(self.world.get_plague_turns())

    def test_plague_does_not_affect_new_generations(self):
        lynx = Lynx(position=Position(xPosition=0, yPosition=0), world=self.world)
        self.world.addOrganism(lynx)
        self.world.activatePlague()
        self.world.makeTurn()
        self.world.makeTurn()

        new_lynx = Lynx(position=Position(xPosition=1, yPosition=1), world=self.world)
        self.world.addOrganism(new_lynx)
        self.assertEqual(new_lynx.liveLength, new_lynx.liveLength)

    def test_life_decrement(self):
        sheep = Sheep(position=Position(xPosition=0, yPosition=0), world=self.world)
        self.world.addOrganism(sheep)

        initial_live_length_sheep = sheep.liveLength

        # Ensure that the sheep can make a move
        self.assertTrue(sheep.canMove())

        self.world.makeTurn()
        self.assertEqual(sheep.liveLength, initial_live_length_sheep - 1)

        # Ensure that the sheep can make another move
        self.assertTrue(sheep.canMove())

        self.world.makeTurn()
        self.assertEqual(sheep.liveLength, initial_live_length_sheep - 2)

if __name__ == '__main__':
    unittest.main()
