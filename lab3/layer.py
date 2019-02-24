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
# firing happens immediately.  Therefore, in local time, the spike
# will always be 0 and therefore self.spikes will always be either
# -1 or 0, where -1 is no spike and 0 is a spike happenning right now.
class Layer():
    def __init__(self, layer_id, num_neurons, prev_layer, threshold):  
        self.layer_id = layer_id
        self.prev_layer = prev_layer
        self.threshold = threshold
        self.num_neurons = num_neurons
        self.W = np.random.random(size=(prev_layer.num_neurons, num_neurons)) * 10
        self.neuron_sums = np.zeros(shape=(num_neurons))
        self.spikes = np.full(shape=(num_neurons),fill_value=-1)
        self.inhibited_spikes = np.full(shape=(num_neurons), fill_value = False)

        self.curr_winner_count = 0
        self.remaining_inhibition_time = 0

        self.curr_volley_count = 0
        self.remaining_FF_time = 0

    def reset(self): 
        # Reset the network, clearing out any accumulator variables, etc
        self.neuron_sums = np.zeros(shape=(self.num_neurons))
        self.spikes = np.full(shape=(self.num_neurons),fill_value=-1)
        self.curr_winner_count = 0
        self.remaining_inhibition_time = 0
        self.curr_volley_count = 0
        self.remaining_FF_time = 0

    
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
        indices = np.array(np.where(self.spikes==0)[0])
        if (indices.shape[0] > 0):
          #print("neuron sums: ",self.neuron_sums)
          #print("Weights: ", self.W)
          #print("Prev layer spikes", self.prev_layer.spikes)
          #print("indicess", indices)
          pass
        self.neuron_sums[self.neuron_sums >= threshold] = 0

        return
    
    def increment_time(self):
        """
        This function will allow the current stimulation of the neurons
        to decay. It will also decrement the spike time number by 1.
        """
        self.spikes[self.spikes > -1] -= 1
        self.neuron_sums[self.neuron_sums > 5] -= .5

    def feedforward_inhibition(self, k, FF_WINDOW):
        # Implements feedforward inhibition by making such that,
        # within a given timestep, if there are more than k spikes,
        # they will be nulled out. otherwise, they will pass
        curr_volley = self.prev_layer.spikes == 0

        if self.remaining_FF_time == 0 and np.sum(curr_volley) > 0:
          self.curr_volley_count = 0
          self.remaining_inhibition_time = FF_WINDOW
        else:
          self.remaining_inhibition_time -= 1
        self.curr_volley_count += np.sum(curr_volley)
        if (np.sum(curr_volley) > k):
          self.prev_layer.spikes[self.prev_layer.spikes == 0] = -1

    def wta(self, num_winners, LI_WINDOW):
        '''
        Performs Winner-Take-All inhibition on the spikes
        num_winner is the number of winners we will let pass the inhibition
        winner_index is the previous winning index
        '''
        spikes = self.spikes

        potential_winners = np.array(np.where(spikes == 0)[0])
        old_spikes = np.copy(spikes)
        out = np.copy(spikes)

        if self.remaining_inhibition_time == 0 and np.sum(spikes == 0) > 0:
          self.curr_winner_count = 0
          self.remaining_inhibition_time = LI_WINDOW
        else:
          self.remaining_inhibition_time -= 1
        
        random_losers = np.array([])

        
        winners_left = num_winners - self.curr_winner_count
        winners_selected = min(winners_left, potential_winners.shape[0])
        self.curr_winner_count += winners_selected
        if potential_winners.shape[0]:
          np.random.shuffle(potential_winners)
          random_losers = potential_winners[winners_selected:]
          out[random_losers] = -1
        
        self.inhibited_spikes[(old_spikes == 0) & (out == -1)] = True
        self.spikes = np.copy(out)
        winners = np.array(np.where(self.spikes == 0))
        return (out, winners)

    def STDP(self):
      input_spikes = self.prev_layer.spikes == 0
      curr_spikes = self.spikes == 0


      input_output = np.outer(input_spikes == True, curr_spikes == True)
      input_no_output = np.outer(input_spikes == True, curr_spikes == False)
      input_inhibited_output = np.outer(input_spikes == True, self.inhibited_spikes == True)
      no_input_output = np.outer(input_spikes == False, curr_spikes == True)

      self.W[input_output == True] = np.minimum(10,self.W[input_output == True] + .5)
      self.W[input_no_output == True] = np.minimum(10,self.W[input_no_output == True] + .1)
      self.W[input_inhibited_output == True] = np.minimum(10,self.W[input_inhibited_output == True] - .1)
      #self.W[no_input_output == True] = 0
      self.W[no_input_output == True] = np.maximum(0,self.W[no_input_output == True] - .5)
