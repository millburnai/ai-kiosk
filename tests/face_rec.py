import aisecurity

facenet = aisecurity.FaceNet()
facenet.real_time_recognize(detector="trt-mtcnn")
