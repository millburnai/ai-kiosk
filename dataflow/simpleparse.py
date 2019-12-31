if __name__ == "__main__":

    import os
    import json
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

    parser = argparse.ArgumentParser()
    parser.add_argument("--img_dir", help="path to image directory", type=str)
    parser.add_argument("--dump_path", help="path to JSON file", type=str)
    parser.add_argument("--verify", help="run facial recognition with new data", type=bool, default=False)
    parser.add_argument("--dropbox_key", help="access key for dropbox account", type=str)

    def verify_data(dump_path):
        facenet.set_data(retrieve_embeds(dump_path, encrypted=None))
        input("Running facial recognition with new data to verify: press enter")
        facenet.real_time_recognize(logging=None, pre_recorded_file='/Users/michaelpilarski/Desktop/test_movie.mov')

    def send_to_dropbox():
        input("Send items? ({}, {}, {}".format(args.dump_path, CONFIG_HOME+"/keys/embedding_keys.txt", CONFIG_HOME+"/keys/name_keys.txt"))
        os.chdir(CONFIG_HOME+"/bin")
        os.system('sh dump_embeds.sh {} "/aisecurity/database/embeddings(12/30/31).txt" {}'.format(args.dropbox_key, args.dump_path))
        os.system('sh dump_embeds.sh {} "/aisecurity/keys/embedding_keys(12/30/31).txt {}'.format(args.dropbox_key, CONFIG_HOME+"/keys/embedding_keys.txt"))
        os.system('sh dump_embeds.sh {} "/aisecurity/keys/name_keys(12/30/31).txt {}'.format(args.dropbox_key, CONFIG_HOME+"/keys/name_keys.txt"))

    def embed(img_dir, dump_path, verify=False):
        dict_list = {}
        x = 0
        for dir in os.listdir(img_dir):
            if os.path.isdir(os.path.join(img_dir, dir)):
                encrypted_data, no_faces = dump_embeds(facenet, os.path.join(img_dir, dir), dump_path,
                            full_overwrite=True, mode=("w+" if x == 0 else "a+"), ignore_encrypt="all")
                dict_list.update(encrypted_data)
                x+=1
        with open(dump_path, 'w+') as json_file:
            json.dump(dict_list, json_file, indent=4, ensure_ascii=False)

        if verify: 
            verify_data(dump_path)

        send_to_dropbox()

    args = parser.parse_args()

    embed(args.img_dir, args.dump_path, args.verify)

