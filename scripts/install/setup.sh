#!/usr/bin/env bash
# "setup.sh": Downloads and sets up all necssary packages for Jetson Nano

# ----- Assertions -----
if [ ! -d /home/aisecurity ] ; then
  exit 1
fi

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

sudo apt install libhdf5-serial-dev hdf5-tools libhdf5-dev zlib1g-dev zip libjpeg8-dev
sudo -H python3 -m install grpcio absl-py py-cpuinfo psutil portpicker six mock requests gast h5py astor termcolor protobuf keras-applications keras-preprocessing wrapt google-pasta
sudo -H python3 -m pip install --pre --extra-index-url https://developer.download.nvidia.com/compute/redist/jp/v43 tensorflow-gpu==1.15.0+nv20.1
sudo -H python3 -m pip install keras pycryptodome tqdm

# ----- Hardware dependencies -----
sudo -H python3 -m pip install adafruit-circuitpython-charlcd

# ----- Database dependencies -----
sudo -H python3 -m pip install Pyrebase requests mysql-connector-python websocket

# ----- Facial recognition and detection -----
sudo -H python3 -m pip install mtcnn --no-dependencies
cd $HOME
git clone "git+https://github.com/orangese/aisecurity.git@v0.9a"
cd aisecurity
sudo -H python3 -m pip install .

# ----- Download ~/.aisecurity files -----
cd $HOME
sudo python3 -c "import aisecurity"
sudo cp -a .aisecurity /root/.aisecurity

# ----- Set up rc.local -----
git clone "git+https://github.com/aisecurity/ai-kiosk.git"
sudo cp ai-kiosk/scripts/rc.local /etc/rc.local

sudo chmod +x ai-kiosk/production/recognition.py
sudo chmod +x /etc/rc.local

sudo systemctl enable rc-local
