import os

from sklearn.model_selection import train_test_split
import shutil
import typing


def get_img_and_labels(path_X: str, path_y: str) -> typing.Tuple[typing.List, typing.List]:
    """
    Get sorted images and labels
    :param path_X: pictures folder path
    :param path_y: labels folder path
    :return: tuple made up of :
          - List of pictures absolute paths
          - List of labels absolute paths
    """
    X = [os.path.join(path_X, x) for x in os.listdir(path_X)]
    y = [os.path.join(path_y, x) for x in os.listdir(path_y)]
    y.sort()
    X.sort()
    return X, y


def copy_ds_files(path_dataset: str, img_folder_name: str, X_train: typing.List, X_test: typing.List,
                  y_train: typing.List, y_test: typing.List) -> None:
    """
    Copy dataset files in output folder. The files are grouped in lists where their names indicates
    if the sample within takes part of train, test / labels, image.
    This output folder contains child folders where different lists are pasted.
    :param path_dataset: output folder path.
    :param X_train: absolute paths list of training picture samples
    :param X_test: absolute paths list of test picture samples
    :param y_train: absolute paths list of train labels samples
    :param y_test: absolute paths list of test labels samples
    """
    if os.path.isdir(path_dataset):
        shutil.rmtree(path_dataset)

    os.makedirs(path_dataset)
    os.makedirs(os.path.join(path_dataset, 'train'))
    os.makedirs(os.path.join(path_dataset, 'train', img_folder_name))
    os.makedirs(os.path.join(path_dataset, 'train', 'labels'))
    os.makedirs(os.path.join(path_dataset, 'val'))
    os.makedirs(os.path.join(path_dataset, 'val', img_folder_name))
    os.makedirs(os.path.join(path_dataset, 'val', 'labels'))

    for dataset, path in zip([X_train, X_test, y_train, y_test], [os.path.join(path_dataset, "train", img_folder_name),
                                                                  os.path.join(path_dataset, "val", img_folder_name),
                                                                  os.path.join(path_dataset, "train", "labels"),
                                                                  os.path.join(path_dataset, "val", "labels")]):
        for i in dataset:
            shutil.copyfile(i, os.path.join(path, i.split('/')[-1]))


def separate_dataset_samples(path_X: str, path_y: str, test_size: float = 0.15,
                             path_dataset: str = "/content/dataset", img_folder_name: str ="images") -> None:
    """
    Separate dataset samples in validation and test samples in a random way. The files which
    represent samples are gathered in different folder in function if they are labels, images,
    test samples, train samples.
    :param path_X: pictures folder path
    :param path_y: labels folder path
    :param test_size: percentage of test files in dataset
    :param path_dataset: path of output dataset folder
    """
    X, y = get_img_and_labels(path_X, path_y)

    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=test_size, random_state=42)

    copy_ds_files(path_dataset, img_folder_name, X_train, X_test, y_train, y_test)
