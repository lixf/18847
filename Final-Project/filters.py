import numpy as np

# Returns a matrix where each cell is a sum of the surrounding cells
def sum_surrounds(data):
  sum = np.zeros(data.shape)

  # Matrix operations to shift data left, right, up, down, diag, etc
  sum = sum + np.pad(data,((0,1),(0,1)), mode='constant')[1:, 1:] # top left
  sum = sum + np.pad(data,((0,0),(0,1)), mode='constant')[:, 1:] # mid left
  sum = sum + np.pad(data,((1,0),(0,1)), mode='constant')[:-1, 1:] # bottom left
  sum = sum + np.pad(data,((1,0),(0,0)), mode='constant')[:-1, :] # bottom
  sum = sum + np.pad(data,((1,0),(1,0)), mode='constant')[:-1, :-1] # bottom right
  sum = sum + np.pad(data,((0,0),(1,0)), mode='constant')[:, :-1] # mid right
  sum = sum + np.pad(data,((0,1),(1,0)), mode='constant')[1:, :-1] # top right
  sum = sum + np.pad(data,((0,1),(0,0)), mode='constant')[1:, :] # top
  return sum

# Average of surround minus center
def OnCenterFilter(data):
  
  # Sum of the surround
  filtered_data = sum_surrounds(data)
  # Number of surrounding cells
  num_surroundings = sum_surrounds(np.full(data.shape,1))

  # Average value of surround
  filtered_data = filtered_data / num_surroundings
  filtered_data = np.round(filtered_data)

  return filtered_data  - data

# Sums the surrounding cells performs center - average of surround
def OffCenterFilter(data):

  # Sum of the surround
  filtered_data = sum_surrounds(data)
  # Number of surrounding cells
  num_surroundings = sum_surrounds(np.full(data.shape,1))

  # Average value of surround
  filtered_data = filtered_data / num_surroundings
  filtered_data = np.round(filtered_data)

  # Makes large difference result in early spike and small difference in late spike
  filtered_data = 8 - (data - filtered_data)

  # Sets value to -1 if no spike
  filtered_data = (filtered_data >= 8) * -1 + (filtered_data < 8) * filtered_data
  return filtered_data