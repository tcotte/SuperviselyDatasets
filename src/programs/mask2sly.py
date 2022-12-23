import os

import cv2
import supervisely as sly

from ..create_sly_project import ProjectStructure
from ..sly_transformer import TransformerSly

"""
https://docs.supervise.ly/data-organization/00_ann_format_navi/04_supervisely_format_objects#bitmap
"""


class Mask2JSON(TransformerSly):
    def __init__(self, folder: str, filename: str, destination: str):
        super(Mask2JSON, self).__init__()
        self.project_folder = folder
        self.filename = filename
        self.destination = destination

        self.binary_picture = self.get_binary_picture()
        self.img_width, self.img_height = self.get_picture_shape()
        self.objects = self.get_sly_bitmap()

        self.sly_dict = self.gather_information()

        self.create_json()

    def get_sly_bitmap(self):
        # if self.img_height > self.img_width:
        #     self.binary_picture = cv2.rotate(self.binary_picture, cv2.ROTATE_90_CLOCKWISE)

        figure = sly.Bitmap(self.binary_picture)
        origin = figure.origin.to_json()
        class_id = 0

        objects = []
        ann = {
            "classId": class_id,
            "description": "",
            "geometryType": "bitmap",
            "classTitle": "living",
            "bitmap": {
                "data": sly.Bitmap.data_2_base64(figure.data),
                "origin": origin["points"]["exterior"][0]
            }
        }

        objects.append(ann)
        return objects

    def get_binary_picture(self):
        try:
            mask = cv2.imread(os.path.join(self.project_folder, "labels", self.filename), cv2.IMREAD_GRAYSCALE)
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
