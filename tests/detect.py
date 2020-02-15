from timeit import default_timer as timer

import aisecurity
import cv2
import tensorflow as tf

tf.Session(config=tf.ConfigProto(gpu_options=tf.GPUOptions(allow_growth=True))).__enter__()

width, height = 640, 360
cap = aisecurity.utils.visuals.get_video_cap(width, height, picamera=False, framerate=20, flip=0)

aisecurity.face.detection.detector_init(min_face_size=int(0.5 * (width + height) / 2))
# if min_face_size is not set to above, the detection speed decreases by 4x

input("Press ENTER to continue: ")

while True:

    _, frame = cap.read()
    original_frame = frame.copy()

    start = timer()

    cropped, face_coords = aisecurity.face.preprocessing.crop_face(frame, 10)

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
