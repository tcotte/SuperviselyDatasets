from typing import Dict

import yaml
from faker import Factory
from yaml import SafeLoader


def create_meta_dict(config_file: str) -> Dict:
    """

    :param config_file:
    :return:
    """
    with open(config_file) as f:
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


if __name__ == "__main__":
    dict_meta = create_meta_dict("../config.yaml")
    print(dict_meta)
