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

# EMBEDDING
def embed(img_dir, dump_path, verify=False):
    facenet = FaceNet(CONFIG_HOME + "/models/20180402-114759.pb")
    current_dir = os.getcwd()
    os.chdir(img_dir)
    os.mkdir("combined")
    for obj in os.listdir(img_dir):
        if not obj in ["combined", ".DS_Store"]:
            os.system("cp -R %s %s_ ; mv %s_/* combined ; rm -R %s_" % (4 * (obj,)))

    os.chdir(current_dir)
    os.system("sh divide.sh {} {}".format(img_dir+"/combined", 10))

    dump_and_embed(facenet, os.path.join(img_dir, "combined"), dump_path, encrypt=None,
                full_overwrite=True, mode="a")

    os.system("rm -R -f combined")

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

    parser = argparse.ArgumentParser()
    parser.add_argument("--img_dir", help="path to image directory", type=str)
    parser.add_argument("--dump_path", help="path to JSON file", type=str)
    parser.add_argument("--verify", help="run facial recognition with new data", type=to_bool)

    args = parser.parse_args()


    detector_init(min_face_size=250)
    embed("/Users/michaelpilarski/Desktop/parsed_images_copy", "/Users/michaelpilarski/Desktop/embeddings_.json", True)
