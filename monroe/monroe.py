import os
import sys
import logging

import cpuinfo
import vlc


if "X86_64" == cpuinfo.get_cpu_info()["arch"]:
    import getchar as interface


def main():
    """Monroe waits for external sensors input and greet people"""

    log_init()
    logging.info("Starting")
    read = interface.read_input()

    stay_alive = True

    while stay_alive:
        try:
            flag = read()
            if flag == "/":
                exit(True)

            logging.info(flag)

        except Exception:
            sys.exit(0)


def exit(flag):
    """Exit the app"""
    if flag:
        logging.info("Bye!")
        sys.exit(0)


def log_init():
    """Initialize log"""
    logging.basicConfig(filename="monroe.log", level=logging.DEBUG)


def play(audio):
    p = vlc.MediaPlayer(audio)
    p.play()

if __name__ == "__main__":
    main()
