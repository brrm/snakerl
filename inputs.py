import numpy as np

def calculate_inputs(head_position, food_position, segment_positions, current_heading):
	# Returns the square root of the sum of square of x distance and square of y distance
	def calculate_distance(item_one, item_two):
		return ((item_one[0]-item_two[0])**2 + (item_one[1]-item_two[1])**2)**0.5
	directions = [[10,0],[0,-10],[-10,0],[0,10]]
	# Get distance between head position, and food position 
	current_distance = (calculate_distance(head_position, food_position))
	# Food distance differential for each direction
	distance_differentials = []
	# Item found in each direction (-1=bad (wall, tail), 0=neutral (nothing), 1=good (food)
	items = []
	food_found = False
	# Go in each direction
	for i in range(0,4):
		# New position after moving in that direction
		new_position = np.sum([head_position,directions[i]],axis=0)
		# Append food distance differential for that direction
		distance_differentials.append(current_distance - calculate_distance(new_position, food_position))
		# Check for item in new position
		item = 0
		# If food is in the new direction
		if not(food_found) and np.array_equal(new_position, food_position):
			item = 1
			food_found = True
		# If wall is in the new direction
		elif not(5 <= new_position[0] <= 385) or not(-185 <= new_position[1] <= 195):
			item = -1
		# If tail is in the new direction
		else:
			for segment_position in segment_positions:
				if np.array_equal(new_position, segment_position):
					item = -1
					continue
		items.append(item)
	# Get distance_differentials and items ready for inputing directly
	# If the snake is stopped
	if current_heading == 4:
		# Then it must be facing up
		current_heading = 3
	# Clipping so that it cycles directions instead of going out of bounds
	def clip(x):
		if x > 3:
			return 0
		elif x < 0 :
			return 3
		else: 
			return x
	input_batches = []
	for i in range(current_heading-1, current_heading+1):
		i = clip(i)
		input_batches.append([distance_differentials[i],items[clip(i-1)],items[i],items[clip(i+1)]])
	return np.array(input_batches)

