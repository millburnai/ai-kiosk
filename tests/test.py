import cv2



z = []
v = []

import aisecurity
facenet=aisecurity.FaceNet("/Users/michaelpilarski/.aisecurity/models/20180402-114759.pb", sess=True)
aisecurity.face.detection.detector_init(min_face_size=250)
for i in range(20):
	x = cv2.imread('/Users/michaelpilarski/Desktop/Keshab.png')
	print(x)
	facenet.predict(x)
