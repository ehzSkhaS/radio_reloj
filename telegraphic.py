import time
import pygame as gm
import importlib.util

try:
    importlib.util.find_spec('RPi.GPIO')
    import RPi.GPIO as GPIO
except ImportError:
    import FakeRPi.GPIO as GPIO

gm.mixer.init()
rr = gm.mixer.Sound('sounds/rr.wav')


def catch_telegraphic(channel):
    rr.play()
    print('Button was pressed...')


if __name__ == '__main__':
    GPIO.setwarnings(False)
    GPIO.setmode(GPIO.BOARD)
    GPIO.setup(10, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)
    GPIO.add_event_detect(10, GPIO.RISING, callback=catch_telegraphic, bouncetime=1000)
    while 1:
        time.sleep(10)
