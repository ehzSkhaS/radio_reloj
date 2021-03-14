import time
import pygame as gm
import importlib.util
from functools import lru_cache

try:
    importlib.util.find_spec('RPi.GPIO')
    import RPi.GPIO as GPIO
except ImportError:
    import FakeRPi.GPIO as GPIO


class Telegraphic():
    # cache audio files into CPU
    @lru_cache(maxsize=None)
    def __init__(self):
        gm.mixer.init()
        self.rr = gm.mixer.Sound('sounds/rr.wav')

    def catch_telegraphic(self):
        print('Button was pressed...')
        self.rr.play()


if __name__ == '__main__':
    tl = Telegraphic()
    GPIO.setwarnings(False)
    GPIO.setmode(GPIO.BOARD)
    GPIO.setup(10, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)
    while 1:
        if GPIO.input(10) == GPIO.HIGH:
            tl.catch_telegraphic()
            time.sleep(1)
