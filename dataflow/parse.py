"""

"parse.py"

Parses image data.

"""

import argparse
import functools
import os
import shutil
import re
import warnings

from aisecurity import FaceNet
from aisecurity.dataflow.loader import dump_and_embed, retrieve_embeds
from aisecurity.utils.paths import CONFIG_HOME
from aisecurity.face.detection import detector_init


# HELPERS
def restore_cwd(func):
    @functools.wraps(func)
    def _func(*args, **kwargs):
        cwd = os.getcwd()
        result = func(*args, **kwargs)
        os.chdir(cwd)
        return result

    return _func


# METADATA PARSING
def parse_index(index_path):

    INDEXES = {
        "grade": 1,
        "img": 2,
        "first_name": 5,
        "last_name": 4,
        "id": -1
    }

    people = {}

    with open(index_path, "r") as file:
        for line in file:
            person = line.split()

            img_path = os.path.join(person[INDEXES["grade"]], person[INDEXES["img"]])
            name = person[INDEXES["first_name"]].lower() + "_" + person[INDEXES["last_name"]].lower()
            student_id = person[INDEXES["id"]]

            people[img_path] = [student_id, name]

    return people


def get_info(item, people):
    construct_dict = lambda d, idx: dict(zip(d.keys(), list(zip(*d.values()))[idx]))

    if item == "ids":
        return construct_dict(people, 0)
    elif item == "names":
        return construct_dict(people, 1)
    else:
        raise ValueError("only 'id' and 'names' are valid arguments")


# IMAGE RENAMING
@restore_cwd
def rename_imgs(img_dir, identifiers, new_img_dir=None):
    def split(string):
        # https://stackoverflow.com/questions/29916065/how-to-do-camelcase-split-in-python
        matches = re.finditer('.+?(?:(?<=[a-z])(?=[A-Z])|(?<=[A-Z])(?=[A-Z][a-z])|$)', string)
        return [m.group(0) for m in matches]

    assert new_img_dir is not None, "please specify a new_img_dir for backup concerns"
    os.chdir(img_dir)

    # underclassmen
    for img_path in identifiers:
        if "_" not in img_path:
            try:
                if new_img_dir is not None:
                    new_path = os.path.join(new_img_dir, img_path.split("/")[0], identifiers[img_path] + ".jpg")
                    shutil.copy(img_path, new_path)
                else:
                    new_path = os.path.join(img_path.split("/")[0], identifiers[img_path] + ".jpg")
                    os.rename(img_path, new_path)
            except FileNotFoundError:
                print("{} not found".format(img_path))

    print("Underclassmen parsed")

    # seniors
    try:
        os.chdir("12")

        for img_path in os.listdir(os.getcwd()):
            if "_" not in img_path and img_path.endswith(".jpg") or img_path.endswith(".png"):
                name = split(img_path)
                name = name[1].lower().strip(".jpg") + "_" + name[0].lower() + ".jpg"

                if new_img_dir is not None:
                    new_path = os.path.join(new_img_dir, "12", name)
                    shutil.copy(img_path, new_path)
                else:
                    new_path = os.path.join(img_dir, "12", name)
                    os.rename(img_path, new_path)

        print("Seniors parsed")

    except FileNotFoundError:
        warnings.warn("senior directory not found (should be named '12')")


# EMBEDDING
def embed(img_dir, dump_path, verify=False):
    facenet = FaceNet(CONFIG_HOME + "/models/20180402-114759.pb")
    for obj in os.listdir(img_dir):
        if os.path.isdir(os.path.join(img_dir, obj)):
            dump_and_embed(facenet, os.path.join(img_dir, obj), dump_path, encrypt=None,
                        full_overwrite=True, mode="a")

    if verify:
        print("Running facial recognition with new data to verify")
        print(dump_path)
        facenet.set_data(retrieve_embeds(dump_path, encrypted=None))
        facenet.real_time_recognize(logging=None)


if __name__ == "__main__":
    # ARGPARSE
    def to_bool(string):
        if string.lower() in ("yes", "true", "t", "y", "1"):
            return True
        elif string.lower() in ("no", "false", "f", "n", "0"):
            return False
        else:
            raise argparse.ArgumentTypeError("boolean value expected")
    '''
    parser = argparse.ArgumentParser()
    parser.add_argument("--index_path", help="path to index file", type=str)
    parser.add_argument("--img_dir", help="path to image directory", type=str)
    parser.add_argument("--new_img_dir", help="path to new image directory (default: [img_dir])", type=str)
    parser.add_argument("--dump_path", help="path to JSON file", type=str)
    parser.add_argument("--filename_type", help="name images using names or IDs (default: names)", type=str,
                        default="names")
    parser.add_argument("--verify", help="run facial recognition with new data", type=to_bool)

    args = parser.parse_args()

    if args.new_img_dir is None:
        args.new_img_dir = args.img_dir

    # ACTUAL STUFF
    people = parse_index(args.index_path)
    rename_imgs(args.img_dir, get_info(args.filename_type, people), new_img_dir=args.new_img_dir)
    embed(args.new_img_dir, args.dump_path, verify=args.verify)
    '''
    detector_init(min_face_size=250)
    embed("/Users/michaelpilarski/Desktop/parsed_images_copy", "/Users/michaelpilarski/Desktop/embeddings_.json", True)
