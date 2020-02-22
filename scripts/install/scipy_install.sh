#!/usr/bin/env bash
# "scipy_install.sh": Download and build cmake, curl, and scipy from source

# prerequisites
sudo apt-get update
sudo apt-get install -y build-essential libatlas-base-dev gfortran libfreetype6-dev python3-setuptools qt4-qmake libqt4-dev

TMP=$HOME/temp_dir
mkdir $TMP

# curl for cmake
if [ ! -f "$TMP/curl-7.68.0.tar.gz" ] ; then
    wget https://curl.haxx.se/download/curl-7.68.0.tar.gz
fi
if [ ! -d "$TMP/curl-7.68.0" ] ; then
    mv curl-7.68.0.tar.gz $TMP
    cd $TMP
    tar xpvf curl-7.68.0.tar.gz
fi
cd $TMP/curl-7.68.0/
./configure --with--ssl
make
sudo make install

# cmake for scipy
if [ ! -f "$TMP/cmake-3.13.0.tar.gz" ] ; then
    wget http://www.cmake.org/files/v3.13/cmake-3.13.0.tar.gz
fi
if [ ! -d "$TMP/cmake-3.13.0" ] ; then
    mv cmake-3.13.0.tar.gz $TMP
    cd $TMP
    tar xpvf cmake-3.13.0.tar.gz
fi
cd $TMP/cmake-3.13.0/
./bootstrap --system-curl
make -j${nproc}
echo 'export PATH=/home/aisecurity/temp_dir/cmake-3.13.0/bin/:$PATH' >> $HOME/.bashrc
source $HOME/.bashrc

# scipy make and install
if [ ! -f "$TMP/scipy-1.3.3.tar.gz" ] ; then
    wget https://github.com/scipy/scipy/releases/download/v1.3.3/scipy-1.3.3.tar.gz
fi
if [ ! -d "$TMP/scipy-1.3.3" ] ; then
    mv scipy-1.3.3.tar.gz $TMP
    cd $TMP
    tar -xzvf scipy-1.3.3.tar.gz
fi
cd $TMP/scipy-1.3.3/
python3 setup.py install --user

# to fix curl system vs. custom build inconsistencies
sudo apt remove -y libcurl4
