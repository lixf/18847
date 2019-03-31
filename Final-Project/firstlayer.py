import math
import numpy as np
from scipy import signal

# This class defines the first input layer. It takes in the raw
# training data for a single image. It will only look at the receptive field
# of 3x3 pixels, which are at the center of the image. It will then output spikes.
# These spikes will be stored in self.spikes.
# After each time iteration, increment_time is called to update the local spike times.

# The threshold value is right above the cutoff point for the highest value of spike time.

class FirstLayer: 
    def __init__ (self, layer_id, training_raw_data, threshold, receptive_field_length=2):
        self.layer_id = layer_id
        self.raw_data = training_raw_data
        self.spikes=np.full((receptive_field_length**2)*2, -1)
        self.num_neurons = self.spikes.shape[0]
        self.threshold = threshold
        self.receptive_field_length = receptive_field_length
        #this stores the spikes which were inhibited laterally
        self.inhibited_spikes = np.full(shape=(8), fill_value = False)

        # this returns the current number of spikes which may pass in lateral inhibition
        # for example, if there are spikes at time t=0, 1, 2, 3, 4, 5, and the inhibition
        # window is the entire volley, at time 3, curr_winner_count will be 3.
        self.curr_winner_count = 0

        # this is the number of time steps remaining before the inhibition 
        # window closes and resets
        self.remaining_inhibition_time = 0

    # Preprocesses the raw data with a filter
    def preprocess (self, my_filter, num_bits=3 ):
        scaled_data = self.raw_data

        # Max value is 255
        step = 255 / math.pow(2,num_bits)

        # Scale the data down to 3 bits
        scaled_data = 8 - (scaled_data / step).astype(int)
        # apply the filter
        return my_filter(scaled_data)

    def reset(self): 
        # Reset the network, clearing out any accumulator variables, etc
        self.curr_winner_count = 0
        self.remaining_inhibition_time = 0

    def generate_spikes(self,filter1, filter2, starting_point, size):

        # Generates spikes with values ranging from 0 to the threshold
        # The spike with value 0 will occur immediately, while the spikes
        # with higher values will occur later.

        # Applies 2 filters to a receptive field of 3x3
        start_x = starting_point[0]
        start_y = starting_point[1]
        preprocessed1 = self.preprocess(filter1)[start_x:start_x+self.receptive_field_length, start_y:start_y+self.receptive_field_length]
        preprocessed2 = self.preprocess(filter2)[start_x:start_x+self.receptive_field_length, start_y:start_y+self.receptive_field_length]

        # Combines the two filters to be contained within 8 neurons

        preprocessed = np.concatenate((preprocessed1, preprocessed2), axis=0)
        # Makes large difference result in early spike and small difference in late spike
        spikes = 8 - preprocessed.reshape(self.spikes.shape)

        # Sets value to -1 if no spike
        spikes[spikes >= self.threshold] = -1
        self.spikes = spikes


    def increment_time(self):
        # Updates the spike time value with each time iteration
        self.spikes[self.spikes > -1] -= 1

    def feedforward_inhibition(self, num_winners):
        potential_winners = self.spikes >= 0
        if np.sum(potential_winners) > num_winners:
          self.spikes[self.spikes >= 0] = -1

        
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