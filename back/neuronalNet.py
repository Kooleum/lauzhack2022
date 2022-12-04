import tensorflow as tf
import numpy as np
import matplotlib.pyplot as plt
import os, os.path
import json

words = os.listdir('datas')

NB_FRAME_PER_WORD = 30
NB_BODY_POINTS = 11
NB_DIMS = 3

# text file to python array
def file_to_array(path):
    array = []
    with open(path) as f:
        for line in f:
            array=json.loads(line)
            
    return array

def get_prediction_result(tensor):
    max_value = 0
    index = 0
    for i in range(len(tensor)):
        if(tensor[i]) > max_value:
            max_value = tensor[i]
            index = i
    return index


def train():
    path = './datas/'
    X_list = []
    Y_list = []


    for i in range(len(words)):
        filenames = os.listdir(path + words[i])
        filenames.sort()
        for n, fi in enumerate(filenames):
            file_path = path + words[i]+'/'+fi
            #read file and convert to array
            X_list.append(file_to_array(file_path))
            Y_list.append(i)

    X = np.array(X_list).reshape(-1,NB_FRAME_PER_WORD, NB_BODY_POINTS, NB_DIMS)
    Y = np.array(Y_list)

    print("-----------------------------------------------------------")

    model = tf.keras.models.Sequential([
            tf.keras.layers.Flatten(input_shape=(NB_FRAME_PER_WORD, NB_BODY_POINTS, NB_DIMS)),
            tf.keras.layers.Dense(64, activation='relu'),
            tf.keras.layers.Dropout(0.2),
            tf.keras.layers.Dense(len(words)*2, activation='softmax')
    ])
    print("-----------------------------------------------------------")

    model.compile(optimizer='adam', loss='sparse_categorical_crossentropy', metrics=['accuracy'])
    model.fit(X, Y, epochs=500)
    return model


def guess(model, data):
    X_testing = []
    X_testing.append(data)

    X_testing_final = np.array(X_testing).reshape(-1, NB_FRAME_PER_WORD, NB_BODY_POINTS, NB_DIMS)
    result_tensor = model.predict(X_testing_final)
    prediction = get_prediction_result(result_tensor[0]) 
    proba = result_tensor[0][prediction]
    return((words[prediction], proba))


def saveModel(location, model):
    model.save(location, save_format='h5')
    
def loadModel(modelName):
    return tf.keras.models.load_model(modelName)