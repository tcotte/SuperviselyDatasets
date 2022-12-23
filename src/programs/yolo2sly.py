import os

import cv2
from tqdm import tqdm

from src.create_sly_project import ProjectStructure
from ..sly_transformer import TransformerSly


class YOLO2JSON(TransformerSly):
    def __init__(self, folder: str, filename: str, destination: str):
        super(YOLO2JSON, self).__init__()
        self.project_folder = folder
        self.filename = filename
        self.destination = destination

        self.img_width, self.img_height = self.get_picture_shape()

        self.objects = self.get_objects_list()
        self.sly_dict = self.gather_information()

        self.create_json()

    def get_picture_shape(self):
        try:
            im = cv2.imread(os.path.join(self.project_folder, "img", self.filename))
            return im.shape[1], im.shape[0]
        except Exception as e:
            raise "Can't find the picture"

    def read_yolo_file(self):
        txt_file = self.filename[:-4] + ".txt"
        with open(os.path.join(self.project_folder, "labels", txt_file)) as file:
            lines = [line.rstrip() for line in file]
        return lines

    def gather_information(self):
        return {
            "description": "",
            "size": {
                "height": self.img_height,
                "width": self.img_width
            },
            "objects": self.objects
        }

    def get_objects_list(self):
        """
        YOLO format => <class> <x> <y> <width> <height>
        :return:
        """
        lines = self.read_yolo_file()

        objects = []
        for line in lines:
            annotation_array = line.split()
            class_id = annotation_array[0]
            x = float(annotation_array[1])
            y = float(annotation_array[2])
            width = float(annotation_array[3])
            height = float(annotation_array[4])

            ann = {
                "classId": class_id,
                "geometryType": "rectangle",
                "classTitle": "duckweed",
                "points": {
                    "exterior": [
                        [
                            (x - width / 2) * self.img_width,
                            (y - height / 2) * self.img_height
                        ],
                        [
                            (x + width / 2) * self.img_width,
                            (y + height / 2) * self.img_height
                        ]
                    ],
                    "interior": []
                }
            }
            objects.append(ann)
        return objects


if __name__ == "__main__":
    source = r"C:\Users\tristan_cotte\PycharmProjects\duckweed\yolo_results\23-11-2022"
    destination = "yolo_dataset"

    ProjectStructure(project_path=source, output_dir=destination, config_file="../../config.yaml")

    for file in tqdm(os.listdir(os.path.join(source, "img"))):
        YOLO2JSON(folder=source, filename=file, destination=destination)
