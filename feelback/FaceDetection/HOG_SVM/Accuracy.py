# Boilerplate to Enable Relative imports when calling the file directly
if (__name__ == '__main__' and __package__ is None) or __package__ == '':
    import sys
    from pathlib import Path

    file = Path(__file__).resolve()
    sys.path.append(str(file.parents[3]))
    __package__ = '.'.join(file.parent.parts[len(file.parents[3].parts):])

from operator import mod
from .FeaturesExtraction import ExtractHOGFeatures
from .Utils import ConvertToGrayScale, HistogramEqualization
import pickle as pickle
import numpy as np
import cv2
import os
from sklearn.metrics import confusion_matrix

# load the model from disk
model = pickle.load(open('./Models/ModelCBCL.sav', 'rb'))

path_to_testset = os.path.join(os.getcwd(), "Test")

output = []

for root, dirs, files in os.walk(path_to_testset):
    for file in files:
        fileName = os.path.join(root, file)
        img = cv2.imread(fileName)
        img = ConvertToGrayScale(img)
        img = HistogramEqualization(img)
        image_features = ExtractHOGFeatures(img)
        predicted_label = model.predict([image_features])
        output.append((fileName, predicted_label))

correct = 0
for image in output:
    label, predicted_label = image

    if predicted_label == "Faces" and "Faces" in label:
        correct += 1
    elif predicted_label == "Non" and "Non" in label:
        correct += 1

print("Accuracy: ", correct / len(output) * 100, "%")