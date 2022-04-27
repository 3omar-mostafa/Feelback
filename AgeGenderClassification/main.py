import pickle as pickle
# import FeaturesExtraction
import AgeGenderClassification.FeaturesExtraction as FeaturesExtraction
# import Preprocessing
import AgeGenderClassification.Preprocessing as Preprocessing

class GenderAgeClassification:
    def __init__(self, model_path_age, model_path_gender):
        self.modelAge = pickle.load(open(model_path_age, 'rb'))
        self.modelGender = pickle.load(open(model_path_gender, 'rb'))

    def getGender(self, frame, facesLocations):
        faces = []
        for x1,y1,x2,y2 in facesLocations:
            faces.append(frame[y1:y2,x1:x2])

        predictedGender = []
        for face in faces:
            img = Preprocessing.preprocess_image(face)
            img_features = FeaturesExtraction.extract_features(img, feature="LPQ")
            predictedGender.append(self.modelGender.predict([img_features])[0])

        return predictedGender
    
    def getAge(self, frame, facesLocations):
        faces = []
        for x1,y1,x2,y2 in facesLocations:
            faces.append(frame[y1:y2,x1:x2])

        predictedAge = []
        for face in faces:
            img = Preprocessing.preprocess_image(face)
            img_features = FeaturesExtraction.extract_features(img, feature="LPQ")
            predictedAge.append(self.modelAge.predict([img_features])[0])

        return predictedAge

            