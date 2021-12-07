import os
import sys
import time
import warnings
#import logging
import random
import pylsl
import pandas as pd
import numpy as np
import win32com.client as wincl
from psychopy import core
from psychopy.monitors import Monitor
from psychopy.visual import Window, Circle, ImageStim
from psychopy.event import Mouse
from psychopy.core import wait


from CONSTANTS import *

# ===============
# === VISUALS ===
# ===============

class Visuals:
    def __init__(self, namespace):
        self.namespace = namespace
        self.trials = TRIALNUMBER
        self.flashes = TRIALREPEATS
        self.marker_stream = Stream(MESSAGE_STREAM)
        self.marker_stream_info = self.marker_stream.create()
        self.path = FILEPATH
        
        core.wait(0.1)
    
    def get_column(self, l):
        bar=[]
        foo=[l[i] for i in [0, 3, 6]]
        bar.append(foo)
        foo=[l[i] for i in [1, 4, 7]]
        bar.append(foo)
        foo=[l[i] for i in [2, 5, 8]]
        bar.append(foo)
        return bar
    
    def get_row(self, l):
        bar=[l[i:i + 3] for i in range(0, len(l), 3)]
        return bar
    
    def create_groups(self, block1, block2, block3):
        random.shuffle(block1)
        random.shuffle(block2)
        random.shuffle(block3)
        r=self.get_row(block1)+self.get_row(block2)+self.get_row(block3)
        c=self.get_column(block1)+self.get_column(block2)+self.get_column(block3)
        return r+c
    
    def create_stim_sequence(self, block1, block2, block3, repeats):
        seq=[]
        for i in range(repeats):
            g=self. create_groups(BLOCK1, BLOCK2, BLOCK3)
            seq+=g
        return seq
    
    def draw_group(self, stimuli):
        for stimulus in stimuli:
            stimulus.draw()
    
    def create_target(self):
        target=[]
        for letter in CIRCLES.keys():
            target.append(letter)
        random.shuffle(target)
        #print(target)
        return target
            
    
    def procede(self):
        
        monitor = Monitor(name = 'HP') 
        monitor.setWidth(WIDTH) 
        monitor.setDistance(DISTANCE)
        monitor.setSizePix(SIZE)

        groups=self.create_stim_sequence(BLOCK1, BLOCK2, BLOCK3, TRIALREPEATS)
        targets= self.create_target()
        #print(groups)
        with open(self.path +'targets.txt', 'w') as file:
            file.write(str(targets))
        with open(self.path +'groups.txt', 'w') as file:
            file.write(str(groups))

        disp=Window(size=SIZE, monitor=monitor, units='deg', color=BACKCOL, screen =1, fullscr=True)
    
        mouse=Mouse()
    
        fixmark=Circle(disp, radius=0.05 ,edges=32, pos=CENTER, lineColor=FIXCOL)
    
        images = []
        for item in CIRCLES.keys():
            image=ImageStim(disp, image=CIRCLES[item][1], pos=CIRCLES[item][0], size=CIRCLES[item][3])
            images.append(image)
            
        marker_outlet = self.marker_stream.create_outlet(self.marker_stream_info)
        
        fixmark.draw()
        self.draw_group(images)
        disp.flip()

        self.send_marker(marker_outlet, [EXP_START], time.time())
        
        while self.trials !=0: # cycle for trials
            
            button=mouse.getPressed() # break if mouse pressed
            if button[0]:
                break
                
            self.send_marker(marker_outlet, [TRIAL_START], time.time())
                
            while self.flashes != 0: # cycle for flaches in each trial
                
                button=mouse.getPressed() # break if mouse pressed
                if button[0]:
                    break

                # presenting all stimuli and flash
                for item in groups: # create a new group (row/column)
                    
                    self.send_marker(marker_outlet,[groups.index(item)], time.time())
                    print(item)
                    
                    flashes=[]
                    for i in item:
                        flash=ImageStim(disp, image=CIRCLES[i][2], pos=CIRCLES[i][0], size=CIRCLES[i][3])
                        flashes.append(flash)
                    fixmark.draw()
                    self.draw_group(images)
                    self.draw_group(flashes)
                    disp.flip()
                    wait(STIM)
                    fixmark.draw()
                    self.draw_group(images)
                    wait(ISI)
                    disp.flip()
                self.flashes -= 1
            self.trials -= 1
            
        self.send_marker(marker_outlet, [EXP_END], time.time())
        print('Presentation End')

        disp.close()
    
    def send_marker(self, outlet, marker, time):
        self.marker_stream.outlet_push(outlet, marker, time)


## ===================
## === EYETRACKING ===
## ===================

#class Eyetracker:
#    def __init__(self):
#        pass


# =================
# === RECORDING ===
# =================

class Record:
    def __init__(self, namespace):
        self.namespace = namespace
        self.eeg_stream = Stream(EEG_STREAM)
        self.eeg_stream_info = self.eeg_stream.resolve()
        self.photo_stream = Stream(PHOTOSENSOR_STREAM)
        self.photo_stream_info = self.photo_stream.resolve()
        self.marker_stream = Stream(MESSAGE_STREAM)
        self.marker_stream_info = self.marker_stream.resolve()
        self.path = FILEPATH
        
    def start_record(self):
        
        eeg_array = []
        photo_array = []
        marker_array = []
        
        
        eeg_inlet = self.eeg_stream.create_inlet(self.eeg_stream_info)
        photo_inlet = self.photo_stream.create_inlet(self.photo_stream_info)
        marker_inlet = self.marker_stream.create_inlet(self.marker_stream_info) 
    
        while 1:
            try:
                eeg_chunk, eeg_timestamp = self.eeg_stream.inlet_pull(eeg_inlet)
                photo_chunk, photo_timestamp = self.photo_stream.inlet_pull(photo_inlet)
                marker_chunk, marker_timestamp = self.marker_stream.inlet_pull(marker_inlet)
                eeg_array.append([eeg_chunk, eeg_timestamp])
                photo_array.append([photo_chunk, photo_timestamp])
                marker_array.append([marker_chunk, marker_timestamp])
            finally:
                pass
            if marker_chunk == [EXP_END]:
                with open(self.path + 'eeg_data.txt', 'w') as file:
                    file.write(eeg_array)
                with open(self.path + 'photo_data.txt', 'w') as file:
                    file.write(photo_array)
                with open(self.path +'marker_data.txt', 'w') as file:
                    file.write(marker_array)
                print('Recording End')
                break

                
    

# =================
# === STREAMING ===
# =================

class Stream:
    def __init__(self, name):
        self.name = name
    def resolve(self):
        print('Connecting to data stream...')
        stream = pylsl.resolve_byprop('name', self.name) # resolve an EEG stream on the lab network
        return stream[0]
    def create(self):
        print('Creating data stream...')
        stream = pylsl.stream_info(self.name)
        return stream
    def create_inlet(self, stream):
        inlet = pylsl.StreamInlet(stream)
        try:
            inlet
        except:
            print('Something went wrong')
        return inlet
    def create_outlet(self, stream):
        outlet = pylsl.StreamOutlet(stream)
        return outlet
    def inlet_pull(self, inlet):
        try:
            chunk, timestamp = inlet.pull_chunk()
        except:
            print('Stream inlet error')

        return chunk, timestamp
    def outlet_push(self, outlet, item, timestamp):
        outlet.push_chunk(item, timestamp)
    

import multiprocessing
from source import *

#def eyetracking_process(namespace):
#    pass


def streaming_process(namespace):
    eeg = Record(namespace)
    eeg.start_record()

if __name__ == '__main__':
    try:
        manager = multiprocessing.Manager()
        Global = manager.Namespace()
        
        #run_eyetracking = multiprocessing.Process(name = 'Eyetracking', target = eyetracking_process, args=(Global,))
        #run_visuals = multiprocessing.Process(name = 'Visuals', target = visuals_process,args=(Global,))
        run_streaming = multiprocessing.Process(name = 'Streaming', target = streaming_process,args=(Global,))
        
        #run_eyetracking.start()
        #run_visuals.start()
        run_streaming.start()
    finally:
        run_streaming.join()
        #run_visuals.join()
        #run_eyetracking.join()