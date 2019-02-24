import numpy as np
import matplotlib.pyplot as plt
from sklearn.datasets import fetch_mldata
import firstlayer as firstlayer
import layer as layer
from filters import OffCenterFilter, OnCenterFilter
import csv

# Lateral inhibition window size
LI_WINDOW = 1

mnist = fetch_mldata('MNIST original')
N, _ = mnist.data.shape

# Reshape the data to be square
mnist.square_data = mnist.data.reshape(N,28,28)


def wta(spikes, t, num_winner, winner_index):
    '''
    Performs Winner-Take-All inhibition on the spikes
    t is the current time step
    num_winner is the number of winners we will let pass the inhibition
    winner_index is the previous winning index
    '''
    out = np.zeros(spikes.shape)
    out[:] = -1
    winner = 0
    index = []

    # Need to generate new winner
    if t % LI_WINDOW == 0:
        index = []
        for i in range(spikes.shape[0]):
            if winner != num_winner and spikes[i] == 0:
                out[i] = 0
                index.append(i)
                winner += 1
    else:
        index = winner_index
        # Take the spikes from the winning neurons
        for i in winner_index:
            out[i] = spikes[i]
    
    return (out, index)


# Structure of the TNN
layer1 = firstlayer.FirstLayer(layer_id=1, training_raw_data=mnist.square_data[0], threshold=8, inhibit_k=3)
layer2 = layer.Layer(layer_id=2, num_neurons=16, prev_layer=layer1, threshold=3)
num_iterations = 9

''' Test for WTA
spikes = []
spikes.append(np.array([0, -1, 0, 0]))
spikes.append(np.array([-1, -1, 0, 0]))
spikes.append(np.array([0, -1, -1, 0]))
spikes.append(np.array([-1, -1, -1, 0]))
spikes.append(np.array([-1, -1, -1, 0]))

li_index = []

for t in range(5):
    print("spikes for LI: ", spikes[t])
    (li_spikes, li_index) = wta(spikes[t], t, 1, li_index)
    print(li_spikes, li_index)
'''

with open('spiketimes.csv', 'w', newline='') as csvfile:
  writer = csv.writer(csvfile)

  # Generates spikes for layer 1 using 2 different filters
  for i in range(len(mnist.square_data)):
    layer1.raw_data = mnist.square_data[i]
    layer1.generate_spikes(OnCenterFilter, OffCenterFilter)

    li_index = []

    for j in range(num_iterations):
      layer2.generate_spikes()
      (li_spikes, li_index) = wta(layer2.spikes, j, 1, li_index)

      for k in range(layer2.spikes.shape[0]):
        if (li_spikes[k] == 0):
          image_number = i
          spike_position = k
          spike_time = j
          #print([image_number, spike_position, spike_time])
          writer.writerow([image_number, spike_position, spike_time])
  
      layer1.increment_time()
      layer2.increment_time()
    
    layer2.reset()
    print("\rComplete: ", i+1, end="")
