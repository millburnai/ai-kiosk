import aisecurity
import cv2

facenet = aisecurity.FaceNet()
cap = aisecurity.utils.visuals.get_video_cap(width=640, height=360, picamera=True, framerate=60, flip=0)

while True:

    _, frame = cap.read()

    start = time.time()
    facenet.predict_fn(frame)
    print("predict_fn time:", time.time() - start)

    cv2.imshow("predict_fn test", frame)

    if cv2.waitKey(1) & 0xFF == ord("q"):
        break

cap.release()
cv2.destroyAllWindows()
