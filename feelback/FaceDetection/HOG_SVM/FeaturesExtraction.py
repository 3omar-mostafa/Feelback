# Boilerplate to Enable Relative imports when calling the file directly
if (__name__ == '__main__' and __package__ is None) or __package__ == '':
    import sys
    from pathlib import Path

    file = Path(__file__).resolve()
    sys.path.append(str(file.parents[3]))
    __package__ = '.'.join(file.parent.parts[len(file.parents[3].parts):])

import cv2
from .Utils import *

def ExtractHOGFeatures(img,target_img_size=(19,19),flatten = False):
    """
    Extracts HOG features from an image
    :param img: image to extract features from
    :param cellSize: size of a cell
    :param blockSize: size of a block
    :param nBins: number of bins
    :return: HOG features
    """
    img = cv2.resize(img, target_img_size)
    img = HistogramEqualization(img)
    
    hog = vectorizedHogSlidingWindows([np.array(img)],flatten=flatten)

    return hog

def ApplyPCA(features,pca):
    """Applies PCA to a feature vector

    Args:
        features (_type_): feature vector
        pca (_type_): PCA object

    Returns:
        _type_: PCA transformed feature vector
    """
    features = np.array(features)
    return pca.transform(features.reshape(1,-1))[0]