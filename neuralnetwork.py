# Neural Network
import numpy as np

class NeuralNetwork:
    def __init__(self, neuron_structure=[4,3,1], filepath=""):
        self.weights = []

        if filepath != "":
            tmp = np.load(filepath, allow_pickle=True)
            self.weights = tmp.tolist()    
            return
        
        # Weight initialization
        for i in range(len(neuron_structure)-1):
            self.weights.append(np.random.rand(neuron_structure[i+1], neuron_structure[i])*2 - 1)
    
    def feedforward(self, inputs):
        # Dot product of input and each layer of weights
        output = np.dot(self.weights[0], inputs)
        for i in range(1, len(self.weights)):
            output = np.dot(self.weights[i], output)
        return output
    
    def save(self, filepath):
        np.save(filepath, np.array(self.weights))

    def mutate(self, mutation_rate):
        def mutate_matrix(matrix, mutation_rate):
            temp = np.array([])
            for _, x in np.ndenumerate(matrix):
                if mutation_rate > np.random.random():
                    temp = np.append(temp, max(min((x+np.random.normal()/5),1), -1))
                else:
                    temp = np.append(temp, x)
            return temp.reshape(matrix.shape)
        for i in range(len(self.weights)):
            self.weights[i] = mutate_matrix(self.weights[i], mutation_rate)