# Supervise.ly formats

Convert datasets into Supervise.ly format to labellise a 2nd time in this platform.

### Installation (with Anaconda3)
```
git clone https://github.com/tcotte/SuperviselyDatasets.git
conda create -n sly python=3.8
conda activate sly
pip install requirements.txt
```


### Utilisation 
```
python main.py -src {input_dataset_folder} -dst {output_folder} -cfg ../config.yaml --program 1
```

**Optional arguments :**
```
  -src SOURCE, --source SOURCE
                        path of the project containing images and labels
  -dst DESTINATION, --destination DESTINATION
                        path of the output project containing Supervise.ly annotations
  -cfg CONFIG, --config CONFIG
                        path of the config file to create meta.json file
  -prg PROGRAM, --program PROGRAM
                        Type of the annotations imported into Supervise.ly: 1. YOLO 2. LabelMe 3. Masks
```

### Input dataset

For all programs except the third program using more than one class:
```
dataset
├── labels
│   ├── img_x.{type}
│   ├── img_y.{type}
│   └── img_z.{type}
└── img
    ├── img_x.jpeg
    ├── img_y.jpeg
    └── img_z.jpeg

```

For the third program multiclass:

```
dataset
├── labels
│   ├── img_x_class1.{type}
│   ├── img_x_class2.{type}
│   ├── img_x_class3.{type}
│   ├── img_y_class1.{type}
│   ├── img_y_class2.{type}
│   ├── img_y_class3.{type}
│   ├── img_z_class1.{type}
│   ├── img_z_class2.{type}
│   ├── img_z_class3.{type}
└── img
    ├── img_x.jpeg
    ├── img_y.jpeg
    └── img_z.jpeg

```


### Supervise.ly project
```
my_project
├── meta.json
├── dataset_name_01
│   ├── ann
│   │   ├── img_x.jpeg.json
│   │   ├── img_y.jpeg.json
│   │   └── img_z.jpeg.json
│   └── img
│       ├── img_x.jpeg
│       ├── img_y.jpeg
│       └── img_z.jpeg
├── dataset_name_02
│   ├── ann
│   │   ├── img_x.jpeg.json
│   │   ├── img_y.jpeg.json
│   │   └── img_z.jpeg.json
│   └── img
│       ├── img_x.jpeg
│       ├── img_y.jpeg
│       └── img_z.jpeg
```

