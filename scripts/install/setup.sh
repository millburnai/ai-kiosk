#!/usr/bin/env bash
# "setup.sh": Downloads and sets up all necssary packages for Jetson Nano

# ----- Update and upgrade -----
sudo apt update && sudo apt upgrade

# ----- Prerequisites -----
sudo apt install python3-pip
sudo -H python3 -m pip install Cython

# ----- Scientific dependencies -----
sudo -H python3 -m pip install numpy

sudo chmod +x *sh*
./scipy_install.sh
./pycuda_install.sh
./opencv_install.sh
# the above three lines will probably take 12+ hours

sudo -H python3 -m pip install keras pycryptodome tqdm

# ----- Hardware dependencies -----
sudo -H python3 -m pip install adafruit-circuitpython-charlcd

# ----- Database dependencies -----
sudo -H python3 -m pip install Pyrebase requests mysql-connector-python

# ----- Facial recognition and detection -----
sudo -H python3 -m pip install mtcnn --no-dependencies
cd $HOME
git clone "git+https://github.com/orangese/aisecurity.git@v0.9a"
cd aisecurity
sudo -H python3 -m pip install .
