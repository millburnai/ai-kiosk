import os
import sys

import aisecurity
import cv2
import tqdm

PATH_TO_IMGS = "/Users/ryan/tmp/all"#"/Volumes/SentryK300/parsed_images/all"
EMBED_FILE = "/Users/ryan/tmp/all/embed.json"#/Volumes/SentryK300/parsed_images/all"
MISSED_FILE = "/Users/ryan/tmp/missed.txt"#"/Volumes/SentryK300/"

class HidePrints(object):

    def __enter__(self):
        self.to_show = sys.stdout
        sys.stdout = open(os.devnull, "w")

    def __exit__(self, exc_type, exc_val, exc_tb):
        sys.stdout.close()
        sys.stdout = self.to_show


if __name__ == "__main__":
    imgs = {}
    data = {}
    missed = []

    # gather imagfes
    all_files = [os.path.join(PATH_TO_IMGS, img) for img in os.listdir(PATH_TO_IMGS)]
    all_imgs = list(filter(lambda file: file.endswith("jpg") or file.endswith("png"), all_files))

    print("Gathering images...")
    with tqdm.trange(len(all_imgs)) as t:
        for person in all_imgs:
            img = cv2.imread(person)

            if img is not None:
                imgs[person] = img[:, :, ::-1]
            else:
                missed.append(person)
                print("'{}' could not be read".format(person))

            t.update()

    # set up facenet
    facenet = aisecurity.FaceNet()
    facenet.set_dist_metric("euclidean")

    aisecurity.face.detection.detector_init()

    # run embedding
    print("Running embedding...")
    with tqdm.trange(len(imgs)) as t:
        for person, img in imgs.items():
            with HidePrints():
                embed, face_coords = facenet.predict(img)

                if face_coords == -1:
                    try:
                        embed, _ = facenet.predict(img, face_detector="haarcascade")
                        if face_coords == -1:
                            raise AssertionError()
                    except (cv2.error, AssertionError):
                        missed.append(person)
                        continue

                data[person] = embed

            t.update()

    with open(MISSED_FILE, "w+") as missed_file:
        for miss in missed:
            missed_file.write(miss + "\n")

    aisecurity.dataflow.data.dump_and_encrypt(data, dump_path=EMBED_FILE, encrypt=["names"])
