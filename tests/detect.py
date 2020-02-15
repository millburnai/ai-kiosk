import time

import aisecurity
import cv2
from mtcnn import MTCNN
import tensorflow as tf

tf.Session(config=tf.ConfigProto(gpu_options=tf.GPUOptions(allow_growth=True))).__enter__()

# facenet = aisecurity.FaceNet()
mtcnn = MTCNN()
cap = aisecurity.utils.visuals.get_video_cap(width=640, height=360, picamera=False, framerate=60, flip=0)

input("Press ENTER to continue: ")

while True:

    _, frame = cap.read()

    resized = cv2.resize(frame, (160, 160))

    start = time.time()
    # facenet.predict(resized)
    mtcnn.detect_faces(resized)
    print("predict_fn time:", time.time() - start)

    cv2.imshow("predict_fn test", frame)

    if cv2.waitKey(1) & 0xFF == ord("q"):
        break

cap.release()
cv2.destroyAllWindows()
