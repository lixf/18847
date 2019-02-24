import numpy as np
import matplotlib.pyplot as plt
from sklearn.datasets import fetch_mldata
import firstlayer as firstlayer
import layer as layer
from filters import OffCenterFilter, OnCenterFilter
import csv

# Lateral inhibition window size
LI_WINDOW = 3

mnist = fetch_mldata('MNIST original')
N, _ = mnist.data.shape

# Reshape the data to be square
mnist.square_data = mnist.data.reshape(N,28,28)

# Structure of the TNN
layer1 = firstlayer.FirstLayer(layer_id=1, training_raw_data=mnist.square_data[0], threshold=8, inhibit_k=3)
layer2 = layer.Layer(layer_id=2, num_neurons=10, prev_layer=layer1, threshold=40)
num_iterations = 9

results = np.zeros(shape=(layer2.spikes.shape[0],10))
permutation = np.random.permutation(len(mnist.square_data))[:1000]
with open('spiketimes.csv', 'w', newline='') as csvfile:
  writer = csv.writer(csvfile)

  # Generates spikes for layer 1 using 2 different filters
  for itr in range(len(permutation)):
    i = permutation[itr]
    layer1.raw_data = mnist.square_data[i]
    layer1.generate_spikes(OnCenterFilter, OffCenterFilter)
    li_index = []

    for j in range(num_iterations):
      layer1.wta(8,8)

      layer2.generate_spikes()
      layer2.STDP()

      for k in range(layer2.spikes.shape[0]):
        if (layer2.spikes[k] == 0):
          image_number = i
          spike_position = k
          spike_time = j
          writer.writerow([image_number, spike_position, spike_time])
          results[int(mnist.target[i]), k]+=1
          
  
      layer1.increment_time()
      layer2.increment_time()
    layer1.reset()
    layer2.reset()
    print(results)
    #print("\rComplete: ", i+1, end="")
