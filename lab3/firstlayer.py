import math
import numpy as np
from scipy import signal

# This class defines the first input layer. It takes in the raw
# training data for a single image. It will only look at the receptive field
# of 3x3 pixels, which are at the center of the image. It will then output spikes.
# These spikes will be stored in self.spikes.
# After each time iteration, increment_time is called to update the local spike times.

# The threshold value is right above the cutoff point for the highest value of spike time.
# Feedforward inhibition is implemented by limiting the number of spikes in a given
# timestep to inhibit_k.
class FirstLayer: 
    def __init__ (self, layer_id, training_raw_data, threshold, inhibit_k):
        self.layer_id = layer_id
        self.raw_data = training_raw_data
        self.spikes=np.full(18, -1)
        self.num_neurons = self.spikes.shape[0]
        self.threshold = threshold
        self.inhibit_k = inhibit_k
        
        self.inhibited_spikes = np.full(shape=(18), fill_value = False)

        self.curr_winner_count = 0
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

    def generate_spikes(self,filter1, filter2):

        # Generates spikes with values ranging from 0 to the threshold
        # The spike with value 0 will occur immediately, while the spikes
        # with higher values will occur later.

        # Applies 2 filters to a receptive field of 3x3
        preprocessed1 = self.preprocess(filter1)[12:15, 12:15]
        preprocessed2 = self.preprocess(filter2)[12:15, 12:15]

        # Combines the two filters to be contained within 18 neurons

        preprocessed = np.concatenate((preprocessed1, preprocessed2), axis=0)
        # Makes large difference result in early spike and small difference in late spike
        spikes = 8 - preprocessed.reshape(self.spikes.shape)

        # Sets value to -1 if no spike
        spikes[spikes >= self.threshold] = -1
        self.spikes = spikes


    def increment_time(self):
        # Updates the spike time value with each time iteration
        self.spikes[self.spikes > -1] -= 1
        #self.feedforward_inhibition(self.inhibit_k)
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
