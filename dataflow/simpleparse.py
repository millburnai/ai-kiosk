
import os
import json

def embed(img_dir, dump_path, error_path, verify=False):
    dict_list = {}
    x = 0
    for dir in os.listdir(img_dir):
        print(dir)
        if os.path.isdir(os.path.join(img_dir, dir)):
            print("dumdum")
            encrypted_data, no_faces = dump_embeds(facenet, os.path.join(img_dir, dir), dump_path,
                        full_overwrite=True, mode=("w+" if x == 0 else "a+"), ignore_encrypt="all")
            dict_list.update(encrypted_data)

            print("oops")
            x+=1

    print(os.listdir(img_dir))
    with open(dump_path, 'w') as json_file:
        json.dump(dict_list, json_file, indent=4, ensure_ascii=False)

    if verify: 
        verify_data(dump_path)

def verify_data(dump_path):
    print("Running facial recognition with new data to verify")
    facenet.set_data(retrieve_embeds(dump_path, encrypted=None))
    input("ISO: Press Enter")
    facenet.real_time_recognize(logging=None, pre_recorded_file='/Users/michaelpilarski/Desktop/movie.mov', False)

import argparse
import functools
import os
import shutil
import re
import warnings

from aisecurity import FaceNet
from aisecurity.data.dataflow import dump_embeds, retrieve_embeds
from aisecurity.utils.paths import CONFIG_HOME
from aisecurity.privacy.encryptions import *

facenet = FaceNet(CONFIG_HOME + "/models/ms_celeb_1m.h5")


print(os.getcwd())
os.chdir(flash_drive)

embed("parsed_images", "embeddings.txt", "missed_frames.txt", True)

verify_data("embeddings.txt")
