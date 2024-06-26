from Position import Position
from Organisms.Plant import Plant
from Action import Action
from ActionEnum import ActionEnum
from Organisms.Lynx import Lynx
from Organisms.Antelope2 import Antelope
from Organisms.Sheep import Sheep
from Organisms.Grass import Grass
import logging

class World(object):

	def __init__(self, worldX, worldY):
		self.__worldX = worldX
		self.__worldY = worldY
		self.__turn = 0
		self.__organisms = []
		self.__newOrganisms = []
		self.__separator = '.'
		self.__isPlagueActive = False
		self.__plagueTurns = 0

	@property
	def worldX(self):
		return self.__worldX

	@property
	def worldY(self):
		return self.__worldY

	@property
	def turn(self):
		return self.__turn

	@turn.setter
	def turn(self, value):
		self.__turn = value

	@property
	def organisms(self):
		return self.__organisms

	@organisms.setter
	def organisms(self, value):
		self.__organisms = value

	@property
	def newOrganisms(self):
		return self.__newOrganisms

	@newOrganisms.setter
	def newOrganisms(self, value):
		self.__newOrganisms = value

	@property
	def separator(self):
		return self.__separator

	@property
	def isPlagueActive(self):
		return self.__isPlagueActive

	def addOrganismInteractive(self):
		try:
			choice = int(input("Czy chcesz dodać nowy organizm? 0-Nie, 1-Tak "))
		except ValueError:
			return

		if choice == 0:
			return
		if choice == 1:
			try:
				choice2 = int(input("1-owca\n2-trawa\n3-Rys\n4-Antylopa\n"))
				coordinates = input("Podaj koordynaty: ")
				x, y = map(int, coordinates.split(','))  # assuming the coordinates are entered in the format x,y
			except ValueError:
				return

			position = Position(xPosition=x, yPosition=y)
			if choice2 == 1:
				newOrg = Sheep(position=position, world=self)
			elif choice2 == 2:
				newOrg = Grass(position=position, world=self)
			elif choice2 == 3:
				newOrg = Lynx(position=position, world=self)
			elif choice2 == 4:
				newOrg = Antelope(position=position, world=self)
			self.addOrganism(newOrg)
		else:
			return

	def makeTurn(self):
		actions = []
		# Apply plague effects if plague_rounds is greater than 0
		if self.__isPlagueActive:
			self.handlePlague()

		for org in self.organisms:
			if self.positionOnBoard(org.position):
				actions = org.move()
				for a in actions:
					self.makeMove(a)
				actions = []
				if self.positionOnBoard(org.position):
					actions = org.action()
					for a in actions:
						self.makeMove(a)
					actions = []

		self.organisms = [o for o in self.organisms if self.positionOnBoard(o.position)]
		for o in self.organisms:
			o.liveLength -= 1
			o.power += 1
			if not self.__isPlagueActive or self.__plagueTurns != 1:
				o.liveLength -= 1
			if o.liveLength < 1:
				print(str(o.__class__.__name__) + ': died of old age at: ' + str(o.position))
		self.organisms = [o for o in self.organisms if o.liveLength > 0]

		self.newOrganisms = [o for o in self.newOrganisms if self.positionOnBoard(o.position)]
		self.organisms.extend(self.newOrganisms)
		self.organisms.sort(key=lambda o: o.initiative, reverse=True)
		self.newOrganisms = []

		self.turn += 1

	def makeMove(self, action):
		print(action)
		if action.action == ActionEnum.A_ADD:
			self.newOrganisms.append(action.organism)
		elif action.action == ActionEnum.A_INCREASEPOWER:
			action.organism.power += action.value
		elif action.action == ActionEnum.A_MOVE:
			action.organism.position = action.position
		elif action.action == ActionEnum.A_REMOVE:
			action.organism.position = Position(xPosition=-1, yPosition=-1)

	def addOrganism(self, newOrganism):
		newOrgPosition = Position(xPosition=newOrganism.position.x, yPosition=newOrganism.position.y)

		if self.positionOnBoard(newOrgPosition):
			self.organisms.append(newOrganism)
			self.organisms.sort(key=lambda org: org.initiative, reverse=True)
			return True
		return False

	def positionOnBoard(self, position):
		return position.x >= 0 and position.y >= 0 and position.x < self.worldX and position.y < self.worldY

	def getOrganismFromPosition(self, position):
		pomOrganism = None

		for org in self.organisms:
			if org.position == position:
				pomOrganism = org
				break
		if pomOrganism is None:
			for org in self.newOrganisms:
				if org.position == position:
					pomOrganism = org
					break
		return pomOrganism

	def getNeighboringPositions(self, position):
		result = []
		pomPosition = None

		for y in range(-1, 2):
			for x in range(-1, 2):
				pomPosition = Position(xPosition=position.x + x, yPosition=position.y + y)
				if self.positionOnBoard(pomPosition) and not (y == 0 and x == 0):
					result.append(pomPosition)
		return result

	def filterFreePositions(self, fields):
		result = []

		for field in fields:
			if self.getOrganismFromPosition(field) is None:
				result.append(field)
		return result

	def filterPositionsWithoutAnimals(self, fields):
		result = []
		pomOrg = None

		for filed in fields:
			pomOrg = self.getOrganismFromPosition(filed)
			if pomOrg is None or isinstance(pomOrg, Plant):
				result.append(filed)
		return result

	def find_nearby(self, position, sign):
		logging.debug("Finding nearby %s from position %s", sign, position)
		for y in range(self.worldY):
			for x in range(self.worldX):
				org = self.getOrganismFromPosition(Position(xPosition=x, yPosition=y))
				if org and org.sign == sign:
					logging.debug("Found %s at %s", sign, Position(xPosition=x, yPosition=y))
					return Position(xPosition=x, yPosition=y)
		logging.debug("No nearby %s found", sign)
		return None

	def __str__(self):
		result = '\nturn: ' + str(self.__turn) + '\n'
		for wY in range(0, self.worldY):
			for wX in range(0, self.worldX):
				org = self.getOrganismFromPosition(Position(xPosition=wX, yPosition=wY))
				if org:
					result += str(org.sign)
				else:
					result += self.separator
			result += '\n'
		return result

	def activatePlague(self):
		if not self.__isPlagueActive:
			logging.info("Plague will start in the next turn.")
			self.__plagueTurns = 2  # Plague will last for 2 turns
			self.__isPlagueActive = True

	def handlePlague(self):
		logging.info("Plague active, %d turns remaining", self.__plagueTurns)
		if self.__plagueTurns == 2:
			print("Plague has started.")
			for org in self.__organisms:
				logging.debug("Halving life length for %s at position %s", org.__class__.__name__, org.position)
				org.liveLength = max(1, org.liveLength // 2)

		self.__plagueTurns -= 1
		if self.__plagueTurns == 0:
			self.__isPlagueActive = False
			logging.info("Plague has ended.")
			print("Plague has ended.")
