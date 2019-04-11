# import matplotlib.pyplot as plt
import os

import cv2
import numpy as np

# Load the data, converters convert the letter to a number
data = np.loadtxt('resources/letter-recognition.data', dtype='float32', delimiter=',', converters={0: lambda ch: ord(ch) - ord('A')})

# split the data to two, 10000 each for train and test
train, test = np.vsplit(data, 2)

# split trainData and testData to features and responses
responses, trainData = np.hsplit(train, [1])
labels, testData = np.hsplit(test, [1])

# Initiate the kNN, classify, measure accuracy.
knn = cv2.ml.KNearest_create()
knn.train(trainData, cv2.ml.ROW_SAMPLE, responses)
ret, result, neighbours, dist = knn.findNearest(testData, k=5)

correct = np.count_nonzero(result == labels)
accuracy = correct*100.0/10000
print(accuracy)

dir_images = '{}/resources/sample_tiles'.format(os.getcwd())

for file in os.listdir(dir_images):
    test_img = cv2.imread('{}/{}'.format(dir_images, file), 0)
    test_img = cv2.resize(test_img, (4, 4))
    x = np.array(test_img)
    test_img = x.reshape(-1, 16).astype(np.float32)
    ret, result, neighbours, dist = knn.findNearest(test_img, k=3)
    # Print the predicted number
    print(int(result))
