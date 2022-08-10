# monroe

## Setup

Certain files are required. In a linux/mac system make sure to have teh following files in your `$HOME` directory.

**config.ini**

It configures which camera and the XML for the model for face detection.

```
[DEFAULT]
facexml=haarcascade_frontalface_default.xml
camera=0
```

## Run

Anaconda is the suggested way. However there a few packages not available and you need to install those with `pip`.

```
conda create --name monroe
conda activate monroe
conda install --file conda-requirements.txt
pip install -r requirements.txt
cd monroe/monroe
python monroe.py
```

## Dependencies

### Python packages

- numpy
- opencv-python
- pyttsx3
- py-cpuinfo

### OpenCV

There are several options

#### Build from source in Ubuntu 22.04

##### Ubuntu 22.04 Dependencies
```
sudo apt install build-essential cmake libgtkglext1 libgtkglext1-dev
```

##### Build
```
cd opencv
mkdir Release
cd Release
cmake -D CMAKE_BUILD_TYPE=RELEASE \
  -D CMAKE_INSTALL_PREFIX=/usr/local \
  -D WITH_TBB=ON -D BUILD_NEW_PYTHON_SUPPORT=ON \
  -D WITH_V4L=ON -D INSTALL_C_EXAMPLES=ON \
  -D INSTALL_PYTHON_EXAMPLES=ON -D BUILD_EXAMPLES=ON \
  -D WITH_QT=ON -D WITH_GTK=ON -D WITH_OPENGL=ON ..
```

TODO maybe the next is not required anymore.

Copy OpenCV files to virtualenv directory.

```
cp opencv/Release/lib/cv2.so monroe/ENV/lib/python2.7/site-packages
cp opencv/Release/lib/cv.py monroe/ENV/lib/python2.7/site-packages
```

### VLC

Download and install [VLC](https://www.videolan.org), a copy o VLC python
binding is included along with monroe source code.

TODO Feed to VLC?

```
python monroe.py | cvlc --demux=rawvideo --rawvid-fps=25 \
  --rawvid-width=720 --rawvid-height=480  \
  --rawvid-chroma=RV24 - \
  --sout "#transcode{vcodec=h264,vb=200,fps=25,width=720,height=480}:rtp{dst=0.0.0.0,port=8081,sdp=rtsp://0.0.0.0:8081/test.sdp}" \
```

## Hardware

TODO I can't recall what this was for.

TODO Check [here](https://circuitsgeek.com/guides-and-how-to/raspberry-pi-ultrasonic-sensor-hc-sr04-interface-tutorial/)

* [HC-sr04](https://www.amazon.com/Arrela%C2%AE-Hc-sr04-Ultrasonic-Distance-Measuring/dp/B00KKKT7YK)
* R1 - 1 1k Ohm resistor
* R2 - 1 2.2k Ohm resistor

### Electronic Diagram

```
   |
   |-GND--------------------------------------------------GPIO GND [Pin 6]
H  |                                                   |
C  |-ECHO---R1 [1k]--GPIO 26 [Pin 37]---R2 [2Pin 2.2k]---
-  |
s  |-TRIG------------GPIO 20 [Pin 38]
r  |
0  |-Vcc-------------GPIO 5v [Pin 2]
4  |
```
