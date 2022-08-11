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
import os
from pathlib import Path
import sys

from cpuinfo import get_cpu_info
import cv2

import logger
from voice import Voice


debug = False
try:
    debug = True if os.environ["DEBUG"] else False
except KeyError:
    pass

log = logger.get(debug)

if "X86_64" == get_cpu_info()["arch"]:  ## TODO I can't recall why I needed it
    import getchar as interface

config = configparser.ConfigParser()


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
    return (face_cc, video_capture)


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
            ## TODO research where this is now? flags=cv2.cv.CV_HAAR_SCALE_IMAGE
        )
        if debug:
            # Draw a rectangle around faces
            for (x, y, w, h) in faces:
                cv2.rectangle(frame, (x, y), (x+w, y+h), (0, 255, 0), 2)
    except:
        raise

    return frame


def listen_signal(read_keyboard_input):
    running = True  ## modify the main running flag in the return
    if (read_keyboard_input == ord('Q')
        or read_keyboard_input == ord('q')
        or read_keyboard_input == ord('/')):
        running = False
    elif read_keyboard_input == ord('.'):
        log.info("Shut up!")
        #player.stop()
    elif read_keyboard_input == ord('0'):
        #log.info("Hello %s" % (not tts_engine.isBusy()))
        #if tts_engine.isBusy():  # TODO use pyttsx3.isBusy()
         ## Initialize Text-to-Speech engine
        log.debug('hello 0')
        voice = Voice(config)
        # tts_engine = pyttsx3.init()
        # tts_engine.setProperty('voice',
        #     config.get('DEFAULT', 'voice', fallback='spanish-latin-am'))
        # tts_engine.setProperty('rate', 95)
        voice.speak("Hello")
        # tts_engine.runAndWait()
        # tts_engine.stop()
            # try:
            #     tts_engine.runAndWait()
            # except Exception:
            #     log.fatal(Exception)
            #     raise Exception
    elif read_keyboard_input == ord('1'):
        log.info("How are you?")
    elif read_keyboard_input == ord('2'):
        log.info("Good morning")
    elif read_keyboard_input == ord('3'):
        log.info("Good afternoon")
    elif read_keyboard_input == ord('4'):
        log.info("Good night")
    elif read_keyboard_input == ord('5'):
        log.info("Good bye")
    elif read_keyboard_input == ord('6'):
        log.info("Thank you")
    elif read_keyboard_input == ord('7'):
        log.info("Please")
    elif read_keyboard_input == ord('8'):
        log.info("You are welcome")
    elif read_keyboard_input == ord('9'):
        log.info("Excuse me")

    return running


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
    """Monroe waits for external sensors input and talks to people"""
    log.info("Starting")
    face_cc, video_capture = initialize()
    #vlc_instance = None
    #player = None
    running = True   # Is the program running?

    while running:
        # TODO Feel
        # Watch
        cv2.imshow('Video', get_frame(face_cc, video_capture))
        # Wait for input, TODO make it more generic loose from cv2
        read_keyboard_input = cv2.waitKey(1) & 0xFF
        if debug:
            log.debug("KEY: %s" % read_keyboard_input)
        running = listen_signal(read_keyboard_input)
        log.debug("I run %s" % running)
    
    exit(0 ,video_capture)

if __name__ == "__main__":
    main()
