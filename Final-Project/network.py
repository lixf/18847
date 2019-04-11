import numpy as np
import matplotlib.pyplot as plt
from sklearn.datasets import fetch_mldata
import firstlayer as firstlayer
import layer as layer
from filters import OffCenterFilter, OnCenterFilter
import csv
import time

weights_array1 = np.zeros((4, 10, 28, 28))
weights_array2 = np.zeros((4, 10, 28, 28))

def evaluate(layer1, layer2, data, target, receptive_field, parameters=None, isTraining=True, assignments=None, isForced=False):
  training_results = np.zeros((10, 10))
  test_results = np.zeros((2,10))

  for i in range(len(data)):
    if (~isForced):
      if (i % 1000 == 0):
        weights_array1[int(i / 1000)] = layer2.W[:784, :].transpose().reshape((10,28,28))

      if (i == 3000):
        np.save('weights_array3', weights_array1)
    if (isForced):
      if (i % 1000 == 0):
        weights_array2[int(i / 1000)] = layer2.W[:784, :].transpose().reshape((10,28,28))

      if (i == 3000):
        np.save('weights_array4', weights_array2)
    layer1.raw_data = data[i]
    layer1.generate_spikes(OnCenterFilter, OffCenterFilter, receptive_field)

    #print(i)
    #for each image go through all time steps

    found_answer = False
    for j in range(8):

      #feedforward inhibitionn with max 4 spikes
      #layer1.feedforward_inhibition(16)

      layer2.generate_spikes()

      # only select one of the 8 spikes
      if (isForced):
        for k in range(len(layer2.spikes)):
          if (k != target[i]):
            layer2.spikes[k] = -1
      else:
        layer2.wta(1, 8)


      if (isTraining):
        # result array is num_patterns x num_labels, where value is number of
        # occurrences


        for k in range(layer2.spikes.shape[0]):
          if (layer2.spikes[k] == 0):
            training_results[k, int(target[i])]+=1
            found_answer = True
        layer2.stdp_update_rule(parameters)

      else:
        for k in range(layer2.spikes.shape[0]):
          if (layer2.spikes[k] == 0):
            test_results[0,k]+=1
            found_answer = True
            if (int(target[i]) == assignments[k]):
              test_results[1,k]+=1
      if (found_answer):
        break
      layer1.increment_time()
      layer2.increment_time()


    layer1.reset()
    layer2.reset()
    #print("\rComplete: ", itr+1, end="")

  assignments = np.argmax(training_results, axis=1)

  if (isTraining):
    training_results[training_results == 0] = .001
    return [training_results, assignments]
  else:
    test_results[0][test_results[0] == 0] = 1
    return test_results


def calculate_metrics(data, target, receptive_field_length, threshold, parameters=None, num_data=2000, isForced=False):

  # Structure of the TNN

  num_outputs = 10

  #threshold indicates the highest filter spiketime that can be condsidered
  layer1 = firstlayer.FirstLayer(layer_id=1, training_raw_data=data[0], threshold=8, receptive_field_length=receptive_field_length)
  receptive_field = (int(14-receptive_field_length/2),int(14-receptive_field_length/2))

  # threshold indicates the max neuron sum before firing
  layer2 = layer.Layer(layer_id=2, num_neurons=num_outputs, prev_layer=layer1, threshold=threshold)
  layer2.W = np.random.random(layer2.W.shape) * 10

  # selects 10000 random images for training and testing
  permutation = np.random.permutation(len(data))
  training = permutation[int(num_data/2):num_data]
  test = permutation[:int(num_data/2)]
  
  # Generates spikes for layer 1 using 2 different filters
  # this is the testing phase

  training_results, assignments = evaluate(layer1, layer2, data[training], target[training], receptive_field, parameters, True, None, isForced)
  print(assignments)
  test_results = evaluate(layer1, layer2, data[test], target[test], receptive_field,parameters, False, assignments)
  return [training_results, test_results]


mnist = fetch_mldata('MNIST original')
N, _ = mnist.data.shape

# Reshape the data to be square
mnist.square_data = mnist.data.reshape(N,28,28)

def runExperiments():
  results_array = np.load('results.out.npy')
  for i in range(0,28):

    range1 = range(0,300, 10)
    range2 = range(0, 500, 20)
    range3 = range(0, 1200, 50)
    selected_range = range1
    if (i >= 4 and i < 12):
      selected_range = range2
    elif (i >=12):
      selected_range = range3

    for j in selected_range:
      j_index = int(j /10)
      if (i >=4 and i < 8):
        j_index = int(j/20)
      elif (i >= 8):
        j_index = int(j/50)

      coverage = 0
      low_coverage = False
      for k in range(2):
        print("Receptive Field: ", i)
        print("Threshold: ", j)
        print("J_index: ", j_index)
        print("isForced", k == 0)
        input_output_weight = 1
        input_no_output_weight = .05
        no_input_output_weight = 1
        input_inhibited_output_weight = 1
        parameters = [input_output_weight, input_no_output_weight, input_inhibited_output_weight, no_input_output_weight]
        num_data = 4000
        training_results, test_results  = calculate_metrics(mnist.square_data, mnist.target, i+1,j, parameters, num_data,k == 0)
        coverage = np.sum(test_results[0]) / (num_data/2)
        purity = np.mean(np.amax(training_results, axis=1) / np.sum(training_results, axis=1))
        accuracy = np.mean(test_results[1] / test_results[0])
        print("Coverage: ", coverage)
        print("Purity: ", purity)
        print("Accuracy: ", accuracy)
        results_array[i, j_index, k, 0] = coverage
        results_array[i, j_index, k, 1] = purity
        results_array[i, j_index, k, 2] = accuracy
        if (coverage < 0.05):
          low_coverage = True
        np.save('results.out', results_array)
      if low_coverage:
        break

input_output_weight = 1
input_no_output_weight = .05
no_input_output_weight = 1
input_inhibited_output_weight = 1
parameters = [input_output_weight, input_no_output_weight, input_inhibited_output_weight, no_input_output_weight]
num_data = 20000

print("Receptive Field: ", 28)
print("Threshold: ", 300)
print("isForced", True)

training_results, test_results  = calculate_metrics(mnist.square_data, mnist.target, 28,300, parameters, num_data,True)
coverage = np.sum(test_results[0]) / (num_data/2)
purity = np.mean(np.amax(training_results, axis=1) / np.sum(training_results, axis=1))
accuracy = np.mean(test_results[1] / test_results[0])
print("Coverage: ", coverage)
print("Purity: ", purity)
print("Accuracy: ", accuracy)

print("Receptive Field: ", 28)
print("Threshold: ", 300)
print("isForced", True)

training_results, test_results  = calculate_metrics(mnist.square_data, mnist.target, 28,300, parameters, num_data,False)
coverage = np.sum(test_results[0]) / (num_data/2)
purity = np.mean(np.amax(training_results, axis=1) / np.sum(training_results, axis=1))
accuracy = np.mean(test_results[1] / test_results[0])
print("Coverage: ", coverage)
print("Purity: ", purity)
print("Accuracy: ", accuracy)