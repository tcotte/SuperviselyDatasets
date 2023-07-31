import typing

import supervisely as sly


def filter_annotations(annotation: sly.Annotation, remain_classes: typing.List) -> sly.Annotation:
    """
    This function filters annotations containing object class name in *remain_classes*.
    :param annotation: annotations of one picture
    :param remain_classes: list of object class names which are kept in returned annotations
    :return: annotations filtered with only labels which has their object class names belonging in
    remain_classes list.
    """

    filtered_labels = []

    for label in annotation.labels:
        if label.obj_class.name in remain_classes:
            filtered_labels.append(label)

    return annotation.clone(labels=filtered_labels)


def change_cls_annotations(annotation: sly.Annotation, input_classes: typing.List, output_classes: typing.List,
                           meta) -> sly.Annotation:
    """
    This function changes the annotation labels for one sample. It iterates through all labels in one sample and if the label contains an object class
    specified by name in *input_classes*, this label is replaced by the object class named in *output_classes* at the index in *input_classes* list.
    :param annotation: annotations of one picture
    :param input_classes: list of object classes which have to be replaced
    :param output_classes: list of object classes which have to replace *input_classes*. It has to be in the same order has *input_class*.
                            Ex. input_classes : ["dog", "cat"]
                                output_classes : ["elephant", "horse"]
                                In this example, dog will be replaced by elephant and cat by horse.
    :param meta: meta of this project. It is useful to retrieve classes.
                 Warning: All object  class names specified in input and output have to be created before using this function else you will get one error.
    :return: annotations where some object classES will be replaced by others.
    """

    new_labels = []

    for label in annotation.labels:
        if label.obj_class.name in input_classes:
            index_cls = input_classes.index(label.obj_class.name)
            new_cls = output_classes[index_cls]

            new_obj_class = meta.obj_classes.get(new_cls)
            new_label = label.clone(obj_class=new_obj_class)

            new_labels.append(new_label)

        else:
            new_labels.append(label)

    return annotation.clone(labels=new_labels)


def remove_pt_ann(annotation: sly.Annotation) -> sly.Annotation:
    """
    Remove annotations which are just points. These annotations are recognizable because their area equals 1.
    """
    labels_2_keep = []
    for label in annotation.labels:
        if label.area == 1:
            pass
        else:
            labels_2_keep.append(label)

    return annotation.clone(labels=labels_2_keep)
