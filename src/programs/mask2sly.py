import os
from typing import List, Union

import cv2
import supervisely as sly
import numpy as np
from ..create_sly_project import ProjectStructure
from ..sly_transformer import TransformerSly

"""
https://docs.supervise.ly/data-organization/00_ann_format_navi/04_supervisely_format_objects#bitmap
"""


class Mask2JSON(TransformerSly):
    def __init__(self, folder: str, filename: str, destination: str, classes: Union[List, None] = ["cls"]):
        super(Mask2JSON, self).__init__()
        self.project_folder = folder
        self.filename = filename
        self.destination = destination
        self.classes = classes

        self.objects = []
        if len(self.classes) > 1:
            for cls_id, cls in enumerate(self.classes):
                self.binary_picture = self.get_binary_picture(cls=cls)
                if cls_id == 0:
                    self.img_width, self.img_height = self.get_picture_shape()
                self.get_sly_bitmap(cls=cls, id_class=cls_id)

        else:
            self.binary_picture = self.get_binary_picture()
            self.img_width, self.img_height = self.get_picture_shape()
            self.get_sly_bitmap()

        self.sly_dict = self.gather_information()

        self.create_json()

    def get_sly_bitmap(self, cls=None, id_class=None):
        # if self.img_height > self.img_width:
        #     self.binary_picture = cv2.rotate(self.binary_picture, cv2.ROTATE_90_CLOCKWISE)

        if cls is None:
            class_id = 0
            class_title = self.classes[0]
        else:
            class_id = id_class
            class_title = cls

        if np.count_nonzero(self.binary_picture) != 0:
            figure = sly.Bitmap(self.binary_picture)
            origin = figure.origin.to_json()

            ann = {
                "classId": class_id,
                "description": "",
                "geometryType": "bitmap",
                "classTitle": class_title,
                "bitmap": {
                    "data": sly.Bitmap.data_2_base64(figure.data),
                    "origin": origin["points"]["exterior"][0]
                }
            }

            self.objects.append(ann)

    def get_binary_picture(self, cls=None):
        if cls is not None:
            extension_file = self.filename.split(".")[-1]
            filename = self.filename[:-4] + "_" + cls + "." + extension_file
        else:
            filename = self.filename

        try:
            mask = cv2.imread(os.path.join(self.project_folder, "labels", filename), cv2.IMREAD_GRAYSCALE)
            _, binary_mask = cv2.threshold(mask, 0, 255, cv2.THRESH_BINARY)
            return binary_mask
        except Exception as e:
            raise "Can't find the picture"

    def get_picture_shape(self):
        return self.binary_picture.shape[1], self.binary_picture.shape[0]


if __name__ == "__main__":
    source = r"dataset_mask"
    destination = "duckweed_multimask"
    ProjectStructure(project_path=source, output_dir=destination)

    for file in os.listdir(os.path.join(source, "img")):
        Mask2JSON(folder=source, filename=file, destination=destination)
