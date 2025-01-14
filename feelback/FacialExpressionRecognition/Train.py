"""
Imports
"""
# Boilerplate to Enable Relative imports when calling the file directly
if (__name__ == '__main__' and __package__ is None) or __package__ == '':
    import sys
    from pathlib import Path

    file = Path(__file__).resolve()
    sys.path.append(str(file.parents[3]))
    __package__ = '.'.join(file.parent.parts[len(file.parents[3].parts):])

from operator import le
import numpy as np
from sklearn.model_selection import train_test_split
from sklearn import svm
from sklearn.neural_network import MLPClassifier
import random
import pickle
from . import DatasetLoading

"""
Global Variables
"""

random_seed = 1
random.seed(random_seed)
np.random.seed(random_seed)

used_classifier = "SVM"

classifiers = {
    # SVM with gaussian kernel
    'SVM': svm.SVC(random_state=random_seed, kernel="rbf"),
    'MLP': MLPClassifier(random_state=random_seed, hidden_layer_sizes=(100,), max_iter=20000),
}

"""
Functions
"""
def train_classifier():

    # Load dataset with extracted features
    print('Loading dataset and extract features. This will take time ...')
    features, labels = DatasetLoading.load_Multiple_datasets()
    # features, labels = DatasetLoading.load_AffectNet_dataset()
    print('Finished loading dataset.')
    print("Number of actual used samples: ", len(labels))
    # Since we don't want to know the performance of our classifier on images it has seen before
    # we are going to withhold some images that we will test the classifier on after training
    train_features, test_features, train_labels, test_labels = train_test_split(
        features, labels, test_size=0.2, random_state=random_seed, stratify=labels, shuffle=True)

    print('############## Training ', used_classifier, "##############")
    # Train the model only on the training features
    model = classifiers[used_classifier]
    model.fit(train_features, train_labels)

    # Test the model on images it hasn't seen before
    accuracy = model.score(test_features, test_labels)
    train_accuracy = model.score(train_features, train_labels)

    print(used_classifier, ' Train accuracy:', train_accuracy *
          100, '%', ' Test accuracy:', accuracy*100, '%')

def main():
    train_classifier()
    classifier = classifiers[used_classifier]
    # save the model to disk
    filename = 'FacialExpressionRecognition/Models/Model.sav'
    pickle.dump(classifier, open(filename, 'wb'))

if __name__ == "__main__":
    main()
