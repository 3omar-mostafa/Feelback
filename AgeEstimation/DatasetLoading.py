import os
import cv2
import FeaturesExtraction

def load_UTK_AgeGender_dataset(label="gender", age_range=(1,90)):
    """Loads the UTK AgeGender Dataset

    Args:
        label (str, optional): label type for the data. Defaults to "gender".
        age_range (tuple, optional): max and min ages. Defaults to (1,90).

    Raises:
        Exception: Wrong label is supplied
        Exception: Wrong age range is supplied

    Returns:
        Tuple(features, labels): Features and Labels of the dataset
    """

    # Args checking
    if label != "gender" and label != "age":
        raise Exception("Wrong Parameter For label argument")
    if type(age_range) != tuple or age_range[0] < 1 or age_range[1] > 90 :
        raise Exception("Wrong Parameter For age_range argument")

    # Set path to dataset
    path_to_dataset = os.path.join(os.path.dirname(
        __file__), "../Data/UTK_AgeGender")

    # Initialize Variables
    features = []
    labels = []

    # Loop over directories and get Images
    count = 0
    for i, fn in enumerate(os.listdir(path_to_dataset)):

        # Extract label
        image_name_split = fn.split('_') 
        age = int(image_name_split[0])

        # Skip if outside of range
        if age < age_range[0] or age > age_range[1]:
            continue

        # Increase count
        count += 1

        # Add Label
        if label == "gender":
            gender = "male" if image_name_split[1] == "0" else "female" 
            labels.append(gender)
        elif label == "age":
            labels.append(age)

        # Extract Image features
        path = os.path.join(path_to_dataset, fn)
        img = cv2.imread(path, cv2.IMREAD_GRAYSCALE)
        features.append(FeaturesExtraction.extract_features(img, feature="LPQ"))

        # Show progress for debugging purposes
        if count % 500 == 0:
            # Utils.show_image(img, gender)
            print(F"UTK Gender_Age Dataset: Finished Reading {count}")

    return features, labels
