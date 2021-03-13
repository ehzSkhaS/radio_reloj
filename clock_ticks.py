import time
import pygame as gm
from datetime import datetime
from functools import lru_cache


class Generator():
    @lru_cache(maxsize=None)
    def __init__(self):        
        gm.mixer.init()
        # List of: audio
        self.naudio = [gm.mixer.Sound('sounds/tick.wav'),
                       gm.mixer.Sound('sounds/min_1_4.wav'),
                       gm.mixer.Sound('sounds/min_0_5.wav')]

    def emit(self):
        t = datetime.now()
        if t.microsecond < 50000:
            if t.second == 0:
                if t.minute % 5 == 0:
                    self.naudio[2].play()
                elif t.minute % 5 != 0:
                    self.naudio[1].play()
            else:
                self.naudio[0].play()
            print(t.hour, ":", t.minute, ":", t.second, ":", t.microsecond)
        time.sleep((1000000 - datetime.now().microsecond) * 0.000001)


if __name__ == "__main__":
    gen = Generator()
    while 1:
        gen.emit()
