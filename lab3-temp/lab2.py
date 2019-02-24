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

layer1 = firstlayer.FirstLayer(layer_id=1, training_raw_data=mnist.square_data[0], threshold=8, inhibit_k=4)

layer2 = layer.Layer(layer_id=2, num_neurons=10, prev_layer=layer1, threshold=25)
num_iterations = 9

result = np.zeros((10,10))

perm = np.random.permutation(len(mnist.square_data))

with open('spiketimes.csv', 'w', newline='') as csvfile:
  writer = csv.writer(csvfile)
  mapping = np.arange(10)
  correct = np.zeros(100)
  # Generates spikes for layer 1 using 2 different filters
  for itr in range(len(mnist.square_data)):
    i = perm[itr]
    layer1.raw_data = mnist.square_data[i]
    layer1.generate_spikes(OnCenterFilter, OffCenterFilter)
    for j in range(num_iterations):
      layer2.generate_spikes()
      layer2.STDP()
      for k in range(layer2.spikes.shape[0]):
        if (layer2.spikes[k] == 0):
          image_number = i
          spike_position = k
          spike_time = j
          result[int(mnist.target[i]), k] += 1
          correct[itr % 100] = (mnist.target[itr] == mapping[k])
          writer.writerow([image_number, spike_position, spike_time])
      
      layer1.increment_time()
      layer2.increment_time()
    
    mapping = np.argmax(result, axis=0)

    layer2.reset()

    if (i % 100 == 0):
      print(layer2.W)
      print(result)
      print(np.sum(correct) / 100)
      pass
    print("\rComplete: ", i+1, end="")

