from .Animal import Animal
from .Lynx import Lynx
from Position import Position
import random
from Action import Action
from ActionEnum import ActionEnum

class Antelope(Animal):

    def __init__(self, antelope=None, position=None, world=None):
        super(Antelope, self).__init__(antelope, position, world)

    def clone(self):
        return Antelope(self, None, None)

    def initParams(self):
        self.power = 4
        self.initiative = 3
        self.liveLength = 11
        self.powerToReproduce = 5
        self.sign = 'A'

    def getNeighboringPosition(self):
        return self.world.filterPositionsWithoutAnimals(self.world.getNeighboringPositions(self.position))

    def getTwoStepsAwayPositions(self):
        positions = []
        for dx in [-2, -1, 0, 1, 2]:
            for dy in [-2, -1, 0, 1, 2]:
                if dx == 0 and dy == 0:
                    continue
                newPosition = Position(xPosition=self.position.x + dx,
                                       yPosition=self.position.y + dy)  # Modify this line
                if self.world.positionOnBoard(newPosition):
                    positions.append(newPosition)
        return positions

    def getEscapePositions(self, lynxPosition):
        dx = self.position.x - lynxPosition.x
        dy = self.position.y - lynxPosition.y
        escapePositions = []
        for step in [-2, 2]:  # Only consider positions two squares away
            newPosition = Position(xPosition=self.position.x + dx * step, yPosition=self.position.y + dy * step)
            if self.world.positionOnBoard(newPosition) and not isinstance(
                    self.world.getOrganismFromPosition(newPosition), Lynx):
                escapePositions.append(newPosition)
        return escapePositions

    def move(self):
        result = []
        pomPositions = self.getTwoStepsAwayPositions()
        safePositions = [pos for pos in pomPositions if not isinstance(self.world.getOrganismFromPosition(pos), Lynx)]
        newPosition = None
        lynx = None

        lynxPositions = [pos for pos in pomPositions if isinstance(self.world.getOrganismFromPosition(pos), Lynx)]
        if lynxPositions:
            lynx = self.world.getOrganismFromPosition(random.choice(lynxPositions))
            escapePositions = self.getEscapePositions(lynx.position)
            if escapePositions:
                newPosition = random.choice(escapePositions)
            else:
                newPosition = lynx.position
                if lynx.power > self.power:
                    result.append(Action(ActionEnum.A_REMOVE, self.position, 0, self))
                    lynx.power -= self.power
                else:
                    result.append(Action(ActionEnum.A_REMOVE, newPosition, 0, lynx))
                    self.power -= lynx.power
                result.append(Action(ActionEnum.A_FIGHT, newPosition, 0, self, newPosition, lynx))
        elif safePositions:
            newPosition = random.choice(safePositions)

        if newPosition and self.world.positionOnBoard(newPosition):
            metOrganism = self.world.getOrganismFromPosition(newPosition)
            if metOrganism is not None and not isinstance(metOrganism, Antelope) and metOrganism != lynx:
                result.append(Action(ActionEnum.A_MOVE, newPosition, 0, self))
                self.lastPosition = self.position
                result.extend(metOrganism.consequences(self))
        return result
