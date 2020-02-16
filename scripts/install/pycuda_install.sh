#!/usr/bin/env bash

# sudo apt-get install ctags
# sudo apt-get install libboost-all-dev
# sudo apt-get install build-essential python-dev python-setuptools libboost-python-dev libboost-thread-dev -y
# sudo python3 -m pip install numpy

wget -O "pycuda-VERSION.tar.gz" https://files.pythonhosted.org/packages/5e/3f/5658c38579b41866ba21ee1b5020b8225cec86fe717e4b1c5c972de0a33c/pycuda-2019.1.2.tar.gz
if [ ! -d pycuda-VERSION ] ; then
    mkdir pycuda-VERSION && tar zxvf pycuda-VERSION.tar.gz -C pycuda-VERSION --strip-components 1
fi

cd pycuda-VERSION
python3 configure.py --cuda-root=/usr/local/cuda --cudadrv-lib-dir=/usr/lib --boost-inc-dir=/usr/include --boost-lib-dir=/usr/lib --boost-python-libname=boost_python-py36 --boost-thread-libname=boost_thread
make -j 4
sudo -H python3 setup.py install
sudo -H python3 -m pip install .
