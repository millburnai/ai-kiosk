import argparse
from timeit import default_timer as timer

import aisecurity
import cv2
import tensorflow as tf

parser = argparse.ArgumentParser()
parser.add_argument("--test", help="either test 'embed' or 'detect'", type=str, default="detect")
args = parser.parse_args()

print("Testing '{}'".format(args.test))

tf.Session(config=tf.ConfigProto(gpu_options=tf.GPUOptions(allow_growth=True))).__enter__()

width, height = 640, 360

if args.test == "embed":
    facenet = aisecurity.FaceNet()
elif args.test == "detect":
    aisecurity.face.detection.detector_init(min_face_size=int(0.5 * (width + height) / 2))
    # if min_face_size is not set to above, the detection speed decreases by 4x

cap = aisecurity.utils.visuals.get_video_cap(width, height, picamera=True, framerate=20, flip=0)

input("Press ENTER to continue: ")

while True:

    _, frame = cap.read()
    original_frame = frame.copy()

    start = timer()

    if args.test == "embed":
        facenet.embed(cv2.resize(frame, (160, 160)))

    elif args.test == "detect":
        cropped, face_coords = aisecurity.face.preprocessing.crop_face(frame, 10, face_detector="haarcascade")

        elapsed = timer() - start

        if face_coords != -1:
            aisecurity.utils.visuals.add_graphics(original_frame, face_coords, width, height, True, "[new person]", None, elapsed)
        else:
            print("No face detected")

    cv2.imshow("Detection test", original_frame)

    if cv2.waitKey(1) & 0xFF == ord("q"):
        break

cap.release()
cv2.destroyAllWindows()
