
import os

def embed(img_dir, dump_path, verify=False):
    facenet = FaceNet(CONFIG_HOME + "/models/ms_celeb_1m.h5")
    x = 0
    for dir in os.listdir(img_dir):
        print(dir)
        if os.path.isdir(os.path.join(img_dir, dir)):
            print("dumdum")
            dump_embeds(facenet, os.path.join(img_dir, dir), dump_path,
                        full_overwrite=True, mode=("w+" if x == 0 else "a+"), ignore_encrypt="embeddings")

            print("oops")
            x+=1
    print(os.listdir(img_dir))

    if verify:
        print("Running facial recognition with new data to verify")
        facenet.set_data(retrieve_embeds(dump_path, encrypted="names"))
        facenet.real_time_recognize(logging=None)

import argparse
import functools
import os
import shutil
import re
import warnings

from aisecurity import FaceNet
from aisecurity.data.dataflow import dump_embeds, retrieve_embeds
from aisecurity.utils.paths import CONFIG_HOME


print(os.getcwd())
os.chdir("/Users/michaelpilarski/Desktop/photos")

embed("parsed_images", "embeds", True)

