import math
import numpy as np
import matplotlib.pyplot as plt

# This layer connects to a previous layer that is spiking.
# It carries W weights that are initialized at random.
# If the sum of the weights from the previous layer that
# are at local time 0 exceeds a neuron_sum threshold,
# then a spike occurs at the neuron.

# Reset is used between each training image to clear
# the neuron sums that have accumulated from the previous image

# After each time step, the neuron sums are decremented along with
# the local spiketimes.

# Immediately as soon as the neuron sums exceeds the threshold,
# firing happens immediately. Therefore, in local time, the spike
# will always be 0 and therefore self.spikes will always be either
# -1 or 0, where -1 is no spike and 0 is a spike happenning right now.
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

        # spike when the neuron sum exceeds the threshold
        self.spikes[self.neuron_sums >= threshold] = 0
        
        # reset the neuron sums after firing
        self.neuron_sums[self.neuron_sums > threshold] = 0

        return
    
    def increment_time(self):
        """
        This function will allow the current stimulation of the neurons
        to decay. It will also decrement the spike time number by 1.
        """
        self.spikes[self.spikes > -1] -= 1
        self.neuron_sums[self.neuron_sums > 5] -= .5

