import json
import os
import shutil
from typing import Dict

import yaml
from faker import Factory
from yaml import SafeLoader


class ProjectStructure:
    def __init__(self, project_path: str, output_dir: str, config_file: str = ""):
        self.img_path = os.path.join(project_path, "img")
        self.output_dir = output_dir
        self.config_file = config_file

        self.create_folders()
        self.copy_img_folder()

        if config_file != "":
            meta_dict = self.create_meta_dict()
            self.save_meta_file(metadata=meta_dict)

    def save_meta_file(self, metadata: Dict) -> None:
        with open(os.path.join(self.output_dir, "meta.json"), "w") as write_file:
            json.dump(metadata, write_file)

    def create_meta_dict(self) -> Dict:
        """

        :param config_file:
        :return:
        """
        with open(self.config_file) as f:
            data = yaml.load(f, Loader=SafeLoader)

        fake = Factory.create()
        class_list = []
        for type_ann, class_names in data.items():
            # one type of annotation can have one or various classes (str or List)
            if isinstance(class_names, str):
                meta_class = {
                    "title": class_names,
                    "shape": type_ann,
                    "color": fake.safe_hex_color().upper(),
                    "geometry_config": {}
                }
                class_list.append(meta_class)
            else:
                for cls in class_names:
                    meta_class = {
                        "title": cls,
                        "shape": type_ann,
                        "color": fake.safe_hex_color().upper(),
                        "geometry_config": {}
                    }
                    class_list.append(meta_class)

        return {"classes": class_list}

    def create_folders(self):
        directories = ["dataset", "dataset/ann"]
        for directory in directories:
            path = os.path.join(self.output_dir, directory)
            os.makedirs(path)

    def copy_img_folder(self):
        dest_dir = os.path.join(self.output_dir, "dataset/img")
        shutil.copytree(self.img_path, dest_dir)


if __name__ == "__main__":
    ProjectStructure(project_path=r"/yolo_dataset/img", output_dir="test")
