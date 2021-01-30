import aisecurity
import cv2
import tensorflow as tf

gstreamer_pipeline = ("nvarguscamerasrc ! video/x-raw(memory:NVMM), width=(int)1280, height=(int)720, "
                                  "format=(string)NV12, framerate=(fraction)30/1 ! nvvidconv flip-method=2 ! "
                                  "video/x-raw, width=(int){}, height=(int){}, format=(string)BGRx ! videoconvert ! "
                                  "video/x-raw, format=(string)BGR ! appsink").format(640, 360)

tf.Session(config=tf.ConfigProto(gpu_options=tf.GPUOptions(allow_growth=True))).__enter__()
#cap = cv2.VideoCapture(0) #aisecurity.utils.visuals.Camera()
detector = aisecurity.face.detection.FaceDetector("trt-mtcnn")
cap = cv2.VideoCapture(gstreamer_pipeline, cv2.CAP_GSTREAMER)

while True:
    _, frame = cap.read()

    face, _ = detector.crop_face(frame, 10)
    cv2.imshow("MTCNN test", frame)
    if cv2.waitKey(1) & 0xFF == ord("q"):
        break
