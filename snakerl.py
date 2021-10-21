# Main controller
import os, sys, time
import numpy as np
import display, geneticalgorithm, inputs, neuralnetwork, snake 

# Adjustable parameters for training
population_size = 50
mutation_rate = 0.2

# Initializations
population = geneticalgorithm.Population(population_size, mutation_rate)
dp = display.Display()
sn = snake.Snake()
# Load neural network from trained_models/pretrained/neuralnetwork.npy if it exists for pretrained mode
nn = neuralnetwork.NeuralNetwork()
if os.path.isfile("pretrained.npy"):
	nn = neuralnetwork.NeuralNetwork(filepath="pretrained.npy")
else:
	sys.exit('Error: pretrained.npy not found')

# Game modes
mode = 0
mode_descriptions = ["training (1)", "pretrained (2)", "human (3)"]
previous_mode = 0
# Direction for human mode
direction = 4
# High scores for pretrained and human modes
high_scores = [0,0]

# Keyboard bindings for switching population mode and switching directions. Seperate functions needed since onkeypress() does not support function arguments
def save_best():
	global population
	population.save_best()
def training_mode():
	global mode
	mode = 0
def pretrained_mode():
	global mode
	mode = 1
def human_mode():
	global mode
	mode = 2
def direction_right():
	global direction
	direction = 0
def direction_down():
	global direction
	direction = 1
def direction_left():
	global direction
	direction = 2
def direction_up():
	global direction
	direction = 3
dp.wn.listen()
dp.wn.onkeypress(save_best, "s")
dp.wn.onkeypress(training_mode, "1")
dp.wn.onkeypress(pretrained_mode, "2")
dp.wn.onkeypress(human_mode, "3")
dp.wn.onkeypress(direction_right, "Right")
dp.wn.onkeypress(direction_down, "Down")
dp.wn.onkeypress(direction_left, "Left")
dp.wn.onkeypress(direction_up, "Up")

# Main game loop
while True:
	# Update turtle graphics
	dp.wn.update()
	# If the mode just switched, reset the snake
	if mode != previous_mode:
		previous_mode = mode
		sn = snake.Snake()
    # Training
	if mode == 0:
    	# Update population and display the best snake if not currently building the next generation
		if population.proceed:
			population.update()
			dp.update(population.snakes[population.current_best_species].head, population.snakes[population.current_best_species].food, population.snakes[population.current_best_species].segments, [population.snakes[population.current_best_species].score, population.population_best, population.snakes_alive, population.current_best_species+1, population.generation, mode_descriptions[mode]])
	# Pretrained/human modes 
	else:
		# Pretrained mode
		if mode == 1:
			# Update high score
			if sn.score > high_scores[0]:
				high_scores[0] = sn.score
			# Gather input batches
			nn_input_batches = inputs.calculate_inputs([sn.head[0],sn.head[1]], [sn.food[0], sn.food[1]], sn.segments, sn.direction)
			# Feed each batch through neural network
			outputs = []
			for nn_input_batch in nn_input_batches:
				outputs.append(nn.feedforward(nn_input_batch))
			# Find highest output, apply it to current direction, and clip it
			decision = sn.direction + np.argmax(outputs) - 1 
			if decision > 3:
				decision = 0
			elif decision < 0:
				decision = 3
		# Human mode
		if mode == 2:
			# Update high score
			if sn.score > high_scores[1]:
				high_scores[1] = sn.score
			# Set snake's decision to arrow key binds
			decision = direction
		# Move the snake
		sn.direction = decision
		sn.move()
		# Reset the snake if it died
		if not(sn.is_alive):
			sn = snake.Snake()
			direction = 4
		# Display the snake
		dp.update(sn.head, sn.food, sn.segments, [sn.score, high_scores[mode-1], -1, -1, -1, mode_descriptions[mode]])
		# Ensure game stays at ~30 fps when in human mode
		if mode == 2:
			time.sleep(1/30)
wn.mainloop()