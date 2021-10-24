# SnakeRL
Getting a computer to play snake using reinforcement learning, written from scratch in Python.

## Usage
The program has 3 modes:
(1) Standard learning mode
(2) Watch a pre-trained neural network play (saved in `pretrained.npy` - you can press `s` to save the current best neural network and replace this file)
(3) Human mode - try playing the game for yourself

## Design
### Neural Network
The same neural network is evaluated 3 times for each possible direction (left, right or straight ahead) the snake can go. The direction with the highest confidence is selected. This design keeps the network very small, allowing it to train much faster.

1. **Inputs (4 neurons):** 
 - Distance differential with food if snake proceeds with this direction (normalised between -1 and 1)
 - Object ahead of snake, to its left and to its right relative to the direction being evaluated (-1 for tail or wall, 1 for food, 0 for nothing)

2. **Single hidden layer of 3 neurons**
3. **Single output neuron representing confidence for this direction**

### Fitness evaluation
Fitness is given by: *fitness=lifetime * (score+1)^2*

Where *lifetime* is the number of moves (including moving straight ahead) the snake has made in total (note that snakes are limited to 150 moves between food acquisitions to prevent the strategy of indefinitely moving in a circle).

### Genetic Algorithm
After every snake in a generation has died (the number of neural networks in a generation can be changed with the `population_size` parameter in `snakerl.py`) the next generation is generated.
 - The top 50% best performing neural networks automatically move onto the next generation. 
 - Remaining neural networks are a crossover generated from a pair of neural networks selected using roulette selection. 
   - Some of their weights can also be "mutated" (the rate at which this occurs can be changed with the `mutation_rate` parameter in `snakerl.py`). When a weight is mutated, it's value is offset by a random number generated from a normal pdf