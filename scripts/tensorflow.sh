sudo apt-get install libhdf5-serial-dev hdf5-tools libhdf5-dev zlib1g-dev zip libjpeg8-dev
sudo apt-get install python3-pip
sudo python3 -m pip install -U pip --user
sudo python3 -m pip install -U numpy grpcio absl-py py-cpuinfo psutil portpicker six mock requests gast h5py astor termcolor protobuf keras-applications keras-preprocessing wrapt google-pasta --user
sudo python3 -m pip install --pre --extra-index-url https://developer.download.nvidia.com/compute/redist/jp/v42 tensorflow-gpu==1.14.0+nv19.9 --user
sudo apt-get install git-all
sudo python3 -m pip install "git+https://github.com/orangese/easyai"
