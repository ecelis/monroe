import os
import sys
import logging
import ConfigParser

import cpuinfo
import cv2
import vlc


if "X86_64" == cpuinfo.get_cpu_info()["arch"]:
    import getchar as interface


config = ConfigParser.ConfigParser()
face_cascade = None
video = None
stay_alive = True   # Keep the program running?
speaking = False    # Am I talking when I detect someone else prescence


def initialize():
    """Initialize program"""
    global video
    global face_cascade
    config.readfp(open('../config.ini'))
    face_cascade = cv2.CascadeClassifier("../"
            + config.get('DEFAULT','facexml'))
    video = cv2.VideoCapture(0)

def get_frame():
    """Capture frames from camera"""
    success, frame = video.read()
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

    faces = face_cascade.detectMultiScale(
            gray,
            scaleFactor=1.1,
            minNeighbors=5,
            minSize=(30, 30),
            flags=cv2.cv.CV_HAAR_SCALE_IMAGE
            )

    ## Draw a rectangle around faces
    for (x, y, w, h) in faces:
       cv2.rectangle(frame, (x, y), (x+w, y+h), (0, 255, 0), 2)

    #cv2.imshow('Video', frame)
    return frame


def jpeg_encode(frame):
    success, jpeg = cv2.imencode('.jpg', frame)

    return jpeg.tobytes()


def main():
    """Monroe waits for external sensors input and greet people"""

    log_init()                      # Initialize loging system
    logging.info("Starting")
    initialize()                    # Initilize global variables
    read = interface.read_input()

    while stay_alive:
        # Feel
        # Watch
        cv2.imshow('Video', get_frame())
        if cv2.waitKey(1) & 0xFF == ord('q'):
            exit(stay_alive)
            break

def exit(flag):
    """Exit the app"""
    if (stay_alive != True):
        video.release()
        cv2.destroyAllWindows()
        logging.info("Bye!")
        sys.exit(0)


def log_init():
    """Initialize log"""
    logging.basicConfig(filename="monroe.log", level=logging.DEBUG)


def play(audio):
    logging.info(audio)
    player = vlc.MediaPlayer(audio)
    player.play()



if __name__ == "__main__":
    main()
