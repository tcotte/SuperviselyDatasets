import json
import os
from typing import Dict

from ..create_sly_project import ProjectStructure
from ..sly_transformer import TransformerSly


class Labelme2JSON(TransformerSly):
    def __init__(self, folder: str, filename: str, destination: str):
        super().__init__()
        self.project_folder = folder

        self.filename = filename
        self.destination = destination

        self.content = self.read_json_file()
        self.img_width, self.img_height = self.get_picture_shape()
        #
        self.objects = self.get_objects_list()
        self.sly_dict = self.gather_information()
        #
        self.create_json()

    def read_json_file(self) -> Dict:
        content = {}
        json_name = self.filename[:-4] + ".json"
        with open(os.path.join(self.project_folder, "labels", json_name)) as f:
            data = json.load(f)
        content['shapes'] = data['shapes']
        content['img_height'] = data['imageHeight']
        content['img_width'] = data['imageWidth']
        return content

    def get_picture_shape(self) -> [int, int]:
        return self.content['img_width'], self.content['img_height']

    def get_objects_list(self):
        objects = []
        for obj in self.content['shapes']:
            ann = {
                # "classId": class_id,
                "geometryType": "rectangle",
                "classTitle": obj["label"],
                "points": {
                    "exterior": [[round(coord) for coord in pts] for pts in obj["points"]],
                    "interior": []
                }
            }

            objects.append(ann)
        return objects


if __name__ == "__main__":
    source = r"C:\Users\tristan_cotte\PycharmProjects\yolo2supervisely\labelme_dataset"
    destination = "test_labelme2sly"

    ProjectStructure(project_path=source, output_dir=destination, config_file="../../config.yaml")

    for file in os.listdir(os.path.join(source, "img")):
        Labelme2JSON(folder=source,
                     filename=file,
                     destination=destination)

