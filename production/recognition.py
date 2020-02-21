"""

Production facial recognition script. Called on startup by /etc/rc.local

"""

import functools
import multiprocessing

import aisecurity

def timeout(sec):
    def _timeout(func):
        @functools.wraps(func)
        def _func(*args, **kwargs):
            p = multiprocessing.Process(target=bar, args=args, kwargs=kwargs)
            p.start()

            p.join(sec)

            if p.is_alive():
                print("Killing func after {} seconds".format(sec))

                p.terminate()
                p.join()

@timeout(sec=10)
def recognize(facenet):
    facenet.real_time_recognize(use_picam=True, flip=0, data_mutability=0, use_graphics=False)


if __name__ == "__main__":
    facenet = aisecurity.FaceNet("/home/aisecurity/.aisecurity/models/ms_celeb_1m.engine")
    recognize(facenet)
