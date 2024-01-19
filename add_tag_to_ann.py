import argparse
import json
import os
from typing import Dict

from tqdm import tqdm


def get_data_from_jsonfile(json_file: str) -> Dict:
    with open(json_file) as json_file:
        data = json.load(json_file)
    json_file.close()
    return data


def write_data_in_jsonfile(json_file: str, dict_ann: Dict) -> None:
    with open(json_file, 'w') as fp:
        json.dump(dict_ann, fp)
    fp.close()


def add_missing_tags(dict_ann: Dict) -> Dict:
    if not "tags" in dict_ann:
        dict_ann["tags"] = []

    for data_object in dict_ann["objects"]:
        if not "tags" in data_object:
            data_object["tags"] = []

    return dict_ann


parser = argparse.ArgumentParser(
    prog="Add tags to Supervisely annotation files",
    description="""
        New version of Supervisely requires "tags" list on each labeled object. Because the export of data as Supervise.ly 
        format was developed with a previous version of Supervise.ly, this code enables to add an empty tag list for the whole 
        annotation and an empty tag list for each labeled objects.
    """,
    epilog="Developed by Tristan Cotte --- SGS France Operational Excellence",
)
parser.add_argument('-src', dest="source", type=str, required=True,
                    help="Path of the annotation folder (or annotation file) where annotations have to change")
args = parser.parse_args()

path_ann = args.source

if os.path.isdir(path_ann):
    for idx in tqdm(range(len(os.listdir(path_ann)))):
        json_filepath = os.path.join(path_ann, os.listdir(path_ann)[idx])
        data = get_data_from_jsonfile(json_filepath)
        data = add_missing_tags(data)
        write_data_in_jsonfile(json_filepath, data)

elif os.path.isfile(path_ann):
    # test if file is json file
    if path_ann.endswith(".json"):
        data = get_data_from_jsonfile(path_ann)
        data = add_missing_tags(data)
        write_data_in_jsonfile(path_ann, data)

    else:
        raise "This program supports only Supervise.ly json files"
