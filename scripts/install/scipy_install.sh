# sudo apt remove python3-numpy
# sudo apt remove python3-scipy
# sudo apt remove python3-sklearn

# sudo python3 -m pip uninstall numpy scipy
# sudo python3 -m pip uninstall sklearn
# sudo python3 -m pip uninstall scikit-learn

# sudo python3 -m pip install numpy

sudo apt-get update
# sudo apt-get install -y build-essential libatlas-base-dev gfortran libfreetype6-dev python3-setuptools

wget http://www.cmake.org/files/v3.13/cmake-3.13.0.tar.gz
tar xpvf cmake-3.13.0.tar.gz cmake-3.13.0/
cd cmake-3.13.0/
./bootstrap --system-curl
make -j8
echo 'export PATH=/home/nvidia/cmake-3.13.0/bin/:$PATH' >> ~/.bashrc
source ~/.bashrc

# wget https://github.com/scipy/scipy/releases/download/v1.3.3/scipy-1.3.3.tar.gz
# tar -xzvf scipy-1.3.3.tar.gz scipy-1.3.3
cd scipy-1.3.3/
python3 setup.py install --user
