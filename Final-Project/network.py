import numpy as np
import matplotlib.pyplot as plt
from sklearn.datasets import fetch_mldata
import firstlayer as firstlayer
import layer as layer
from filters import OffCenterFilter, OnCenterFilter
import csv
import time

import pdb
fig=plt.figure(figsize=(8, 4))



def evaluate(in_layer, hidden_layers, data, target, receptive_field, parameters=None, isTraining=True, assignments=None, isForced=False, isRSTDP=False):
  training_results = np.zeros((10, 10))
  test_results = np.zeros((2,10))
  #imshows = []
  #for num1 in range(2):
  #  list_imshow = []
  #  for num2 in range(10):
  #    fig.add_subplot(2, 10, num1 * 10 + num2 + 1)
  #    list_imshow.append(plt.imshow((hidden_layers[0].W[:784,0]).reshape((28,28)), cmap='hot', interpolation='nearest'))
  #  imshows.append(list_imshow)
  #plt.show(block=False)

  for i in range(len(data)):
    in_layer.raw_data = data[i]
    in_layer.generate_spikes(OnCenterFilter, OffCenterFilter, receptive_field)



    #if (i % 50 == 0 and isTraining):
    #  for s in range(10):
    #    imshows[0][s].set_data((hidden_layers[0].W[:784,s]).reshape((28,28)))
    #    imshows[1][s].set_data((hidden_layers[0].W[784:,s]).reshape((28,28)))
    #  plt.draw()
    #  plt.pause(.00001)  
    found_answer = False
    for layer in hidden_layers:

      for j in range(8):

        layer.generate_spikes()

        # only select one of the 8 spikes
        layer.wta(1, 8)
        if (isForced):
          for k in range(len(layer.spikes)):
            if (k != target[i]):
              layer.spikes[k] = -1

        if (isTraining):
          # result array is num_patterns x num_labels, where value is number of
          # occurrences

          for k in range(layer.spikes.shape[0]):
            if (layer.spikes[k] == 0):
              training_results[k, int(target[i])]+=1
              found_answer = True
              #layer.stdp_update_rule(parameters, isRSTDP, target[i])

        else:
          for k in range(layer.spikes.shape[0]):
            if (layer.spikes[k] == 0):
              test_results[0,k]+=1
              found_answer = True
              if (int(target[i]) == assignments[k]):
                test_results[1,k]+=1
        if (found_answer):
          break
        in_layer.increment_time()
        layer.increment_time()
      
      if (isTraining):
        layer.stdp_update_rule(parameters, isRSTDP, target[i])

      in_layer.reset()
      layer.reset()
      #print("\rComplete: ", itr+1, end="")

  #pdb.set_trace()
  assignments = np.argmax(training_results, axis=1)

  if (isTraining):
    training_results[training_results == 0] = .001
    return [training_results, assignments]
  else:
    test_results[0][test_results[0] == 0] = 1
    return test_results


def calculate_metrics(data, target, receptive_field_length, threshold, parameters=None, num_data=2000, isForced=False, isSorted=False, isRSTDP=False):

  # Structure of the TNN

  num_outputs = 10

  #threshold indicates the highest filter spiketime that can be condsidered
  layer1 = firstlayer.FirstLayer(layer_id=1, training_raw_data=data[0], threshold=8, receptive_field_length=receptive_field_length)
  receptive_field = (int(14-receptive_field_length/2),int(14-receptive_field_length/2))

  # threshold indicates the max neuron sum before firing
  layer2 = layer.Layer(layer_id=2, num_neurons=num_outputs, prev_layer=layer1, threshold=threshold)
  #layer3 = layer.Layer(layer_id=3, num_neurons=num_outputs, prev_layer=layer2, threshold=threshold)
  #layer4 = layer.Layer(layer_id=4, num_neurons=num_outputs, prev_layer=layer3, threshold=threshold)
  #layer5 = layer.Layer(layer_id=5, num_neurons=num_outputs, prev_layer=layer4, threshold=threshold)

  hidden_layers = []
  hidden_layers.append(layer2)
  #hidden_layers.append(layer3)
  #hidden_layers.append(layer4)
  #hidden_layers.append(layer5)

  # selects 10000 random images for training and testing
  permutation = np.random.permutation(len(data))
  training = permutation[int(num_data/2):num_data]
  test = permutation[:int(num_data/2)]

  if isSorted:
      training = np.sort(training)
  
  # Generates spikes for layer 1 using 2 different filters
  # this is the testing phase
  #pdb.set_trace()

  training_results, assignments = evaluate(layer1, hidden_layers, data[training], target[training], receptive_field, parameters, True, None, isForced, isRSTDP)
  print(assignments)

  test_results = evaluate(layer1, hidden_layers, data[test], target[test], receptive_field,parameters, False, assignments)
  return [training_results, test_results]


mnist = fetch_mldata('MNIST original')
N, _ = mnist.data.shape

# Reshape the data to be square
mnist.square_data = mnist.data.reshape(N,28,28)
#pdb.set_trace()

def runExperiments():
  results_array = np.load('results.out.npy')
  #results_array = np.zeros((28, 50, 5, 3))

  for i in range(12,28):

    range1 = range(0,300, 10)
    range2 = range(0, 500, 20)
    range3 = range(0, 1200, 50)
    selected_range = range1
    if (i >= 4 and i < 12):
      selected_range = range2
    elif (i >=12):
      selected_range = range3
    
    low_coverage_array = np.full((5), False)
    for j in selected_range:
      j_index = int(j /10)
      if (i >=4 and i < 12):
        j_index = int(j/20)
      elif (i >= 12):
        j_index = int(j/50)

      coverage = 0
      low_coverage = True

      for k in range(5):
        if (low_coverage_array[k] == True):
          continue
        isForced = False
        isSorted = False
        isRSTDP = False

        if (k == 1):
          isForced = True
        elif (k == 2):
          isSorted = True
        elif (k == 3):
          isForced = True
          isRSTDP = True
        elif (k == 4):
          isRSTDP = True

        print("Receptive Field: ", i)
        print("Threshold: ", j)
        print("J_index: ", j_index)
        print("isForced", isForced)
        print("isSorted", isSorted)
        print("isRSTDP", isRSTDP)

        input_output_weight = 1
        input_no_output_weight = .05
        no_input_output_weight = 1
        input_inhibited_output_weight = 1
        parameters = [input_output_weight, input_no_output_weight, input_inhibited_output_weight, no_input_output_weight]
        num_data = 10000
        training_results, test_results  = calculate_metrics(mnist.square_data, mnist.target, i+1,j, parameters, num_data, isForced, isSorted, isRSTDP)
        coverage = np.sum(test_results[0]) / (num_data/2)
        purity = np.mean(np.amax(training_results, axis=1) / np.sum(training_results, axis=1))
        accuracy = np.mean(test_results[1] / test_results[0])
        print("Coverage: ", coverage)
        print("Purity: ", purity)
        print("Accuracy: ", accuracy)
        results_array[i, j_index, k, 0] = coverage
        results_array[i, j_index, k, 1] = purity
        results_array[i, j_index, k, 2] = accuracy
        if (coverage >= 0.05):
          low_coverage = False
        else:
          low_coverage_array[k] = True
        np.save('results.out', results_array)
      if low_coverage:
        break


runExperiments()
input_output_weight = 1
input_no_output_weight = .05
no_input_output_weight = 1
input_inhibited_output_weight = 1
parameters = [input_output_weight, input_no_output_weight, input_inhibited_output_weight, no_input_output_weight]
num_data = 20000

# Configs
isForced = True
isSorted = False
isRSTDP = False

print("Receptive Field: ", 28)
print("Threshold: ", 300)
print("isForced", isForced)
print("isSorted", isSorted)
print("isRSTDP", isRSTDP)

training_results, test_results  = calculate_metrics(mnist.square_data, mnist.target, 28,300, parameters, num_data, isForced, isSorted)
coverage = np.sum(test_results[0]) / (num_data/2)
purity = np.mean(np.amax(training_results, axis=1) / np.sum(training_results, axis=1))
accuracy = np.mean(test_results[1] / test_results[0])
print("Coverage: ", coverage)
print("Purity: ", purity)
print("Accuracy: ", accuracy)
print("#" * 20)

isForced = False
isSorted = False
isRSTDP = True
print("Receptive Field: ", 28)
print("Threshold: ", 300)
print("isForced", isForced)
print("isSorted", isSorted)
print("isRSTDP", isRSTDP)

training_results, test_results  = calculate_metrics(mnist.square_data, mnist.target, 28,300, parameters, num_data, isForced, isSorted)
coverage = np.sum(test_results[0]) / (num_data/2)
purity = np.mean(np.amax(training_results, axis=1) / np.sum(training_results, axis=1))
accuracy = np.mean(test_results[1] / test_results[0])
print("Coverage: ", coverage)
print("Purity: ", purity)
print("Accuracy: ", accuracy)
print("#" * 20)

isForced = True
isSorted = False
isRSTDP = True
print("Receptive Field: ", 28)
print("Threshold: ", 300)
print("isForced", isForced)
print("isSorted", isSorted)
print("isRSTDP", isRSTDP)

training_results, test_results  = calculate_metrics(mnist.square_data, mnist.target, 28,300, parameters, num_data, isForced, isSorted, isRSTDP)
coverage = np.sum(test_results[0]) / (num_data/2)
purity = np.mean(np.amax(training_results, axis=1) / np.sum(training_results, axis=1))
accuracy = np.mean(test_results[1] / test_results[0])
print("Coverage: ", coverage)
print("Purity: ", purity)
print("Accuracy: ", accuracy)
print("#" * 20)

isForced = False
isSorted = False
isRSTDP = False
print("Receptive Field: ", 28)
print("Threshold: ", 300)
print("isForced", isForced)
print("isSorted", isSorted)
print("isRSTDP", isRSTDP)

training_results, test_results  = calculate_metrics(mnist.square_data, mnist.target, 28,300, parameters, num_data, False)
coverage = np.sum(test_results[0]) / (num_data/2)
purity = np.mean(np.amax(training_results, axis=1) / np.sum(training_results, axis=1))
accuracy = np.mean(test_results[1] / test_results[0])
print("Coverage: ", coverage)
print("Purity: ", purity)
print("Accuracy: ", accuracy)



