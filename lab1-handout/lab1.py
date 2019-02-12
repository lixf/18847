import numpy as np
import matplotlib.pyplot as plt
from sklearn.datasets import fetch_mldata
import firstlayer as firstlayer

mnist = fetch_mldata('MNIST original')
N, _ = mnist.data.shape

# Reshape the data to be square
mnist.square_data = mnist.data.reshape(N,28,28)

layer1 = firstlayer.FirstLayer(1, mnist.square_data, mnist.target)

# 3. On Center Off Center Filtering
def off_center_filter(data):
    ret = np.zeros(data.shape)
    for n in range(len(data)):
    #for n in [40000]:
        pic = data[n]
        for x in range(1,27):
            for y in range(1,27):
                # Calculate average of surrounding
                s = pic[x-1][y-1] + pic[x-1][y] + pic[x-1][y+1] + \
                    pic[x][y-1] + pic[x][y+1] + \
                    pic[x+1][y-1] + pic[x+1][y] + pic[x+1][y+1]
                avg = s // 8
                s_max = max([pic[x-1][y-1], pic[x-1][y], pic[x-1][y+1],\
                            pic[x][y-1], pic[x][y], pic[x][y+1], \
                            pic[x+1][y-1], pic[x+1][y],pic[x+1][y+1]])
                off_center = s_max - avg - data[n][x][y]
                if off_center > 0 :
                    ret[n][x][y] = int(s_max - off_center)
                else :
                    ret[n][x][y] = 0
            #print('', end='\n')
    return ret

def on_center_filter(data):
    ret = np.zeros(data.shape)
    for n in range(len(data)):
    #for n in [40000]:
        pic = data[n]
        for x in range(1,27):
            for y in range(1,27):
                # Calculate average of surrounding
                s = pic[x-1][y-1] + pic[x-1][y] + pic[x-1][y+1] + \
                    pic[x][y-1] + pic[x][y+1] + \
                    pic[x+1][y-1] + pic[x+1][y] + pic[x+1][y+1]
                s_max = max([pic[x-1][y-1], pic[x-1][y], pic[x-1][y+1],\
                            pic[x][y-1], pic[x][y], pic[x][y+1], \
                            pic[x+1][y-1], pic[x+1][y],pic[x+1][y+1]])
                avg = s // 8
                on_center = data[n][x][y] - avg
                if on_center > 0 :
                    ret[n][x][y] = int(s_max - on_center)
                else :
                    ret[n][x][y] = 0
            #print('', end='\n')
    return ret

def intense_area_filter(data):
    ret = np.zeros(data.shape)
    for n in range(len(data)):
    #for n in [15000]:
        pic = data[n]
        for x in range(1,27):
            for y in range(1,27):
                # count number of pixels > 5
                count = 0
                for i in [-1, 0, 1]:
                    for j in [-1, 0, 1]:
                        if pic[x+i][y+j] > 5: 
                            count = count + 1
                if count > 5 :
                    ret[n][x][y] = pic[x][y]
                else :
                    ret[n][x][y] = 0
            #print('', end='\n')
    return ret

#layer1.preprocess(on_center_filter)
layer1.preprocess(off_center_filter)
#layer1.preprocess(intense_area_filter)

# 4. Visualize Your Outputs
# This is done in the firstlayer.py:dump_data() function  

# 5. Spiketimes: use threshold == 2 to filter out noise
# Also output into CSV format
layer1.generate_spikes(2)

fields = [(12,12), (12,13), (12,14),\
          (13,12), (13,13), (13,14),\
          (14,12), (14,13), (14,14)]

layer1.write_spiketimes("output2.csv", fields)

