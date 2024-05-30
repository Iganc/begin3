from ActionEnum import ActionEnum


class Action(object):

	def __init__(self, action, position, value, organism, fight_position=None, opponent=None):
		self.__action = action
		self.__position = position
		self.__value = value
		self.__organism = organism
		self.__fight_position = fight_position
		self.__opponent = opponent

	@property
	def action(self):
		return self.__action

	@property
	def position(self):
		return self.__position

	@property
	def value(self):
		return self.__value

	@property
	def organism(self):
		return self.__organism

	@property
	def opponent(self):
		return self.__opponent

	@property
	def fight_position(self):
		return self.__fight_position

	def __str__(self):
		className = self.organism.__class__.__name__
		opponentName = self.opponent.__class__.__name__ if self.opponent else ""
		choice = {
			ActionEnum.A_ADD: '{0}: add at: {1}'.format(className, self.position),
			ActionEnum.A_INCREASEPOWER: '{0} increase power: {1}'.format(className, self.value),
			ActionEnum.A_MOVE: '{0} move form: {1} to: {2}'.format(className, self.organism.position, self.position),
			ActionEnum.A_REMOVE: '{0} remove form: {1}'.format(className, self.organism.position),
			ActionEnum.A_FIGHT: '{0} fought {1} at {2}'.format(className, opponentName, self.fight_position)
		}
		return choice[self.action]
