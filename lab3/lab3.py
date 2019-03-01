import numpy as np
import matplotlib.pyplot as plt
from sklearn.datasets import fetch_mldata
import firstlayer as firstlayer
import layer as layer
from filters import OffCenterFilter, OnCenterFilter
import csv
import time


def calculate_metrics(data, target, receptive_field):
  # Structure of the TNN
  layer1 = firstlayer.FirstLayer(layer_id=1, training_raw_data=data[0], threshold=8)
  layer2 = layer.Layer(layer_id=2, num_neurons=16, prev_layer=layer1, threshold=15)

  num_iterations = 9
  results = np.zeros(shape=(16, 10))
  permutation = np.random.permutation(len(data))
  training = permutation[:10000]
  test = permutation[10000:20000]
  
  start_time = time.time()
  # Generates spikes for layer 1 using 2 different filters
  # this is the testing phase
  for itr in range(len(training)):
    i = permutation[itr]
    layer1.raw_data = data[i]
    layer1.generate_spikes(OnCenterFilter, OffCenterFilter, receptive_field)
  
    for j in range(num_iterations):
      layer1.feedforward_inhibition(3)
  
      layer2.generate_spikes()
      layer2.wta(1, 8)
      layer2.stdp_update_rule()             
      layer1.increment_time()
      layer2.increment_time()
    layer1.reset()
    layer2.reset()
    print("\rComplete: ", itr+1, end="")

  end_time = time.time()
  print("Training time: ", end_time - start_time, "s");

  start_time = time.time()
  for itr in range(len(test)):
    i = permutation[itr]
    layer1.raw_data = data[i]
    layer1.generate_spikes(OnCenterFilter, OffCenterFilter, receptive_field)
  
    for j in range(num_iterations):
      layer1.feedforward_inhibition(3)
  
      layer2.generate_spikes()
      layer2.wta(1, 8)
  
      for k in range(layer2.spikes.shape[0]):
        if (layer2.spikes[k] == 0):
          image_number = i
          spike_position = k
          spike_time = j
          results[k, int(target[i])]+=1
             
      layer1.increment_time()
      layer2.increment_time()
    layer1.reset()
    layer2.reset()
    print("\rComplete: ", itr+1, end="")

  end_time = time.time()
  print("Test time: ", end_time - start_time, "s");
  return results;


mnist = fetch_mldata('MNIST original')
N, _ = mnist.data.shape

# Reshape the data to be square
mnist.square_data = mnist.data.reshape(N,28,28)

print("Receptive Field: (4,4)")
results1 = calculate_metrics(mnist.square_data, mnist.target, (4, 4))
max1 = np.transpose(np.asarray([np.amax(results1, axis=1)]))
totals1 = np.transpose(np.asarray([np.sum(results1, axis=1)]))
coverage1 = np.transpose(np.asarray([np.sum(results1, axis=1) / 10000]))
purity1 = np.transpose(np.asarray([np.amax(results1, axis=1) / np.sum(results1, axis=1)]))
final_results1 = np.concatenate((results1, max1, totals1, coverage1, purity1), axis=1)
np.savetxt("results1.csv", final_results1, delimiter=",")

print("Receptive Field: (12,12)")
results2 = calculate_metrics(mnist.square_data, mnist.target, (12,12))
max2 = np.transpose(np.asarray([np.amax(results2, axis=1)]))
totals2 = np.transpose(np.asarray([np.sum(results2, axis=1)]))
coverage2 = np.transpose(np.asarray([np.sum(results2, axis=1) / 10000]))
purity2 = np.transpose(np.asarray([np.amax(results2, axis=1) / np.sum(results2, axis=1)]))
final_results2 = np.concatenate((results2, max2, totals2, coverage2, purity2), axis=1)
np.savetxt("results2.csv", final_results2, delimiter=",")

print("Receptive Field: (12,16)")
results3 = calculate_metrics(mnist.square_data, mnist.target, (12,16))
max3 = np.transpose(np.asarray([np.amax(results3, axis=1)]))
totals3 = np.transpose(np.asarray([np.sum(results3, axis=1)]))
coverage3 = np.transpose(np.asarray([np.sum(results3, axis=1) / 10000]))
purity3 = np.transpose(np.asarray([np.amax(results3, axis=1) / np.sum(results3, axis=1)]))
final_results3 = np.concatenate((results3,max3, totals3, coverage3, purity3), axis=1)
np.savetxt("results3.csv", final_results3, delimiter=",")