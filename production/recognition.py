"""

Production facial recognition script. Called on startup by /etc/rc.local

"""

import signal

from aisecurity import FaceNet


def recognize(facenet, sec):

    def handler(signum, frame):
        raise Exception("{}s have elapsed, killing process".format(sec))

    def _recognize(facenet):
        facenet.real_time_recognize(use_picam=True, socket=True, flip=0, data_mutability=True, use_graphics=True)

    signal.signal(signal.SIGALRM, handler)
    signal.alarm(sec)

    try:
        _recognize(facenet)
    except Exception as e:
        print(e)

if __name__ == "__main__":
    facenet = FaceNet()
    recognize(facenet, sec=100)
    #facenet.real_time_recognize(use_picam=True, socket=True, flip=0, data_mutability=0, use_graphics=True)
