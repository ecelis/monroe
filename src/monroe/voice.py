
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


class Voice:
    def __init__(self, config):
        self.tts_engine = pyttsx3.init()
        self.tts_engine.setProperty('voice',
            config.get('DEFAULT', 'voice', fallback='spanish-latin-am'))
        self.tts_engine.setProperty('rate', 95)

    def speak(self, utterance):
        self.tts_engine.say(utterance)
        self.tts_engine.runAndWait()
