
import warnings
warnings.filterwarnings('ignore') # suppress import warnings

import os
import sys
import cv2
import tflearn
import numpy as np
import tensorflow as tf
from tflearn.layers.conv import conv_2d, max_pool_2d
from tflearn.layers.core import input_data, dropout, fully_connected
from tflearn.layers.estimator import regression

''' <global actions> '''

IMG_SIZE = 50
LR = 1e-3
MODEL_NAME = 'diabeticEYE-{}-{}.model'.format(LR, '2conv-basic')
tf.logging.set_verbosity(tf.logging.ERROR) # suppress keep_dims warnings
os.environ['TF_CPP_MIN_LOG_LEVEL'] = '3' # suppress tensorflow gpu logs


''' </global actions> '''


def process_verify_data(filepath):

	verifying_data = []

	img_name = filepath.split('.')[0]
	img = cv2.imread(filepath, cv2.IMREAD_COLOR)
	img = cv2.resize(img, (IMG_SIZE, IMG_SIZE))
	verifying_data = [np.array(img), img_name]
	
	np.save('train_data.npy', verifying_data)
	
	return verifying_data

def analysis(filepath):

	verify_data = process_verify_data(filepath)


	tf.reset_default_graph()

	convnet = input_data(shape=[None, IMG_SIZE, IMG_SIZE, 3], name='input')
	
	convnet = conv_2d(convnet, 32, 3, activation='relu')
	convnet = max_pool_2d(convnet, 3)

	convnet = conv_2d(convnet, 64, 3, activation='relu')
	convnet = max_pool_2d(convnet, 3)

	convnet = conv_2d(convnet, 128, 3, activation='relu')
	convnet = max_pool_2d(convnet, 3)

	convnet = conv_2d(convnet, 32, 3, activation='relu')
	convnet = max_pool_2d(convnet, 3)

	convnet = conv_2d(convnet, 64, 3, activation='relu')
	convnet = max_pool_2d(convnet, 3)

	convnet = fully_connected(convnet, 1024, activation='relu')
	convnet = dropout(convnet, 0.8)
	
	convnet = fully_connected(convnet, 4, activation='softmax')
	convnet = regression(convnet, optimizer='adam', learning_rate=LR, loss='categorical_crossentropy', name='targets')

	model = tflearn.DNN(convnet, tensorboard_dir='log')
	"""
	if os.path.exists('{}.meta'.format(MODEL_NAME)):
		model.load(MODEL_NAME)
		print ('Model loaded successfully.')
	else:
		print ('Error: Create a model using tfModel.py first.')
	"""
	img_data, img_name = verify_data[0], verify_data[1]

	data = img_data.reshape(IMG_SIZE, IMG_SIZE, 3)

	model_out = model.predict([data])[0]
    
#    print(model_out)
#    
#    print(np.argmax(model_out))

	if np.argmax(model_out) == 0:
		str_label = 'NON-Diabetic EYE'
	elif np.argmax(model_out) == 1:
		str_label = 'Diabetic EYE Having  Basic stage'
	elif np.argmax(model_out) == 2:
		str_label = 'Diabetic EYE Having In Mediam stage'
	elif np.argmax(model_out) == 3:
		str_label = 'Diabetic EYE Having In High stage'

	return str_label
# def main(Fname):
#    
#	DName=analysis(Fname)
#    print(DName)
#    A = "Selected Image is '{0}'".format(DName)
#    return DName

# if __name__ == '__main__':
#    main()
