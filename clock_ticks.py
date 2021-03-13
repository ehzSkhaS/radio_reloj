import time
import pygame as gm
from datetime import datetime
from functools import lru_cache


class Generator():
    @lru_cache(maxsize=None)
    def __init__(self, host, sync_time):
        self.host = host
        self.sync_time = sync_time
        gm.mixer.init()
        # List of: audio
        self.naudio = [gm.mixer.Sound('sounds/tick.wav'),
                       gm.mixer.Sound('sounds/min_1_4.wav'),
                       gm.mixer.Sound('sounds/min_0_5.wav'),
                       gm.mixer.Sound('sounds/rr.wav')]
        # self.sys_timer_sync(host, sync_time)

    def sys_timer_sync(self, host, sync_time):
        import sys
        import time_sync_ntp as tsn
        from multiprocessing import Process
        p = 0
        if sys.platform == "win32":
            p = Process(target=tsn.set_windows_time,
                        args=(host, sync_time))
        if sys.platform.startswith('linux'):
            p = Process(target=tsn.set_linux_time,
                        args=(host, sync_time))
        p.start()

    def notes_build(self, t_note):
        import numpy as np
        # Distibute the tick by fs
        t = np.linspace(0,
                        self.ntype[t_note][2],
                        int(self.ntype[t_note][2] * self.ntype[t_note][1]),
                        False)
        # Generate a 1000 Hz sine wave
        note = np.sin(self.ntype[t_note][0] * t * 2 * np.pi)
        # Ensure that highest value is in 16-bit range
        audio = note * (2**15 - 1) / np.max(np.abs(note))
        # Convert to 16-bit data
        audio = audio.astype(np.int16)
        return audio

    def emit(self):
        t = datetime.now()
        if t.microsecond < 25000:
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
    gen = Generator("pool.ntp.org", 5)
    while 1:
        gen.emit()
