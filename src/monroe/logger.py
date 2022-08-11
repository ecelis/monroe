
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

import logging
import os
import sys


def get(debug=False):
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
    return log
