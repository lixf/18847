import numpy as np
import matplotlib.pyplot as plt
from sklearn.datasets import fetch_mldata
import firstlayer as firstlayer
import layer as layer
from filters import OffCenterFilter, OnCenterFilter
import csv

mnist = fetch_mldata('MNIST original')
N, _ = mnist.data.shape

# Reshape the data to be square
mnist.square_data = mnist.data.reshape(N,28,28)

layer1 = firstlayer.FirstLayer(layer_id=1, training_raw_data=mnist.square_data[0], threshold=8, inhibit_k=3)

layer2 = layer.Layer(layer_id=2, num_neurons=10, prev_layer=layer1, threshold=3)
num_iterations = 9


with open('spiketimes.csv', 'w', newline='') as csvfile:
  writer = csv.writer(csvfile)

  # Generates spikes for layer 1 using 2 different filters
  for i in range(len(mnist.square_data)):
    layer1.raw_data = mnist.square_data[i]
    layer1.generate_spikes(OnCenterFilter, OffCenterFilter)
    for j in range(num_iterations):
      layer2.generate_spikes()
      for k in range(layer2.spikes.shape[0]):
        if (layer2.spikes[k] == 0):
          image_number = i
          spike_position = k
          spike_time = j
          writer.writerow([image_number, spike_position, spike_time])
  
      layer1.increment_time()
      layer2.increment_time()
    
    layer2.reset()
    print("\rComplete: ", i+1, end="")

