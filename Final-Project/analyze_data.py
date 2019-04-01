import numpy as np
import matplotlib.pyplot as plt

results_array = np.load('results.out.npy')

def calculateThresholds():
  threshold_values = np.zeros((28, 50))
  
  for i in range(28):
    range1 = range(10,int((i**2)*10*.75), 5)
    range2 = range(20, int((i**2)*10*.75), 20)
    range3 = range(100, min(int((i**2)*10*.75), 1200), 50)

    selected_range = range1
    if (i >= 4 and i < 8):
      selected_range = range2
    elif (i >=8):
      selected_range = range3

    for j in selected_range:
      j_index = int((j - 10)/5)
      if (i >=4 and i < 8):
        j_index = int((j - 20)/20)
      elif (i >= 8):
        j_index = int((j-100)/50)
    
      threshold_values[i, j_index] = j
  return threshold_values

thresholds = calculateThresholds()

best_overall_accuracy = np.zeros((28,2, 2))
results_array[results_array == -1] = 0

for i in range(28):
  max = 0
  for j in range(50):
    overall_accuracy = results_array[i, j, 0, 0] * results_array[i, j, 0, 2]
    if (overall_accuracy > max):
      max = overall_accuracy
      best_overall_accuracy[i,0, 0] = max
      best_overall_accuracy[i,1, 0] = j


  max = 0
  for j in range(50):
    overall_accuracy = results_array[i, j, 1, 0] * results_array[i, j, 1, 2]
    if (overall_accuracy > max):
      max = overall_accuracy
      best_overall_accuracy[i,0, 1] = max
      best_overall_accuracy[i,1, 1] = j


best_thresholds = np.zeros((28, 2))

for i in range(28):
  best_thresholds[i, 0] = thresholds[i, int(best_overall_accuracy[i, 1, 0])]
  best_thresholds[i, 1] = thresholds[i, int(best_overall_accuracy[i, 1, 1])]

#print(best_thresholds)

plt.plot(range(28), best_overall_accuracy[:, 0, 0], label='Supervised STDP')
plt.plot(range(28), best_overall_accuracy[:, 0, 1], label='Unsupervised STDP')
plt.legend()

plt.show()

coverage_over_thresholds = np.zeros((50, 2))

for j in range(50):
  coverage_over_thresholds[j, 0] = results_array[18, j, 0, 0]
  coverage_over_thresholds[j, 1] = results_array[18, j, 1, 0]

coverage_indices1 = np.array(np.nonzero(coverage_over_thresholds[:,0] > 0), dtype=int).reshape(-1)
coverage_indices2 = np.array(np.nonzero(coverage_over_thresholds[:,1] > 0), dtype=int).reshape(-1)


plt.plot(thresholds[18,coverage_indices1], coverage_over_thresholds[coverage_indices1, 0], label='Supervised STDP')
plt.plot(thresholds[18,coverage_indices2], coverage_over_thresholds[coverage_indices2, 1], label='Unsupervised STDP')
plt.legend()
plt.show()

accuracy_over_thresholds = np.zeros((50, 2))

for j in range(50):
  accuracy_over_thresholds[j, 0] = results_array[18, j, 0, 2]
  accuracy_over_thresholds[j, 1] = results_array[18, j, 1, 2]

accuracy_indices1 = np.array(np.nonzero(accuracy_over_thresholds[:,0] > 0), dtype=int).reshape(-1)
accuracy_indices2 = np.array(np.nonzero(accuracy_over_thresholds[:,1] > 0), dtype=int).reshape(-1)


plt.plot(thresholds[18,accuracy_indices1], accuracy_over_thresholds[accuracy_indices1, 0], label='Supervised STDP')
plt.plot(thresholds[18,accuracy_indices2], accuracy_over_thresholds[accuracy_indices2, 1], label='Unsupervised STDP')
plt.legend()
plt.show()

overall_accuracy_over_thresholds = np.zeros((50, 2))

for j in range(50):
  overall_accuracy_over_thresholds[j, 0] = results_array[18, j, 0, 2] * results_array[18, j, 0, 0]
  overall_accuracy_over_thresholds[j, 1] = results_array[18, j, 1, 2] * results_array[18, j, 1, 0]

overall_accuracy_indices1 = np.array(np.nonzero(overall_accuracy_over_thresholds[:,0] > 0), dtype=int).reshape(-1)
overall_accuracy_indices2 = np.array(np.nonzero(overall_accuracy_over_thresholds[:,1] > 0), dtype=int).reshape(-1)


plt.plot(thresholds[18,overall_accuracy_indices1], overall_accuracy_over_thresholds[overall_accuracy_indices1, 0], label='Supervised STDP')
plt.plot(thresholds[18,overall_accuracy_indices2], overall_accuracy_over_thresholds[overall_accuracy_indices2, 1], label='Unsupervised STDP')
plt.legend()
plt.show()

purities = []
accuracies = []
for i in range(28):
  for j in range(50):
    purities.append(results_array[i, j, 0, 1])
    accuracies.append(results_array[i, j, 0, 2])

plt.scatter(accuracies, purities, label='Puritys vs Accuracies')
plt.plot(np.arange(0, 1, .1), np.arange(0, 1, .1), label='Expectation')

plt.legend()
plt.show()