import numpy as np
import matplotlib.pyplot as plt
from sklearn.datasets import fetch_mldata
import firstlayer as firstlayer
import layer as layer
from filters import OffCenterFilter, OnCenterFilter

mnist = fetch_mldata('MNIST original')
N, _ = mnist.data.shape

# Reshape the data to be square
mnist.square_data = mnist.data.reshape(N,28,28)

layer1 = firstlayer.FirstLayer(layer_id=1, training_raw_data=mnist.square_data[0], threshold=8)

layer2 = layer.Layer(layer_id=2, num_neurons=10, prev_layer=layer1, threshold=3)
num_iterations = 9

# Generates spikes for layer 1 using 2 different filters
for i in range(len(mnist.square_data[:4])):
  layer1.raw_data = mnist.square_data[i]
  layer1.generate_spikes(OnCenterFilter, OffCenterFilter)
  for j in range(num_iterations):
    for k in range(layer1.spikes.shape[0]):
      if (layer1.spikes[k] == 0):
        pass
        #print(i, j, k)
    layer2.generate_spikes()
    for k in range(layer2.spikes.shape[0]):
      if (layer2.spikes[k] != -1):
        pass
        print(i, j, k)
  
    layer1.increment_time()
    layer2.increment_time()
    
  layer2.reset()