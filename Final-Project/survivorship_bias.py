import numpy as np
import matplotlib.pyplot as plt
from sklearn.datasets import fetch_mldata
import firstlayer as firstlayer
import layer as layer
from filters import OffCenterFilter, OnCenterFilter
import csv
import time

results_array = np.zeros(shape=(10,10))

for i in range(2000):
  random_num = np.random.randint(0, 100)
  i_idx = int(random_num / 10)
  j_idx = int(random_num % 10)

  results_array[i_idx, j_idx] += 1

purity = np.amax(results_array, axis=1) / np.sum(results_array, axis=1)

print("Purities for each neuron: ", purity)
print("Average Purity: ", np.mean(purity))