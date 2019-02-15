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

    # Preprocesses the raw data with a filter
    def preprocess (self, my_filter, num_bits=3 ):
        scaled_data = self.raw_data

        # Max value is 255
        step = 255 / math.pow(2,num_bits)

        # Scale the data down to 3 bits
        scaled_data = 8 - (scaled_data / step).astype(int)
        # apply the filter
        return my_filter(scaled_data)

    def feedforward_inhibition(self, k):
        # Implements feedforward inhibition by making such that,
        # within a given timestep, if there are more than k spikes,
        # they will be nulled out. otherwise, they will pass
        current_volley = self.spikes == 0
        if (np.sum(current_volley) > k):
          self.spikes[self.spikes == 0] = -1

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
        self.feedforward_inhibition(self.inhibit_k)


    def increment_time(self):
        # Updates the spike time value with each time iteration
        self.spikes[self.spikes > -1] -= 1
        self.feedforward_inhibition(self.inhibit_k)