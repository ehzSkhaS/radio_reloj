import time
import asyncio
import pygame as gm
from datetime import datetime
from functools import lru_cache


class Generator():
    def __init__(self):
        gm.mixer.pre_init(frequency=44100, size=-16, channels=1, buffer=1024)
        gm.mixer.init()
        # List of: audio
        self.naudio = [gm.mixer.Sound('sounds/tick.wav'),
                       gm.mixer.Sound('sounds/min_1_4.wav'),
                       gm.mixer.Sound('sounds/min_0_5.wav')]

    def emit(self):
        while 1:
            t = datetime.now()
            # avoid time tick lag after sync with NTP
            if t.microsecond < 10000:
                if t.second != 0:
                    self.naudio[0].play()
                else:
                    if t.minute % 5 != 0:
                        self.naudio[1].play()
                    elif t.minute % 5 == 0:
                        self.naudio[2].play()
                # print(t.hour, ':', t.minute, ':', t.second, ':', t.microsecond)
            # sleep only the amount of micros left after now timestamp
            time.sleep((1000000 - datetime.now().microsecond) * 0.000001)

    @lru_cache(maxsize=16)
    async def async_emit(self):
        while 1:
            t = datetime.now()
            # avoid time tick lag after sync with NTP
            if t.microsecond < 10000:
                if t.second != 0:
                    self.naudio[0].play()
                else:
                    if t.minute % 5 != 0:
                        self.naudio[1].play()
                    elif t.minute % 5 == 0:
                        self.naudio[2].play()
                # print(t.hour, ':', t.minute, ':', t.second, ':', t.microsecond)
            # sleep only the amount of micros left after now timestamp
            await asyncio.sleep((1000000 - datetime.now().microsecond) * 0.000001)


if __name__ == "__main__":
    gen = Generator()
    # gen.emit()
    asyncio.run(gen.async_emit())
