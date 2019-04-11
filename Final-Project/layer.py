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
    def __init__(self, layer_id, num_neurons, prev_layer, threshold, can_overlap=True, max_repeats=-1):  
        self.layer_id = layer_id
        self.prev_layer = prev_layer
        self.threshold = threshold
        self.num_neurons = num_neurons
        self.W = np.random.random(size=(prev_layer.num_neurons, num_neurons)) * 10
        self.neuron_sums = np.zeros(shape=(num_neurons))
        self.spikes = np.full(shape=(num_neurons),fill_value=-1)
        self.contributing_spikes = np.full(shape=(self.W.shape),fill_value=False)
        self.can_overlap = can_overlap
        self.max_repeats = max_repeats

        self.assignments = np.full((10,num_neurons), False)

        #this stores the spikes which were inhibited laterally
        self.inhibited_spikes = np.full(shape=(num_neurons), fill_value = False)

        self.old_spikes = np.full(shape=(num_neurons),fill_value=-1)

        # this returns the current number of spikes which may pass in lateral inhibition
        # for example, if there are spikes at time t=0, 1, 2, 3, 4, 5, and the inhibition
        # window is the entire volley, at time 3, curr_winner_count will be 3.
        self.curr_winner_count = 0

        # this is the number of time steps remaining before the inhibition 
        # window closes and resets
        self.remaining_inhibition_time = 0

        # this is the current number of spikes which may pass feedforward inhibition
        self.curr_volley_count = 0
        #this is the number of time steps remaining before feedfoward inhibition
        #window closers and resets
        self.remaining_FF_time = 0
        

    def reset(self): 
        # Reset the network, clearing out any accumulator variables, etc
        self.neuron_sums = np.zeros(shape=(self.num_neurons))
        self.spikes = np.full(shape=(self.num_neurons),fill_value=-1)
        self.curr_winner_count = 0
        self.remaining_inhibition_time = 0
        self.curr_volley_count = 0
        self.remaining_FF_time = 0
        self.contributing_spikes = np.full(shape=(self.W.shape),fill_value=False)
        self.old_spikes = np.full(shape=(self.num_neurons),fill_value=-1)

    
    def generate_spikes(self):
        """
        This function generates spikes based for the current time iteration
        based on the how much the neurons have been stimulated in
        this iteration and previous iterations
        """
        W = self.W
        threshold = self.threshold
        input_spikes = (self.prev_layer.spikes == 0)
        contributing_spikes = np.outer(input_spikes == True, np.full((self.num_neurons), True))

        self.contributing_spikes = contributing_spikes | self.contributing_spikes

        self.neuron_sums += np.matmul(input_spikes, W)
        self.spikes[self.neuron_sums >= threshold] = 0
        self.old_spikes = np.copy(self.spikes)
        indices = np.array(np.where(self.spikes==0)[0])
        if (indices.shape[0] > 0):
          #print("neuron sums: ",self.neuron_sums)
          #print("Weights: ", self.W)
          #print("Prev layer spikes", self.prev_layer.spikes)
          #print("indicess", indices)
          pass
        self.neuron_sums[self.neuron_sums >= threshold] = 0

        return
    
    def supervised_rule(self, label):
        if self.can_overlap == False:
          for i in range(len(self.spikes)):
            if self.spikes[i] == 0:
              existing_assignments = self.assignments[:,i]
              if (np.sum(existing_assignments) != 0 and existing_assignments[label] == False):
                self.spikes[i] = -1
        existing_assignments = self.assignments[label]
        assignments_left = self.max_repeats - np.sum(existing_assignments)
        for i in range(len(self.spikes)):
          if (self.spikes[i] == 0):
            if (assignments_left > 0 or self.max_repeats == -1):
              if (existing_assignments[i] == False):
                assignments_left -= 1
              self.assignments[label, i] = True

            elif existing_assignments[i] == False:
              self.spikes[i] = -1


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

        # this array stores the indices of potential winning neurons
        # that may pass lateral inhibition
        potential_winners = np.array(np.where(spikes == 0)[0])

        old_spikes = np.copy(spikes) #copying the spikes to some temp variable
        out = np.copy(spikes) # out is the output of winner take all

        # if the window has not been set yet, then the remaining inhibition
        # time will be zero. once a spike occurs and the window has not been set,
        # then the inhibition time counter will be set to the size of the window
        if self.remaining_inhibition_time == 0 and np.sum(spikes == 0) > 0:
          self.curr_winner_count = 0
          self.remaining_inhibition_time = LI_WINDOW
        else:
          #decrement the counter for lateral inhibition time
          self.remaining_inhibition_time -= 1
        
        random_losers = np.array([]) #stores the spike indices that will be set to no spike

        # indicates the number of remaining winners possible as the total acceptable winners
        # minus the current number of accepted winners
        winners_left = num_winners - self.curr_winner_count

        # indicates the number of winners selected from the potential winners
        winners_selected = min(winners_left, potential_winners.shape[0])

        # increments the accepted winners count
        self.curr_winner_count += winners_selected
        if potential_winners.shape[0]:

          #shuffles the potential winners
          np.random.shuffle(potential_winners)

          # subindexes the array to section off the loser indices
          random_losers = potential_winners[winners_selected:]

          # sets the output given the loser indices to -1
          out[random_losers] = -1
        
        # sets the inhibited spike array based on if a neuron was inhibited
        self.inhibited_spikes[(old_spikes == 0) & (out == -1)] = True

        # updates self.spikes
        self.spikes = np.copy(out)

        # winners is the indices for the winners
        winners = np.array(np.where(self.spikes == 0))
        return (out, winners)

    def stdp_update_rule(self, parameters=None):
      curr_spikes = self.spikes == 0
      selected_spikes = np.outer(np.full((self.prev_layer.num_neurons), True), curr_spikes == True)
      inhibited_spikes = np.outer(np.full((self.prev_layer.num_neurons), True), self.spikes != self.old_spikes)

      input_output_weight = 0.5
      input_no_output_weight = 0.5
      input_inhibited_output_weight = 0.5
      no_input_output_weight = 0.5

      if parameters:
        input_output_weight, input_no_output_weight, input_inhibited_output_weight, no_input_output_weight = parameters

      # these are 2d arrays storing boolean values for the condition of the input and
      # output arrays. for example, input_output[i,j] is true if the input neuron i
      # is true and output neuron j is true.


      input_output = self.contributing_spikes & selected_spikes
      input_no_output = self.contributing_spikes & ~selected_spikes
      input_inhibited_output = self.contributing_spikes & inhibited_spikes
      no_input_output = ~self.contributing_spikes & selected_spikes

      #print(self.W)

      # self.W indixes these 2d arrays and performs stdp 
      # the values for the weights to increase and decrease are manually picked
      self.W[input_output == True] = np.minimum(10,self.W[input_output == True] + input_output_weight)
      self.W[input_no_output == True] = np.minimum(10,self.W[input_no_output == True] + input_no_output_weight)
      self.W[input_inhibited_output == True] = np.maximum(0,self.W[input_inhibited_output == True] - input_inhibited_output_weight)
      #self.W[no_input_output == True] = 0
      self.W[no_input_output == True] = np.maximum(0,self.W[no_input_output == True] - no_input_output_weight)

