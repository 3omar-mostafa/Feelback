# Boilerplate to Enable Relative imports when calling the file directly
if (__name__ == '__main__' and __package__ is None) or __package__ == '':
    import sys
    from pathlib import Path

    file = Path(__file__).resolve()
    sys.path.append(str(file.parents[3]))
    __package__ = '.'.join(file.parent.parts[len(file.parents[3].parts):])

import os
import numpy as np
import cv2
from sklearn.metrics import f1_score
from .FeaturesExtraction import ExtractHOGFeatures
from sklearn.model_selection import train_test_split
from sklearn import svm
from sklearn.svm import LinearSVC
import random
import pickle
import time
from sklearn.decomposition import PCA
from sklearn.neural_network import MLPClassifier
import matplotlib.pyplot as plt
import seaborn as sns
import pandas as pd
from sklearn import metrics

random_seed = 1
random.seed(random_seed)
np.random.seed(random_seed)

used_classifier = "SVM"

classifiers = {
    # SVM with gaussian kernel
    'SVM': svm.SVC(random_state=random_seed, kernel="rbf"),
    'LinearSVM': LinearSVC(random_state=random_seed),
    'MPL': MLPClassifier(random_state=random_seed, max_iter=500)
}


def load_dataset(path_to_dataset):
    features = []
    labels = []
    path_to_dataset = os.path.join(os.getcwd(), path_to_dataset)
    directoriesNames = os.listdir(path_to_dataset)
    print(directoriesNames)
    for directory in directoriesNames:
        print(directory)
        directoryPath = os.path.join(path_to_dataset, directory)
        for root, dirs, files in os.walk(directoryPath):
            for file in files:
                # append the file name to the list
                fileName = os.path.join(root, file)
                labels.append(directory)
                # read the image and extract features
                img = cv2.imread(fileName)
                features.append(ExtractHOGFeatures(img,flatten=True))

    return features, labels


def train_classifier(path_to_dataset):
    # Load dataset with extracted features
    print('Loading dataset. This will take time ...')
    features, labels = load_dataset(path_to_dataset)
    print('Finished loading dataset.')
    # PCA
    D_before = len(features[0])
    pca = PCA(n_components=50)
    pca.fit(features)
    filename = './Models/PCA_v4.sav'
    pickle.dump(pca, open(filename, 'wb'))
    features = pca.transform(features)
    D_after = len(features[0])
    # print('Reduced the dimension from ', D_before, ' to ', D_after)

    # Since we don't want to know the performance of our classifier on images it has seen before
    # we are going to withhold some images that we will test the classifier on after training
    train_features, test_features, train_labels, test_labels = train_test_split(
        features, labels, test_size=0.2, random_state=random_seed, stratify=labels, shuffle=True)

    # save test features and labels
    filename = './Test_Features_v3.sav'
    pickle.dump(test_features, open(filename, 'wb'))
    filename = './Test_Labels_v3.sav'
    pickle.dump(test_labels, open(filename, 'wb'))

    print('############## Training ', used_classifier, "##############")
    # Train the model only on the training features
    model = classifiers[used_classifier]
    model.fit(train_features, train_labels)

    # Test the model on images it hasn't seen before
    accuracy = model.score(test_features, test_labels)
    train_accuracy = model.score(train_features, train_labels)

    # Calculate f1 score
    f1 = f1_score(test_labels, model.predict(test_features), average='weighted')

    print('f1 score: ', f1)

    cnf_matrix = metrics.confusion_matrix(test_labels, model.predict(test_features))
    class_names=[0,1] # name  of classes
    fig, ax = plt.subplots()
    tick_marks = np.arange(len(class_names))
    plt.xticks(tick_marks, class_names)
    plt.yticks(tick_marks, class_names)
    # create heatmap
    sns.heatmap(pd.DataFrame(cnf_matrix), annot=True, cmap="YlGnBu" ,fmt='g')
    ax.xaxis.set_label_position("top")
    plt.tight_layout()
    plt.title('Confusion matrix', y=1.1)
    plt.ylabel('Actual label')
    plt.xlabel('Predicted label')
    # plt.show()

    print(used_classifier, ' Train accuracy:', train_accuracy *
          100, '%', ' Test accuracy:', accuracy * 100, '%')


def main():
    train_classifier("Data")
    classifier = classifiers[used_classifier]
    # save the model to disk
    filename = './Models/Model_v4.sav'
    pickle.dump(classifier, open(filename, 'wb'))


if __name__ == "__main__":
    # calculate training time
    start_time = time.time()
    main()
    end_time = time.time()
    print("[INFO] Training time is {:.5f} seconds".format(end_time - start_time))
