import os
import sys

import aisecurity
import tqdm

PATH_TO_IMGS = "/Volumes/SentryK300/parsed_images/all"
EMBED_FILE = "/Volumes/SentryK300/parsed_images/all"
MISSED_FILE = "/Volumes/SentryK300/"

class HidePrints(object):

    def __enter__(self):
        self.to_show = sys.stdout
        sys.stdout = open(os.devnull, "w")

    def __exit__(self, exc_type, exc_val, exc_tb):
        sys.stdout.close()
        sys.stdout = self.to_show


if __name__ == "__main__":
    data = {}
    missed =[]

    facenet = aisecurity.FaceNet()
    facenet.set_dist_metric("euclidean")

    aisecurity.face.detection.detector_init()

    all_imgs = os.listdir(PATH_TO_IMGS)
    os.chdir(PATH_TO_IMGS)

    with tqdm.trange(len(all_imgs)) as t:
        for person in all_imgs:
            with HidePrints():
                embed, face_coords = facenet.predict(person)

                if face_coords == -1:
                    embed, _ = facenet.predict(person, face_detector="haarcascade")

                    if face_coords == -1:
                        missed.append(person)
                        continue

                data[person] = embed

            t.update()

    with open(MISSED_FILE, "w+") as missed_file:
        for miss in missed:
            missed_file.write(miss + "\n")

    aisecurity.dataflow.data.dump_and_encrypt(data, dump_path=EMBED_FILE, encrypt=["names"])
