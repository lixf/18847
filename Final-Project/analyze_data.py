import numpy as np
import matplotlib.pyplot as plt

results_array = np.load('results.out.npy')
def calculateThresholds():
  threshold_values = np.zeros((28, 50))
  
  for i in range(28):
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
      if (i >=4 and i < 12):
        j_index = int(j/20)
      elif (i >= 12):
        j_index = int(j/50)
    
      threshold_values[i, j_index] = j
  return threshold_values

thresholds = calculateThresholds()

best_overall_accuracy = np.zeros((28,2, 5))
results_array[results_array == -1] = 0

for i in range(28):

  for k in range(5):
    max = 0
    for j in range(50):
      overall_accuracy = results_array[i, j, k, 0] * results_array[i, j, k, 2]
      if (overall_accuracy > max):
        max = overall_accuracy
        best_overall_accuracy[i,0, k] = max
        best_overall_accuracy[i,1, k] = j


best_thresholds = np.zeros((28, 5))

for i in range(28):
  for k in range(5):
    best_thresholds[i, k] = thresholds[i, int(best_overall_accuracy[i, 1, k])]


plt.scatter(range(1,29), best_overall_accuracy[:, 0, 0], label='Unsupervised STDP')
plt.scatter(range(1,29), best_overall_accuracy[:, 0, 1], label='Forced STDP')
plt.scatter(range(1,29), best_overall_accuracy[:, 0, 2], label='Sorted STDP')
plt.scatter(range(1,29), best_overall_accuracy[:, 0, 3], label='RSTDP+Forced STDP')
plt.scatter(range(1,29), best_overall_accuracy[:, 0, 4], label='RSTDP')
plt.legend()
plt.ylabel('Overall Accuracy')
plt.xlabel('Receptive Field Length (px)')
plt.title('Best Overall Accuracy vs Receptive Field Length')
plt.show()

plt.scatter(range(1,29), best_thresholds[:, 0], label='Unsupervised STDP')
plt.scatter(range(1,29), best_thresholds[:, 1], label='Supervised STDP')
plt.scatter(range(1,29), best_thresholds[:, 2], label='Sorted STDP')
plt.scatter(range(1,29), best_thresholds[:, 3], label='RSTDP+Forced STDP')
plt.scatter(range(1,29), best_thresholds[:, 4], label='RSTDP')
plt.legend()
plt.ylabel('Threshold')
plt.xlabel('Receptive Field Length (px)')
plt.title('Best Threshold vs Receptive Field Length')
plt.show()

coverage_over_thresholds = np.zeros((50, 5))

for j in range(50):
  for k in range(5):
    coverage_over_thresholds[j, k] = results_array[27, j, k, 0]

coverage_indices1 = np.array(np.nonzero(coverage_over_thresholds[:,0] > 0), dtype=int).reshape(-1)
coverage_indices2 = np.array(np.nonzero(coverage_over_thresholds[:,1] > 0), dtype=int).reshape(-1)
coverage_indices3 = np.array(np.nonzero(coverage_over_thresholds[:,2] > 0), dtype=int).reshape(-1)
coverage_indices4 = np.array(np.nonzero(coverage_over_thresholds[:,3] > 0), dtype=int).reshape(-1)
coverage_indices5 = np.array(np.nonzero(coverage_over_thresholds[:,4] > 0), dtype=int).reshape(-1)


plt.scatter(thresholds[27,coverage_indices1], coverage_over_thresholds[coverage_indices1, 0], label='Unsupervised STDP')
plt.scatter(thresholds[27,coverage_indices2], coverage_over_thresholds[coverage_indices2, 1], label='Forced STDP')
plt.scatter(thresholds[27,coverage_indices3], coverage_over_thresholds[coverage_indices3, 2], label='Sorted STDP')
plt.scatter(thresholds[27,coverage_indices4], coverage_over_thresholds[coverage_indices4, 3], label='RSTDP+Forced STDP')
plt.scatter(thresholds[27,coverage_indices5], coverage_over_thresholds[coverage_indices5, 4], label='RSTDP')
plt.legend()

plt.xlabel('Threshold')
plt.ylabel('Coverage')
plt.title('Coverage vs Threshold for Receptive Field Length 28')

plt.show()

accuracy_over_thresholds = np.zeros((50, 5))

for j in range(50):
  for k in range(5):
    accuracy_over_thresholds[j, k] = results_array[27, j, k, 2]

accuracy_indices1 = np.array(np.nonzero(accuracy_over_thresholds[:,0] > 0), dtype=int).reshape(-1)
accuracy_indices2 = np.array(np.nonzero(accuracy_over_thresholds[:,1] > 0), dtype=int).reshape(-1)
accuracy_indices3 = np.array(np.nonzero(accuracy_over_thresholds[:,2] > 0), dtype=int).reshape(-1)
accuracy_indices4 = np.array(np.nonzero(accuracy_over_thresholds[:,3] > 0), dtype=int).reshape(-1)
accuracy_indices5 = np.array(np.nonzero(accuracy_over_thresholds[:,4] > 0), dtype=int).reshape(-1)

plt.scatter(thresholds[27,accuracy_indices1], accuracy_over_thresholds[accuracy_indices1, 0], label='Unsupervised STDP')
plt.scatter(thresholds[27,accuracy_indices2], accuracy_over_thresholds[accuracy_indices2, 1], label='Forced STDP')
plt.scatter(thresholds[27,accuracy_indices3], accuracy_over_thresholds[accuracy_indices3, 2], label='Sorted STDP')
plt.scatter(thresholds[27,accuracy_indices4], accuracy_over_thresholds[accuracy_indices4, 3], label='RSTDP+Forced STDP')
plt.scatter(thresholds[27,accuracy_indices5], accuracy_over_thresholds[accuracy_indices5, 4], label='RSTDP')

plt.legend()
plt.ylabel('Accuracy (over successfully classified data)')
plt.xlabel('Threshold')
plt.title('Accuracy vs Threshold for Receptive Field Length 28')
plt.show()

overall_accuracy_over_thresholds = np.zeros((50, 5))

for j in range(50):
  for k in range(5):
    overall_accuracy_over_thresholds[j, k] = results_array[27, j, k, 2] * results_array[27, j, k, 0]

overall_accuracy_indices1 = np.array(np.nonzero(overall_accuracy_over_thresholds[:,0] > 0), dtype=int).reshape(-1)
overall_accuracy_indices2 = np.array(np.nonzero(overall_accuracy_over_thresholds[:,1] > 0), dtype=int).reshape(-1)
overall_accuracy_indices3 = np.array(np.nonzero(overall_accuracy_over_thresholds[:,2] > 0), dtype=int).reshape(-1)
overall_accuracy_indices4 = np.array(np.nonzero(overall_accuracy_over_thresholds[:,3] > 0), dtype=int).reshape(-1)
overall_accuracy_indices5 = np.array(np.nonzero(overall_accuracy_over_thresholds[:,4] > 0), dtype=int).reshape(-1)

plt.scatter(thresholds[27,overall_accuracy_indices1], overall_accuracy_over_thresholds[overall_accuracy_indices1, 0], label='Unsupervised STDP')
plt.scatter(thresholds[27,overall_accuracy_indices2], overall_accuracy_over_thresholds[overall_accuracy_indices2, 1], label='Forced STDP')
plt.scatter(thresholds[27,overall_accuracy_indices3], overall_accuracy_over_thresholds[overall_accuracy_indices3, 2], label='Sorted STDP')
plt.scatter(thresholds[27,overall_accuracy_indices4], overall_accuracy_over_thresholds[overall_accuracy_indices4, 3], label='RSTDP+Forced STDP')
plt.scatter(thresholds[27,overall_accuracy_indices5], overall_accuracy_over_thresholds[overall_accuracy_indices5, 4], label='RSTDP')
plt.legend()
plt.ylabel('Overall Accuracy')
plt.xlabel('Threshold')
plt.title('Overall Accuracy vs Threshold for Receptive Field Length 28')

plt.show()

purities = []
accuracies = []
for i in range(28):
  for j in range(50):
    for k in range(5):
      if (k != 4 and k!= 3 and k!= 1):
        purities.append(results_array[i, j, k, 1])
        accuracies.append(results_array[i, j, k, 2])

plt.scatter(accuracies, purities, label='Purities vs Accuracies')
plt.plot(np.arange(0, 1, .1), np.arange(0, 1, .1), label='Expectation')

plt.legend()
plt.ylabel('Purity')
plt.xlabel('Accuracy')
plt.title('Purity vs Accuracy')
plt.show()