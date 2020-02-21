"""

Will be filled in later once I retrieve the code from the Jetson Nano.

"""

import aisecurity

facenet = aisecurity.FaceNet("/home/aisecurity/.aisecurity/models/ms_celeb_1m.engine")
facenet.real_time_recognize(use_picam=True, flip=0, data_mutability=0, use_graphics=False)
