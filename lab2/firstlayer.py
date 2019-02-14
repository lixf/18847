import math
import numpy as np
from scipy import signal

#Layer may not be both the first layer and an output layer
class FirstLayer: 
    def __init__ (self, layer_id, training_raw_data, threshold):
        self.layer_id = layer_id
        self.raw_data = training_raw_data
        self.spikes=np.full(18, -1)
        self.num_neurons = self.spikes.shape[0]
        self.threshold = threshold

    # Preprocesses the raw data with a filter
    def preprocess (self, my_filter, num_bits=3 ):
        scaled_data = self.raw_data

        # Max value is 255
        step = 255 / math.pow(2,num_bits)

        # Scale the data down to 3 bits
        scaled_data = 8 - (scaled_data / step).astype(int)
        # apply the filter
        return my_filter(scaled_data)

    def generate_spikes(self,filter1, filter2):

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
        self.spikes[self.spikes >= -1] -= 1
