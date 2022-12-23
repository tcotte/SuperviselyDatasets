import json
import os


class TransformerSly:
    def __init__(self):
        self.objects = None
        self.filename = None
        self.destination = None
        self.img_height = None
        self.img_width = None

    @staticmethod
    def create_output_folder(directory: str):
        if not os.path.exists(directory):
            os.makedirs(directory)

    def create_json(self):
        output_directory = os.path.join(self.destination, "dataset/ann")
        self.create_output_folder(directory=output_directory)
        extension_file = self.filename[-4:].lower()

        with open(os.path.join(output_directory, self.filename[:-4] + extension_file + ".json"), "w") as outfile:
            json.dump(self.sly_dict, outfile)

    def gather_information(self):
        return {
            "description": "",
            "size": {
                "height": self.img_height,
                "width": self.img_width
            },
            "objects": self.objects
        }

