import argparse
import os

from tqdm import tqdm

from create_sly_project import ProjectStructure
from src.programs.labelme2sly import Labelme2JSON
from src.programs.mask2sly import Mask2JSON
from src.programs.yolo2sly import YOLO2JSON

parser = argparse.ArgumentParser(
    prog='Supervise.ly imports',
    description='Import some type of annotations to Supervise.ly format',
    epilog='The objective is to annotate a 2nd time with Sly ')

parser.add_argument('-src', '--source', type=str, required=True,
                    help='path of the project containing images and labels')
parser.add_argument('-dst', '--destination', type=str, default="Output",
                    help='path of the output project containing Supervise.ly annotations')
parser.add_argument('-cfg', '--config', type=str, required=False,
                    help='path of the config file to create meta.json file')
parser.add_argument('-prg', '--program', type=int, required=True,
                    help='Type of the annotations imported into Supervise.ly: \n'
                         '1. YOLO\n'
                         '2. LabelMe\n'
                         '3. Masks'
                    )

if __name__ == "__main__":
    args = parser.parse_args()

    ProjectStructure(project_path=args.source, output_dir=args.destination, config_file=args.config)

    for file in tqdm(os.listdir(os.path.join(args.source, "img"))):
        if args.program == 1:
            YOLO2JSON(folder=args.source, filename=file, destination=args.destination)
        if args.program == 2:
            Labelme2JSON(folder=args.source, filename=file, destination=args.destination)
        if args.program == 3:
            Mask2JSON(folder=args.source, filename=file, destination=args.destination)
