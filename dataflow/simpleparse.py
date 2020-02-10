"""

"dataflow/simpleparse.py"

Data parsing?

"""

import argparse
from contextlib import contextmanager
import signal

# TIME LIMIT
# ... why do we need this?
class TimeoutException(Exception): pass

@contextmanager
def time_limit(seconds):
    def signal_handler(signum, frame):
        raise TimeoutException("Timed out!")

    signal.signal(signal.SIGALRM, signal_handler)
    signal.alarm(seconds)

    try:
        yield
    finally:
        signal.alarm(0)


if __name__ == "__main__":
    from aisecurity import FaceNet
    from aisecurity.data.dataflow import dump_embeds, retrieve_embeds
    from aisecurity.utils.paths import CONFIG_HOME
    from aisecurity.privacy.encryptions import *

    facenet = FaceNet(CONFIG_HOME + "/models/ms_celeb_1m.h5")

    parser = argparse.ArgumentParser()
    parser.add_argument("--img_dir", help="path to image directory", type=str)
    parser.add_argument("--dump_path", help="path to JSON file", type=str)
    parser.add_argument("--verify", help="how long to run face-rec test- default is 0", type=int, default=0)
    parser.add_argument("--dropbox_key", help="access key for dropbox account", type=str)

    def verify_data(dump_path, verify):
        facenet.set_data(retrieve_embeds(dump_path, encrypted=None))
        input("Running facial recognition with new data to verify: press enter")
        if verify:
            try:
                with time_limit(verify): 
                    facenet.real_time_recognize(logging=None)
            except TimeoutException:
                pass
        

    def send_to_dropbox():
        input("Send items? ({}, {}, {}".format(args.dump_path, CONFIG_HOME+"/keys/embedding_keys.txt", CONFIG_HOME+"/keys/name_keys.txt"))
        os.chdir(CONFIG_HOME+"/bin")
        os.system('sh dump_embeds.sh {} "/aisecurity/database/embeddings.txt" {}'.format(args.dropbox_key, args.dump_path))
        os.system('sh dump_embeds.sh {} "/aisecurity/keys/embedding_keys.txt" {}'.format(args.dropbox_key, CONFIG_HOME+"/keys/embedding_keys.txt"))
        os.system('sh dump_embeds.sh {} "/aisecurity/keys/name_keys.txt" {}'.format(args.dropbox_key, CONFIG_HOME+"/keys/name_keys.txt"))

    def embed(img_dir, dump_path, verify):
        dict_list = {}
        x = 0

        directories = lambda x: os.path.isdir(os.path.join(img_dir, x))

        for position, dir in enumerate(filter(directories, os.listdir(img_dir))):
            encrypted_data, no_faces = dump_embeds(facenet, os.path.join(img_dir, dir), dump_path,
                            full_overwrite=True, mode=("w+" if position == 0 else "a+"), ignore_encrypt="all")
            dict_list.update(encrypted_data)

        with open(dump_path, 'w+') as json_file:
            json.dump(dict_list, json_file, indent=4, ensure_ascii=False)

        if verify: 
            verify_data(dump_path, verify)

        send_to_dropbox()
    
    args = parser.parse_args()

    embed(args.img_dir, args.dump_path, args.verify)

