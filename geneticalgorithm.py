# Genetic Algorithm and Reinforcement Learning
import os, random
import numpy as np
import neuralnetwork, inputs, snake

class Population:
	def __init__(self, population_size, mutation_rate):
		# Round population size to nearest even number
		self.population_size = population_size + population_size%2
		# Set mutation rate
		self.mutation_rate = mutation_rate
		# Generate a random neural network and snake for each species
		self.neuralnetworks = []
		self.snakes = []
		for i in range(self.population_size):
			self.neuralnetworks.append(neuralnetwork.NeuralNetwork())
			self.snakes.append(snake.Snake())
		# Current mode (training (0) or resume (1))
		self.current_mode = 0
		# Current generation number
		self.generation  = 1
		# Best score achieved by population
		self.population_best = 0
		# Best fitness achieved by population
		self.population_best_fitness = 0
		# Best neural network achieved by population
		self.population_best_nn = self.neuralnetworks[0]
		# Current best score in generation
		self.current_best = 0
		# Current best species in generation
		self.current_best_species = 0
		# When false stops feedforward so that next generation can be built
		self.proceed = True
		# Number of snakes still alive
		self.snakes_alive = self.population_size
		
	# Update population
	def update(self):
		snakes_alive = 0
		self.current_best = 0
		# For each snake
		for i in range(self.population_size):
			# If it is alive
			if self.snakes[i].is_alive:
				# Increase alive count
				snakes_alive += 1
				# If it has the highest score, set it as current_best_species
				if self.snakes[i].score > self.current_best:
					self.current_best = self.snakes[i].score
					self.current_best_species = i
					# Same for high score
					if self.current_best > self.population_best:
						self.population_best = self.current_best
				# Gather inputs and feed them through neural network
				nn_input_batches = inputs.calculate_inputs([self.snakes[i].head[0],self.snakes[i].head[1]], [self.snakes[i].food[0], self.snakes[i].food[1]], self.snakes[i].segments, self.snakes[i].direction)
				outputs = []
				for nn_input_batch in nn_input_batches:
					outputs.append(self.neuralnetworks[i].feedforward(nn_input_batch))
				# Find highest output, apply it to current direction, and clip it
				decision = self.snakes[i].direction + np.argmax(outputs) - 1 
				if decision > 3:
					decision = 0
				elif decision < 0:
					decision = 3
				self.snakes[i].direction = decision
				# Move the snake
				self.snakes[i].move() 
		self.snakes_alive = snakes_alive
		if snakes_alive < 1:
			self.proceed = False
			self.natural_selection()

	# Perform natural selection to create next generation
	def natural_selection(self):
		# Auxiliary functions for natural_selection()
		
		# Calculate all fitnesses
		def calculate_fitnesses(snakes):
			fitnesses = []
			for snake in snakes:
				fitnesses.append(snake.lifetime*((snake.length-2)**2))
			return np.array(fitnesses)
		
		# Fitness Proportionate Selection (Roulette Wheel Selection) of snakes for crossover
		def select_snake(fitnesses_sum, fitnesses, population_size, neuralnetworks):
			# Randomize cutoff
			fitnesses_cutoff = random.randint(0, fitnesses_sum)
			# Run through each snake's fitness and add it to a running sum, as soon as the sum surpasses the cutoff, select that snake
			running_sum = 0
			for i in range(int(population_size/2)):
				running_sum += fitnesses[i]
				if running_sum >= fitnesses_cutoff:
					return neuralnetworks[i]
		
		# Crossover two parent neural networks to form a child neural network
		def crossover(parent_one, parent_two):
			def matrix_crossover(parent_matrix_one, parent_matrix_two):
				child_matrix = []
				row_cutoff = random.randint(0, len(parent_matrix_one))
				column_cutoff = random.randint(0, len(parent_matrix_one[0]))
				for row in range(len(parent_matrix_one)):
					for column in range(len(parent_matrix_one[0])):
						if row < row_cutoff or (row == row_cutoff and column < column_cutoff):
							child_matrix.append(parent_matrix_one[row][column])
						else:
							child_matrix.append(parent_matrix_two[row][column])
				return np.array(child_matrix).reshape(parent_matrix_one.shape)
			child = neuralnetwork.NeuralNetwork()
			for i in range(len(parent_one.weights)):
				child.weights[i] = matrix_crossover(parent_one.weights[i], parent_two.weights[i])
			return child

		# Calculate fitnesses
		fitnesses = calculate_fitnesses(self.snakes)
		for i in range(len(fitnesses)):
			if fitnesses[i] > self.population_best_fitness:
				self.population_best_fitness = i
				self.population_best_nn = self.neuralnetworks[i]
		
		# Keep top 50% fittest neural networks
		best_fitnesses = np.argsort(fitnesses)
		best_fitnesses = best_fitnesses[::-1]
		best_fitnesses = best_fitnesses[:int(self.population_size/2)]
		self.neuralnetworks = [self.neuralnetworks[i] for i in best_fitnesses]

		# Crossover and mutate bottom 50% of species
		fitnesses = [fitnesses[i] for i in best_fitnesses]
		fitnesses_sum = np.sum(fitnesses)
		for i in range(int(self.population_size/2)):
			child = crossover(select_snake(fitnesses_sum, fitnesses, self.population_size, self.neuralnetworks), select_snake(fitnesses_sum, fitnesses, self.population_size, self.neuralnetworks))
			child.mutate(self.mutation_rate)
			self.neuralnetworks.append(child)
		
		# Reset variables for next generation
		self.snakes = []
		for i in range(self.population_size):
			self.snakes.append(snake.Snake())
		self.generation += 1
		self.current_best = 0
		self.current_best_species = 0
		self.proceed = True
	
	# Save best snake
	def save_best(self):
		self.population_best_nn.save("saved")

	