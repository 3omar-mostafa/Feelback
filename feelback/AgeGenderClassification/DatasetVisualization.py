# Boilerplate to Enable Relative imports when calling the file directly
if (__name__ == '__main__' and __package__ is None) or __package__ == '':
    import sys
    from pathlib import Path

    file = Path(__file__).resolve()
    sys.path.append(str(file.parents[3]))
    __package__ = '.'.join(file.parent.parts[len(file.parents[3].parts):])

from . import DatasetLoading
from . import Utils


def visualise_Gender_Kaggle(type="Validation"):
    """Visualize the Gender Kaggle Dataset

    Args:
        type (str, optional): Load Either Training or Validation Datasets. Defaults to "Validation".

    """
    # Read Datset
    _, labels, _ = DatasetLoading.load_Gender_Kaggle_dataset(selected_feature=None,type=type)

    # Draw the dataset histogram
    Utils.plot_dataset_histogram(labels)
    
    # Draw the dataset piechart
    Utils.plot_dataset_piechart(labels)

def visualise_UTK_AgeGender(label="gender", age_range=(1, 90)):
    """Visualize the UTK Age Gender Dataset
    
    Args:
        label (str, optional): label type for the data. Defaults to "gender".
        age_range (tuple, optional): max and min ages. Defaults to (1,90).

    """
    _, labels, _ = DatasetLoading.load_UTK_AgeGender_dataset(selected_feature=None,label=label, age_range=age_range)

    # Draw the dataset histogram
    Utils.plot_dataset_histogram(labels)
    
    # Draw the dataset piechart
    Utils.plot_dataset_piechart(labels)


def visualise_FGNET_Age():

    _, labels, _ = DatasetLoading.load_FGNET_Age_dataset(selected_feature=None)

    # Draw the dataset histogram
    Utils.plot_dataset_histogram(labels)
    
    # Draw the dataset piechart
    Utils.plot_dataset_piechart(labels)


if __name__ == "__main__":
    visualise_FGNET_Age()
    # visualise_UTK_AgeGender(label="age", age_range=(1,90))
    # visualise_Gender_Kaggle(type="Validation")
