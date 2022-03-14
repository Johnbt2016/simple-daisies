import numpy as np
import tensorflow as tf
from tensorflow import keras
import concurrent.futures


##################################################################################################
def transform(X, A, B, gradient, intercept):
	'''
	X is the vector passed by the user.
	R is the vector to be passed to the neural network.
	A and B are matrices. gradient and intercept are vectors.

	Solve the following system with unknown R:
	A.X = [diag(B.X + gradient)].R + intercept
	'''

	# try:
	return (np.diag(1. / (B.dot(X) + gradient))).dot((A.dot(X) - intercept))
	# except:
	# 	return np.nan * np.ones(B.shape[0])

##################################################################################################
def group_transform(largeX, A, B, gradient, intercept):
	return [transform(X, A, B, gradient, intercept) for X in largeX]

##################################################################################################
def split_data_array(data_array, batches):
	nb_samples = data_array.shape[0]
	lim = int(nb_samples / batches)

	largeX_list = [data_array[i*lim:(i+1)*lim] for i in range(batches-1)]
	largeX_list.append(data_array[(batches-1)*lim:nb_samples])

	return largeX_list

##################################################################################################
def prepare_vector(A, B, gradient, intercept, data_array):


	batches = 1
	data_array = data_array.T

	if batches < 4:
		final = np.vstack([transform(a, A, B, gradient, intercept) for a in data_array])
	else:
		largeX_list = split_data_array(data_array, batches)

		executor = concurrent.futures.ProcessPoolExecutor(10)
		result = [executor.submit(group_transform, largeX, A, B, gradient, intercept) for largeX in largeX_list]
		concurrent.futures.wait(result)

		final = np.vstack([list(r.result()) for r in list(result)])
	print(final.shape)

	final[final < 0.] = 0.
	final[final > 1.] = 1.


	return final

##################################################################################################
def predict(input, model):

	batch_size = 300000
	prediction = model.predict(input, verbose=1, batch_size=batch_size)

	return prediction



##################################################################################################
class NN:
	def __init__(self, model, out_property_name, out_property_unit):
		self.model = keras.models.load_model(model, compile=False)
		self.out_property_name = out_property_name
		self.out_property_unit = out_property_unit

##################################################################################################
def compute(A, B, gradient, intercept, mat_model, temp_model, data_array):
	input_vectors = prepare_vector(A, B, gradient, intercept, data_array = data_array)
	temperature = predict(input_vectors, temp_model.model)
	maturity = predict(input_vectors, mat_model.model)

	return temperature, maturity