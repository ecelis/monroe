"""
Copyright 2017 - 2022 Ernesto Angel Celis de la Fuente

Licensed under the Apache License, Version 2.0 (the "License");
you may not use this file except in compliance with the License.
You may obtain a copy of the License at

    http://www.apache.org/licenses/LICENSE-2.0

Unless required by applicable law or agreed to in writing, software
distributed under the License is distributed on an "AS IS" BASIS,
WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
See the License for the specific language governing permissions and
limitations under the License."""

import configparser
import logging
import os
from pathlib import Path
import sys

from cpuinfo import get_cpu_info
import cv2
import pyttsx3

if "X86_64" == get_cpu_info()["arch"]:  ## TODO I can't recall why I needed it
    import getchar as interface


config = configparser.ConfigParser()

debug = False
try:
    debug = True if os.environ["DEBUG"] else False
except KeyError:
    pass

logging_level = logging.DEBUG if debug else logging.INFO
FORMAT = logging.Formatter('%(asctime)-15s %(message)s')
log = logging.getLogger()
log.setLevel(logging_level)
sh = logging.StreamHandler(sys.stdout)
sh.setFormatter(FORMAT)
log.addHandler(sh)
fh = logging.FileHandler(filename=os.environ['HOME'] + "/monroe.log")
fh.setFormatter(FORMAT)
log.addHandler(fh)


def initialize():
    """Initialize program"""
    ## Initialize ~/.config/monroe
    config_dir = str(Path.home().joinpath('.config', 'monroe'))
    os.makedirs(config_dir, exist_ok=True)
    config_file = Path.home().joinpath(config_dir, 'config.ini')
    config_list = config.read(config_file)
    
    ## Check for the required files to be in place
    if len(config_list) < 1:
        msg = "File %s not found." % config_file
        log.critical(msg)
        raise Exception(msg)
    face_cc_xml = str(Path.home().joinpath(config_dir,
        config.get('DEFAULT', 'facexml')))
    if(not Path(face_cc_xml).is_file()):
        msg = "File %s not found!" % face_cc_xml
        raise FileNotFoundError(msg)

    ## Load the Face Cascade Classifier model
    face_cc = cv2.CascadeClassifier(face_cc_xml)

    ## Initialize Text-to-Speech engine
    tts_engine = pyttsx3.init()
    tts_engine.setProperty('voice',
        config.get('DEFAULT', 'voice', fallback='spanish-latin-am'))
    tts_engine.setProperty('rate', 95)

    ## Initialize camera
    video_capture = cv2.VideoCapture(0)
    
    # TODO I can't recall why I wanted VLC
    # # Create basic VLC instance
    # vlc_instance = vlc.Instance()
    # # Create VLC player
    # player = vlc_instance.media_player_new()
    # # TODO Make it load a playlist and set it up to play random
    # promos = vlc_instance.media_new("file://"
    #                                 + os.environ["HOME"] + "/01.ogg")
    # player.set_media(promos)
    return (face_cc, tts_engine, video_capture)

def get_frame(face_cc, video_capture):
    """Capture frames from camera"""
    if video_capture.isOpened():
        success, frame = video_capture.read()
    else:
        success = False
        #stay_alive = success  ## TODO maybe stay_aliv isn't required

    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

    try:
        faces = face_cc.detectMultiScale(
            gray,
            scaleFactor=1.1,
            minNeighbors=5,
            minSize=(30, 30),
            ## TODO research where this is  nowflags=cv2.cv.CV_HAAR_SCALE_IMAGE
        )
        if debug:
            # Draw a rectangle around faces
            for (x, y, w, h) in faces:
                cv2.rectangle(frame, (x, y), (x+w, y+h), (0, 255, 0), 2)
    except:
        raise

    return frame


def amIspeaking(speaking):
    if speaking == True:
        log.debug("I'am currently talking")
        return speaking
    else:
        speaking = True
        return False


def listen_signal(read_keyboard_input, speaking, tts_engine):
    running = True  ## modify the main running flag in the return
    if (read_keyboard_input == ord('Q')
        or read_keyboard_input == ord('q')
        or read_keyboard_input == ord('/')):
        running = False
    elif read_keyboard_input == ord('.'):
        log.info("Shut up!")
        tts_engine.stop()
        #player.stop()
        speaking = False
    elif read_keyboard_input == ord('1'):
        log.info("Shout out!")
        #shout_out()
    elif read_keyboard_input == ord('2'):
        log.info("Say something")
        if False == amIspeaking():
            tts_engine.say("Hola mundo!")
            tts_engine.runAndWait()
            speaking = False

    return (running, speaking)


def jpeg_encode(frame):
    success, jpeg = cv2.imencode('.jpg', frame)

    return jpeg.tobytes()


# def shout_out(snd_file=None):
#     """Say something"""
#     if False == amIspeaking():
#         if (snd_file != None):
#             speech = vlc_instance.media_new(snd_file)
#             player.set_media(speech)

#         player.play()
#         speaking = False


def exit(flag, video_capture):
    """Exit the app"""
    #if (not running):
    video_capture.release()
    cv2.destroyAllWindows()
    log.info("Bye!")
    sys.exit(flag)


def main():
    """Monroe waits for external sensors input and greet people"""
    log.info("Starting")
    face_cc, tts_engine, video_capture = initialize()
    #vlc_instance = None
    #player = None
    running = True   # Is the program running>
    speaking = False    # Am I talking when I detect someone else prescence?

    while running:
        # TODO Feel
        # Watch
        cv2.imshow('Video', get_frame(face_cc, video_capture))
        # Wait for input, TODO make it more generic loose from cv2
        read_keyboard_input = cv2.waitKey(1) & 0xFF
        if debug:
            log.debug("KEY: %s" % read_keyboard_input)
        running, speaking = listen_signal(read_keyboard_input, speaking,
            tts_engine)
    
    exit(0 ,video_capture)

if __name__ == "__main__":
    main()
