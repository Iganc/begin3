from .Animal import Animal


class Lynx(Animal):

    def __init__(self, lynx=None, position=None, world=None):
        super(Lynx, self).__init__(lynx, position, world)

    def clone(self):
        return Lynx(self, None, None)

    def initParams(self):
        self.power = 6
        self.initiative = 5
        self.liveLength = 18
        self.powerToReproduce = 14
        self.sign = 'R'

    def getNeighboringPosition(self):
        return self.world.filterPositionsWithoutAnimals(self.world.getNeighboringPositions(self.position))