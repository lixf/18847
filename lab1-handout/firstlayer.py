import math
import numpy as np
from scipy import signal

TEST = 15000

class colors:
    reset='\033[0m'
    class fg:
        red='\033[31m'
        green='\033[32m'
        orange='\033[33m'
        blue='\033[34m'
    class bg:
        black='\033[40m'
        red='\033[41m'
        green='\033[42m'
        orange='\033[43m'
        blue='\033[44m'

def GetColor(x):
    if x > 0 and x < 3:
        return colors.bg.green
    elif x >= 3 and x < 6:
        return colors.bg.blue
    elif x >= 6:
        return colors.bg.red
    else: 
        # x == 0
        return ''


#Layer may not be both the first layer and an output layer
class FirstLayer: 
    def __init__ (self, layer_id, training_raw_data, training_target):
        self.layer_id = layer_id
        self.raw_data = training_raw_data
        self.num_bits = 0

        # Stored data after applying the needed filter
        self.filtered_data = np.zeros(np.shape(self.raw_data))
        self.target = training_target # Not sure what this is for!

        # Only output 3 * 3 matrix for spike times
        self.spikes = np.zeros((len(self.raw_data), 28, 28))

    def dump_data(self, data):
        print ("Need to print %d samples" % (len(data)))
        for n in range(len(data)):

            if n != TEST:
                continue

            print('Sample #%d' % n)
            for x in range(28):
                for y in range(28):
                    print (GetColor(data[n][x][y]) + str(int(data[n][x][y])) 
                            + " " + colors.reset, end='')
                print('', end='\n')
    
    def dump_data_small(self, data):
        print ("Need to print %d samples" % (len(data)))
        for n in range(len(data)):

            if n != TEST:
                continue

            print('Sample #%d' % n)
            for x in range(3):
                for y in range(3):
                    print ("%d " % (data[n][(x+12)][(y+12)]), end='')
                print('', end='\n')

    def preprocess(self, my_filter, num_bits=3 ):
        self.num_bits = num_bits
        for n in range(len(self.raw_data)):
            image = np.array(self.raw_data[n]).astype(np.float64)
            image *= (float((1 << num_bits) - 1) / image.max())
            self.raw_data[n] = np.rint(image).astype(np.int8)

        print("after normalizing")
        self.dump_data(self.raw_data)
        self.filtered_data = my_filter(self.raw_data)

        print("after filtering")
        self.dump_data(self.filtered_data)

    def generate_spikes(self, threshold):
        self.dump_data_small(self.filtered_data)
        if self.num_bits == 0:
            print("did not go through preprocessing yet!")
            return

        for n in range(len(self.filtered_data)):
            for x in range(28):
                for y in range(28):
                    # The more intense the data, the earlier the spike time
                    # Since we scaled to some number of bits, let's flip the 
                    # order to generate spikes: (e.g. if 3 bits)
                    # if pixel value is 1 after filtering, the spike time is 6
                    # for 7, it's 0; 5 -> 2,  etc..
                    val = self.filtered_data[n][x][y]
                    if val > threshold :
                        self.spikes[n][x][y] = ((1 << self.num_bits) - 1) - val
                    else :
                        # If less than threshold, then use 8 since we know data
                        # range is only 0-7 and 8 is not in the range.
                        self.spikes[n][x][y] = 8
                    #print ("%d, (%d, %d), %d " % (n, (x), (y), \
                    #            self.spikes[n][x][y]))


    def write_spiketimes(self, path, receptive_field): 
        f= open(path,"w+")
        for n in range(len(self.spikes)):
        #for n in range(10):
            for (x, y) in receptive_field:
                f.write("%d, (%d, %d)/OFF, %d\n" % (n, (x), (y), \
                        self.spikes[n][x][y]))
        return
