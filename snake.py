# Snake game
import random
import numpy as np

class Snake:
	def __init__(self):
		# Initialize snake head position
		self.head = [205, 5]
		# Initialize variables for neural network
		self.is_alive = True
		self.moves = 150
		self.lifetime = 0
		self.length = 0
		self.score = 0
		# Initialize snake's tail
		self.segments = []
		self.add_segments(3)
		# Initialize food position
		self.food = []
		self.position_food()
		# Set snake's direction to stop
		self.direction = 4

	# Add x segments (num_segments) to the snake
	def add_segments(self, num_segments):
		for i in range(num_segments):
			self.segments.append([205,-5-10*i])
			self.length += 1

	# Randomly position food, ensuring it is not on the snake's body
	def position_food(self):
		# Randomize food position
		self.food = [random.randint(-20, 18)*10+205,random.randint(-19, 19)*10+5]
		# If on head
		if np.array_equal(self.head, self.food):
			# Rerandomize it
			self.position_food()
		# If on body
		else:
			for segment in self.segments:
				if np.array_equal(segment, self.food):
					# Rerandomize it
					self.position_food()
					continue

	# Move the snake in a specified direction
	def move(self):
		# Check that direction is not "stop"
		if self.direction != 4:
			# Move the segments in reverse order
			for i in range(len(self.segments)-1, 0, -1):
				self.segments[i] = [self.segments[i-1][0], self.segments[i-1][1]]
			# Move first segment to head's position
			self.segments[0] = [self.head[0], self.head[1]]
			# Move the head
			# If direction is "right"
			if self.direction == 0:
				self.head[0] += 10
			# If direction is "down"
			elif self.direction == 1:
				self.head[1] -= 10
			# If direciton is "left"
			elif self.direction == 2:
				self.head[0] -= 10
			# If direction is "up"
			elif self.direction == 3:
				self.head[1] += 10
			# Check the snake's status
			self.check_status()
			self.moves -= 1
			self.lifetime += 1

	# Check if the snake has eaten food, is out of moves, has hit a wall, or hit itself
	def check_status(self):
		# Check if snake is out of moves
		if self.moves < 1:
			self.is_alive = False
			self.direction = 4
		# Check if snake has eaten food
		elif np.array_equal(self.head, self.food):
			self.position_food()
			self.add_segments(1)
			self.score += 1
			self.moves += 100
		# Check if snake has hit a wall
		elif not(5 <= self.head[0] <= 385) or not(-185 <= self.head[1] <= 195):
			self.is_alive = False
			self.direction = 4
		# Check if snake has hit itself
		else:
			for segment in self.segments:
				if np.array_equal(self.head, segment):
					self.is_alive = False
					self.direction = 4
					continue