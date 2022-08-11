
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

import os
from pathlib import Path
import sys

import pyttsx3

import logger

debug = False
try:
    debug = True if os.environ["DEBUG"] else False
except KeyError:
    pass

log = logger.get(debug)


class Voice:
    def __init__(self, config):
        log.debug("TTS engine start")
        self.tts_engine = pyttsx3.init()
        self.tts_engine.setProperty('voice',
            config.get('DEFAULT', 'voice', fallback='spanish-latin-am'))
        self.tts_engine.setProperty('rate', 95)
        self.tts_engine.connect('started-utterance', self.onStart)
        self.tts_engine.connect('finished-utterance', self.onEnd)

    def onStart(self, name):
        log.debug("Starting utterance: %s" % name)

    def onEnd(self, name, completed):
        log.debug("Utterance ended: %s as %s" % (name, completed))
        self.tts_engine.endLoop()

    def speak(self, utterance, name):
        self.tts_engine.say(utterance, name)
        self.tts_engine.startLoop()
        #self.tts_engine.runAndWait()
