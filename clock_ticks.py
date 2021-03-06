#!/usr/bin/python3.6

import sys
import time
import numpy as np
import simpleaudio as sa
from subprocess import *
from datetime import datetime
from multiprocessing import Process

class Generator():
    sec_changed = 'dead'        

    def __init__(self, host, sync_time):
        self.host = host              
        self.sync_time = sync_time     
        # Dictionary of:       [freq, fs,    secs]
        self.ntype =    {"1" : [1000, 44100, 0.01],  # secs
                         "2" : [1000, 44100, 0.125], # mins 1, 2, 3, 4  
                         "3" : [1000, 44100, 0.25],  # mins 0, 5
                         "4" : [1000, 44100, 0.05],  # .
                         "5" : [1000, 44100, 0.15]}  # _
        # Dictionary of:       audio                      
        self.naudio =   {"1" : self.notes_build("1"),
                         "2" : self.notes_build("2"),
                         "3" : self.notes_build("3"),
                         "4" : self.notes_build("4"),
                         "5" : self.notes_build("5")}      
        #self.sys_timer_sync(host, sync_time)

    def sys_timer_sync(self, host, sync_time):
        import time_sync_ntp as tsn  
        p = 0
        if sys.platform == "win32":      
            p = Process(target = tsn.set_windows_time, 
                        args = (host, sync_time))
        if sys.platform.startswith('linux') :      
            p = Process(target = tsn.set_linux_time, 
                        args = (host, sync_time))
        p.start()            

    def notes_build(self, t_note):        
        # Distibute the tick by fs
        t = np.linspace(0, 
                        self.ntype[t_note][2], 
                        int(self.ntype[t_note][2] * self.ntype[t_note][1]), 
                        False)
        # Generate a 440 Hz sine wave
        note = np.sin(self.ntype[t_note][0] * t * 2 * np.pi)
        # Ensure that highest value is in 16-bit range
        audio = note * (2**15 - 1) / np.max(np.abs(note))
        # Convert to 16-bit data
        audio = audio.astype(np.int16)
        return audio

    def start_palyback(self, t_note):
        # Start playback        
        play_obj = sa.play_buffer(self.naudio[t_note], 
                                  1, 
                                  2, 
                                  self.ntype[t_note][1])
        # Wait for playback to finish before exiting
        play_obj.wait_done()

    def get_sys_time_data(self):
        left_micro = (1000000 - datetime.now().microsecond) / 1000000 
        time.sleep(left_micro)
        t = datetime.now()
        print(t.hour,":",t.minute,":",t.second,":",t.microsecond)
        t = datetime.now()        
        if (t.minute % 5) == 0 and t.second == 0:
            self.start_palyback("3")
        elif (t.minute % 5) != 0 and t.second == 0:
            self.start_palyback("2")
        else:
            self.start_palyback("1")

if __name__ == "__main__":    
    gen = Generator("pool.ntp.org", 17)                    
    while 1:                
        gen.get_sys_time_data()   
    
