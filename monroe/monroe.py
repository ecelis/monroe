import configparser
import logging
import os
from pathlib import Path
import sys

from cpuinfo import get_cpu_info
import cv2
import pyttsx3
import vlc


if "X86_64" == get_cpu_info()["arch"]:
    import getchar as interface


config = configparser.ConfigParser()
tts_engine = None
face_cascade = None
video = None
vlc_instance = None
player = None
stay_alive = True   # Keep the program running?
speaking = False    # Am I talking when I detect someone else prescence


def initialize():
    """Initialize program"""
    global video
    global vlc_instance
    global tts_engine
    global player
    global face_cascade

    base_path = Path(__file__).parent
    config.read((base_path / '../config.ini').resolve())
    
    ## Initialize Text-to-Speech engine
    tts_engine = pyttsx3.init()
    tts_engine.setProperty('voice', 'spanish-latin-am')
    tts_engine.setProperty('rate', 95)

    ## Initialize camera
    video = cv2.VideoCapture(0)
    
    face_cascade = cv2.CascadeClassifier("../"
        + config.get('DEFAULT', 'facexml'))
    # Create basic VLC instance
    vlc_instance = vlc.Instance()
    # Create VLC player
    player = vlc_instance.media_player_new()
    # TODO Make it load a playlist and set it up to play random
    promos = vlc_instance.media_new("file://"
                                    + os.environ["HOME"] + "/01.ogg")
    player.set_media(promos)


def get_frame():
    """Capture frames from camera"""
    if video.isOpened():
        success, frame = video.read()
    else:
        success = False
        stay_alive = success  ## TODO maybe stay_aliv isn't required

    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

    faces = face_cascade.detectMultiScale(
        gray,
        scaleFactor=1.1,
        minNeighbors=5,
        minSize=(30, 30),
        ## TODO research where this is  nowflags=cv2.cv.CV_HAAR_SCALE_IMAGE
    )

    # Draw a rectangle around faces
    for (x, y, w, h) in faces:
        cv2.rectangle(frame, (x, y), (x+w, y+h), (0, 255, 0), 2)

    return frame


def jpeg_encode(frame):
    success, jpeg = cv2.imencode('.jpg', frame)

    return jpeg.tobytes()


def main():
    """Monroe waits for external sensors input and greet people"""
    global speaking
    global stay_alive
    log_init()                      # Initialize loging system
    logging.info("Starting")
    initialize()                    # Initilize global variables
    # read = interface.read_input() TODO replace it for something else

    while stay_alive:
        # Feel
        # Watch
        cv2.imshow('Video', get_frame())
        # Wait for input, TODO make it more generic loose from cv2
        r_input = cv2.waitKey(1) & 0xFF
        if r_input == ord('/'):
            stay_alive = False
            exit(stay_alive)
            break
        elif r_input == ord('.'):
            logging.info("Shut up!")
            tts_engine.stop()
            player.stop()
            speaking = False
        elif r_input == ord('1'):
            logging.info("Shout out!")
            shout_out()
        elif r_input == ord('2'):
            logging.info("Say something")
            if False == amIspeaking():
                tts_engine.say("Hola mundo!")
                tts_engine.runAndWait()
                speaking = False


def amIspeaking():
    global speaking
    if speaking == True:
        logging.info("I'am currently talking")
        return speaking
    else:
        speaking = True
        return False


def shout_out(snd_file=None):
    """Say something"""
    if False == amIspeaking():
        if (snd_file != None):
            speech = vlc_instance.media_new(snd_file)
            player.set_media(speech)

        player.play()
        speaking = False


def exit(flag):
    """Exit the app"""
    if (stay_alive != True):
        video.release()
        cv2.destroyAllWindows()
        logging.info("Bye!")
        sys.exit(0)


def log_init():
    """Initialize log"""
    FORMAT = '%(asctime)-15s %(message)s'
    logging.basicConfig(filename=os.environ['HOME'] + "/monroe.log",
                        level=logging.DEBUG,
                        format=FORMAT)


if __name__ == "__main__":
    main()
