import warnings
warnings.filterwarnings('ignore') # suppress import warnings

import os
import cv2
import tflearn
import numpy as np
import tensorflow as tf
from random import shuffle
from tqdm import tqdm 
from tflearn.layers.conv import conv_2d, max_pool_2d
from tflearn.layers.core import input_data, dropout, fully_connected
from tflearn.layers.estimator import regression

''' <global actions> '''

TRAIN_DIR = 'D:/project/c9188----tree/diabetic practice/dataset/train1'
TEST_DIR = 'D:/project/c9188----tree/diabetic practice/dataset/test1'
IMG_SIZE = 50
LR = 1e-3
MODEL_NAME = 'diabeticEYE-{}-{}.model'.format(LR, '2conv-basic')
tf.logging.set_verbosity(tf.logging.ERROR) # suppress keep_dims warnings
os.environ['TF_CPP_MIN_LOG_LEVEL'] = '3' # suppress tensorflow gpu logs
tf.reset_default_graph()

''' </global actions> '''


def find_target_label(img_name):
    typ_lbl = img_name[0]
    ans = [0, 0, 0, 0]

    if int(typ_lbl) == 0:
        ans = [1, 0, 0, 0]
    elif int(typ_lbl) == 1:
        ans = [0, 1, 0, 0]
    elif int(typ_lbl) == 2:
        ans = [0, 0, 1, 0]
    elif int(typ_lbl) == 3:
        ans = [0, 0, 0, 1]
    return ans

def create_training_data():

    training_data = []

    for img in tqdm(os.listdir(TRAIN_DIR)):
        label = find_target_label(img)
        path = os.path.join(TRAIN_DIR, img)
        img = cv2.imread(path,cv2.IMREAD_COLOR)
        img = cv2.resize(img, (IMG_SIZE,IMG_SIZE))
        training_data.append([np.array(img),np.array(label)])

    shuffle(training_data)
    np.save('train_data.npy', training_data)

    return training_data

def main():

    train_data = create_training_data()

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


    #if os.path.exists('{}.meta'.format(MODEL_NAME)):
    #    model.load(MODEL_NAME)
    #    print('Model Loaded')

    train = train_data[-800:]
    test = train_data[-800:]

    X = np.array([i[0] for i in train]).reshape(-1,IMG_SIZE,IMG_SIZE,3)
    Y = [i[1] for i in train]

    test_x = np.array([i[0] for i in test]).reshape(-1,IMG_SIZE,IMG_SIZE,3)
    test_y = [i[1] for i in test]

    model_info = model.fit({'input': X}, {'targets': Y}, n_epoch=5, validation_set=({'input': test_x}, {'targets': test_y}), snapshot_step=40, show_metric=True, run_id=MODEL_NAME)

    print(model_info)
    model.save(MODEL_NAME)

    from sklearn.metrics import classification_report

    #####pred = model.predict(test_x)

    ####predicted = np.argmax(pred, axis=1)
    ##########report = classification_report(np.argmax(test_y, axis=1), predicted)
    ##########print(report)


##########################################################################################################################################
    predictions = model.predict(X)
    accuracy = 0
    for prediction, actual in zip(predictions, Y):
        predicted_class = np.argmax(prediction)
        actual_class = np.argmax(actual)
        if (predicted_class == actual_class):
            accuracy += 1

    accuracy = (accuracy / len(Y)) * 100

    A = "Training Accuracy is {0}".format(accuracy)

    predictions = model.predict(test_x)
    accuracy = 0
    for prediction, actual in zip(predictions, test_y):
        predicted_class = np.argmax(prediction)
        actual_class = np.argmax(actual)
        if (predicted_class == actual_class):
            accuracy += 1

    accuracy = (accuracy / len(test_y)) * 100

    B = "Testing Accuracy is {0}".format(accuracy)

    model.save(MODEL_NAME)

    msg = A + '\n' + B + '\n' + "Saved as " + MODEL_NAME

    #    print(msg)
    return msg

    # # plot model history after each epoch
    # from plt_graph import plot_model_history
    # plot_model_history(model_info)
    #
    # return Str
#if __name__ == '__main__':main()

#####################################################==========================================================
