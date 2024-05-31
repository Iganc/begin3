import logging
from Organisms.Animal import Animal
from Position import Position
from Action import Action
from ActionEnum import ActionEnum

class Antelope(Animal):
    def __init__(self, position=None, world=None):
        super().__init__(None, position, world)
        self.initParams()
        logging.debug("Antelope created at %s with world %s", self.position, self.world)

    def initParams(self):
        self.power = 4
        self.initiative = 3
        self.liveLength = 11
        self.powerToReproduce = 5
        self.sign = 'A'

    def clone(self):
        logging.debug("Cloning Antelope at %s with world %s", self.position, self.world)
        return Antelope(position=self.position, world=self.world)

    def move(self):
        logging.debug("Antelope at %s is moving with world %s", self.position, self.world)
        if self.world is None:
            logging.error("World is None for Antelope at %s", self.position)
            raise AttributeError("World is None for Antelope")
        lynx_position = self.world.find_nearby(self.position, 'R')
        if lynx_position:
            escape_position = self.find_escape_position(lynx_position)
            logging.debug("Antelope escaping to %s", escape_position)
            return [Action(ActionEnum.A_MOVE, escape_position, 0, self)]
        else:
            return super().move()

    def find_escape_position(self, lynx_position):
        escape_direction = (self.position.x - lynx_position.x, self.position.y - lynx_position.y)
        escape_position = Position(xPosition=self.position.x + 2 * escape_direction[0], yPosition=self.position.y + 2 * escape_direction[1])
        logging.debug("Calculated escape position: %s", escape_position)
        if self.world.positionOnBoard(escape_position):
            return escape_position
        else:
            return self.position
