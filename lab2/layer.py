import math
import numpy as np
import matplotlib.pyplot as plt

class Layer():
    def __init__(self, layer_id, num_neurons, prev_layer, threshold):  
        self.layer_id = layer_id
        self.prev_layer = prev_layer
        self.threshold = threshold
        self.num_neurons = num_neurons
        self.W = np.random.random(size=(prev_layer.num_neurons, num_neurons))
        self.neuron_sums = np.zeros(shape=(num_neurons))
        self.spikes = np.full(shape=(num_neurons),fill_value=-1)

    def reset(self): 
        # Reset the network, clearing out any accumulator variables, etc
        self.neuron_sums = np.zeros(shape=(self.num_neurons))
        self.spikes = np.full(shape=(self.num_neurons),fill_value=-1)

    
    def generate_spikes(self):
        """
        This function generates spikes based for the current time iteration
        based on the how much the neurons have been stimulated in
        this iteration and previous iterations
        """
        W = self.W
        threshold = self.threshold
        input_spikes = (self.prev_layer.spikes == 0)

        self.neuron_sums += np.matmul(input_spikes, W)
        self.spikes[self.neuron_sums >= threshold] = 0
        
        self.neuron_sums[self.neuron_sums > threshold] = 0

        return
    
    def increment_time(self):
        """
        This function will allow the current stimulation of the neurons
        to decay. It will also decrement the spike time number by 1.
        """
        self.spikes[self.spikes > -1] -= 1
        self.neuron_sums[self.neuron_sums > 5] -= .5

