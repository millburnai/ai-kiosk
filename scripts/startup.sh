#!/usr/bin/env bash

# Sets up SD card for usage in a kiosk

# Downloads and installs:
# 1. pip, Cython
# 2. tensorflow, cv2, scipy, sklearn, keras, (other scientific libraries)
# 3. adafruit-circuitpython-charlcd, Jetson.GPIO, (other hardware libraries)
# 4. Pyrebase, requests, (other db libraries)
# 5. mtcnn
# 6. aisecurity

# ----- Prerequisites -----
sudo apt install python3-pip
sudo python3 -m pip install Cython

# ----- Scientific dependencies -----
sudo bash tensorflow.sh
sudo apt install python3-opencv
sudo apt install python3-scipy
sudo apt install python3-sklearn
sudo python3 -m pip install keras pycryptodome tqdm

# ----- Hardware dependencies -----
sudo python3 -m pip install adafruit-circuitpython-charlcd

# ----- Database dependencies -----
sudo python3 -m pip install Pyrebase requests mysql-connector-python

# ----- Facial recognition and detection -----
sudo python3 -m pip install mtcnn --no-dependencies --user
sudo python3 -m pip install "git+https://github.com/orangese/aisecurity.git@v0.9a" --no-dependencies --user
