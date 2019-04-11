import csv

import cv2
import numpy as np

target = 'resources/data/alphabet.csv'

alphabet = {}

samples = 500

with open(target, newline='') as f:
    reader = csv.reader(f, delimiter=',', quotechar='|')

    current_letter = None
    count = 0

    for row in reader:
        label = row.pop(0)
        image_array = np.asarray(row)

        if label != current_letter:
            current_letter = label
            alphabet[str(current_letter)] = []
            count = 0

        if count == samples:
            pass

        else:
            alphabet[str(current_letter)].append(image_array)
            count += 1

test = []
train = []
train_labels = []

for letter, images in alphabet.items():
    num_images = len(images)

    if num_images % 2 != 0:
        num_images -= 1

    half = int(num_images/2)

    images_train = images[:half]
    labels = np.repeat(int(letter), half)

    print("images_train: {}, labels: {}".format(len(images_train), labels.size))

    train.append(images_train)
    train_labels.append(labels)
    test.append(images[half:num_images])

train_labels = np.concatenate(train_labels)[:, np.newaxis]
test_labels = train_labels.copy()

test = np.array(np.concatenate(test)).astype(np.float32)
train = np.array(np.concatenate(train)).astype(np.float32)

print("test: {}, train: {}".format(test.shape, train.shape))
print(train_labels)

knn = cv2.ml.KNearest_create()
knn.train(train, cv2.ml.ROW_SAMPLE, train_labels)

ret, result, neighbours, dist = knn.findNearest(test, k=5)
matches = (result == test_labels)
correct = np.count_nonzero(matches)
accuracy = correct*100.0/result.size
print(accuracy)

np.savez('knn_data.npz', train=train, train_labels=train_labels)
