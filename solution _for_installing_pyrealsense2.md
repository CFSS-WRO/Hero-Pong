# This is the solution for installing pyrealsense2 library into Jetson Nano 

Normally, when we install library into our system, we can install it easily by using pip install

e.g, pip install numpy

However, when using pip install to install pyrealsense2 library, it cannot be installed successfully due to the following reason

1. PyPI lacks an ARM-compatible wheel
2. librealsense SDK isn’t pre-installed

In order to solve these problems, we have to build it from source
## Installation process
### step 1:
Registration of server's public key and install resources
1. sudo apt-key adv --keyserver keys.gnupg.net --recv-key F6E65AC044F831AC80A06380C8B3A55A6F3EFCDE || sudo apt-key adv --keyserver hkp://keyserver.ubuntu.com:80 --recv-key F6E65AC044F831AC80A06380C8B3A55A6F3EFCDE
2. $ sudo add-apt-repository "deb http://realsense-hw-public.s3.amazonaws.com/Debian/apt-repo bionic main" -u
3. $ sudo apt-get install librealsense2-utils
4. realsense-viewer

If you complete these steps successfully, you would be able to find a window that can view the information from the camera.

### step 2:
1. $ git clone https://github.com/IntelRealSense/librealsense.git
2. $ sudo apt-get install python3 python3-dev
3. $ mkdir build
4. $ cd build
5. $ cmake ../ -DBUILD_PYTHON_BINDINGS:bool=true -DPYTHON_EXECUTABLE=/usr/bin/python3.6
6. $ make -j5
7. $ sudo make install

If you completed the above step, you should be able to find a file containing the pyrealsense library

### step 3 
Move the file to site package
1. sudo mv (your pyrealsense library current location) (Python site-package folder)

### step 4
Run the Python script
import pyrealsense2 as rs
rs.__path__

If it is work, the file path should be shown
