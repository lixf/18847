import numpy as np
import matplotlib.pyplot as plt
from sklearn.datasets import fetch_mldata
import firstlayer as firstlayer
import layer as layer
from filters import OffCenterFilter, OnCenterFilter
import csv
import time

def evaluate(layers, data, target, receptive_field, parameters=None, isTraining=True, assignments=None, isForced=False):
  training_results = np.zeros((layers[-1].num_neurons, 10))
  test_results = np.zeros((2,layers[-1].num_neurons))

  svm_inputs = []
  oldW = np.copy(layers[-1].W)
  for i in range(len(data)):
    layers[0].raw_data = data[i]
    layers[0].generate_spikes(OnCenterFilter, OffCenterFilter, receptive_field)
    neurons_spiked = np.full(layers[-1].spikes.shape, -1)
    #for each image go through all time steps

    found_answer = False
    for j in range(8):

      #feedforward inhibitionn with max 4 spikes
      #layer2.feedforward_inhibition(100, 8)

      for k in range(1,len(layers)):
        layers[k].generate_spikes()
        if (isTraining):
          if (isForced):
            for l in range(1,len(layers)):
              pass
              layers[l].supervised_rule(int(target[i]))
          else:
            layers[1].wta(25, 8)
            layers[2].wta(1, 8)

      if (isTraining):
        # result array is num_patterns x num_labels, where value is number of
        # occurrences

        for k in range(layers[-1].spikes.shape[0]):
          if (layers[-1].spikes[k] == 0):
            training_results[k, int(target[i])]+=1
            found_answer = True
      else:
        for k in range(layers[-1].spikes.shape[0]):
          if (layers[-1].spikes[k] == 0):
            test_results[0,k]+=1
            found_answer = True
            if (int(target[i]) == assignments[k]):
              test_results[1,int(target[i])]+=1
        neurons_spiked[(layers[-1].spikes == 0) & (neurons_spiked == -1)] = j
      for layer in layers:
        layer.increment_time()

    svm_inputs.append(neurons_spiked)
    if (isTraining):
      for k in range(1,len(layers)):
        layers[k].stdp_update_rule(parameters[k-1])
    for layer in layers:
      layer.reset()
    #print("\rComplete: ", itr+1, end="")

  assignments = np.argmax(training_results, axis=1)

  if (isTraining):
    training_results[training_results == 0] = .001
    return [training_results, assignments]
  else:
    test_results[0][test_results[0] == 0] = 1
    svm_inputs = np.array(svm_inputs)
    pre_svm_inputs = np.copy(svm_inputs)
    svm_inputs[svm_inputs == -1] = 8
    svm_inputs = svm_inputs - np.mean(svm_inputs, axis=0)
    svm_inputs = svm_inputs / (.001 + 2* np.std(svm_inputs, axis=0))
    return [test_results, svm_inputs, pre_svm_inputs]



def calculate_metrics(data, target, receptive_field_length, threshold, parameters=None, num_data=2000, isForced=False):

  # Structure of the TNN

  num_outputs = 128

  #threshold indicates the highest filter spiketime that can be condsidered
  layer1 = firstlayer.FirstLayer(layer_id=1, training_raw_data=data[0], threshold=8, receptive_field_length=receptive_field_length)
  receptive_field = (int(14-receptive_field_length/2),int(14-receptive_field_length/2))

  # threshold indicates the max neuron sum before firing
  layer2 = layer.Layer(layer_id=2, num_neurons=num_outputs, prev_layer=layer1, threshold=threshold[0], can_overlap=True, max_repeats=25)

  # threshold indicates the max neuron sum before firing
  layer3 = layer.Layer(layer_id=3, num_neurons=10, prev_layer=layer2, threshold=threshold[1], can_overlap=False, max_repeats=1)

  layers = [layer1, layer2, layer3]
  #layers = [layer1, layer2]
  # selects 10000 random images for training and testing
  permutation = np.random.permutation(len(data))
  training = permutation[int(num_data/2):num_data]
  test = permutation[:int(num_data/2)]
  
  # Generates spikes for layer 1 using 2 different filters
  # this is the testing phase

  training_results, assignments = evaluate(layers, data[training], target[training], receptive_field, parameters, True, None, isForced)
  print(assignments)
  distributions = np.zeros(10)
  for i in range(10):
    distributions[i] = np.sum(assignments == i) / len(assignments) * 1.0
  print(distributions)

  test_results, svm_inputs, pre_svm_inputs = evaluate(layers, data[training], target[training], receptive_field,parameters, False, assignments)

  from sklearn.svm import SVC
  
  print('SVM Classifier with gamma = 0.1; Kernel = Polynomial')
  classifier = SVC(gamma=0.1, kernel='poly', random_state = 0)
  classifier.fit(svm_inputs,target[training])
  from sklearn.metrics import accuracy_score
  test_results, svm_inputs, pre_svm_inputs = evaluate(layers, data[test], target[test], receptive_field,parameters, False, assignments)
  y_pred = classifier.predict(svm_inputs)

  print("SVM Accuracy score: ",accuracy_score(target[test], y_pred))
  print("Coverage: ", np.mean(np.sum(pre_svm_inputs != -1, axis=1) > 0))
  print("Neuron Coverage: ", np.mean(np.mean(pre_svm_inputs != -1, axis=1)))

  

  return [training_results, test_results, accuracy_score(target[test], y_pred)]


mnist = fetch_mldata('MNIST original')
N, _ = mnist.data.shape

# Reshape the data to be square
mnist.square_data = mnist.data.reshape(N,28,28)

best_results = np.array([1.340, .0622, .492, .386, 100])
best_accuracy = 0
input_output_weight = 1.340
input_no_output_weight = 0.0622
input_inhibited_output_weight = .492
no_input_output_weight = .386
input_output_weight2 = 1.2465
input_no_output_weight2 = .054
input_inhibited_output_weight2 = .5
no_input_output_weight2 = .37
parameters = [[input_output_weight, input_no_output_weight, input_inhibited_output_weight, no_input_output_weight],
              [input_output_weight2, input_no_output_weight2, input_inhibited_output_weight2, no_input_output_weight2]]
num_data = 4000

print("Receptive Field: ", 28)
thresholds = [210.7, 126.5]
print("Threshold: ", thresholds)
print("isForced", True)

training_results, test_results, svm_accuracy  = calculate_metrics(mnist.square_data, mnist.target, 28,thresholds, parameters, num_data,True)
coverage = np.sum(test_results[0]) / (num_data/2)
purity = np.mean(np.amax(training_results, axis=1) / np.sum(training_results, axis=1))
accuracy = np.mean(test_results[1] / test_results[0])
if (svm_accuracy > best_accuracy):
  best_accuracy = svm_accuracy
  best_results= [parameters[1][0], parameters[1][1], parameters[1][2], parameters[1][3], thresholds[1]]
print(best_results, best_accuracy)
#print("Coverage: ", coverage)
print("Purity: ", purity)
print("Accuracy: ", accuracy)

print("Receptive Field: ", 28)
print("Threshold: ", thresholds)
print("isForced", False)

training_results, test_results, svm_accuracy  = calculate_metrics(mnist.square_data, mnist.target, 28,thresholds, parameters, num_data,False)
coverage = np.sum(test_results[0]) / (num_data/2)
purity = np.mean(np.amax(training_results, axis=1) / np.sum(training_results, axis=1))
accuracy = np.mean(test_results[1] / test_results[0])
print("Coverage: ", coverage)
print("Purity: ", purity)
print("Accuracy: ", accuracy)