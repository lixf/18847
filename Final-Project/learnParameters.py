from keras.models import Sequential
from keras.layers import Dense, Activation

from keras import backend as K
import numpy as np

model = Sequential()
model.add(Dense(4, input_dim=4))
model.add(Activation('relu'))
model.add(Dense(2))
# For a mean squared error regression problem
model.compile(optimizer='rmsprop',
              loss='mse')

input_parameters = np.load('input_parameters.npy')
outputs = np.load('outputs.npy')

# Train the model, iterating on the data in batches of 32 samples
model.fit(input_parameters, outputs, epochs=500, batch_size=75)

output = model.layers[-1].output
loss = K.mean(output[:,0] * output[:,1]) + 10000 * K.mean(K.cast((model.input < 0), float)) + 10000 * K.mean(K.cast((model.input > 1), float))
grads = K.gradients(loss, model.input)[0]

grads = K.l2_normalize(grads)

func = K.function([model.input], [loss, grads])

input_temp = np.random.random((1, 4)) # define an initial random image

lr = .01  # learning rate used for gradient updates
max_iter = 1000  # number of gradient updates iterations
for i in range(max_iter):
    loss_val, grads_val = func([input_temp])
    input_temp += grads_val * lr  # update the image based on gradients
    print(loss_val)

print(input_temp)
new_array = np.array([[1,.1,.1,.1]])
print(model.predict(new_array))