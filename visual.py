import psychopy.visual 
import multiprocessing
import logging
import numpy as np
import time
import datetime
from psychopy import core
from psychopy.monitors import Monitor
from psychopy.visual import Window
from psychopy.visual.circle import Circle
from psychopy.visual.rect import Rect
from psychopy.visual import TextStim
from psychopy.visual import ImageStim
from psychopy.event import Mouse
from psychopy.core import wait
from pylsl import StreamInfo, StreamOutlet
from CONSTANTS import *

class Visual:
    def __init__(self):
        self.monitor = Monitor(MONITOR, currentCalib={'sizePix':SIZE, 'width': WIDTH, 'distance':DISTANCE})
        self.display = Window(size=SIZE, monitor=self.monitor, units=SCREEN_UNITS, color=BACKCOL, screen=MONITOR_N, fullscr=True)
        self.mouse = Mouse()
        self.mode = VIS_MODE
        self.fixation_mark = Circle(self.display, radius=0.05 ,edges=32, pos=CENTER, lineColor=FIXCOL)
        self.photosensor_stim = Rect(self.display, size = (5.5,5.5), fillColor = FIXCOL, lineWidth = 0, pos = PHOTOSENSOR_POS)
        self.LSL = self.create_lsl_outlet()
        
    def visual_environment(self, idx=(), state=""):
        '''Draw the visual environment'''

        if self.mode == 'rc':
            pass
        elif self.mode == 'spiral':
            # Blink condition
            # draw all main stimuli
            for position in STIM_POS:
                
                index = STIM_POS.index(position)
                group_size = len(STIM_POS)/len(STIM_SIZE)
                
                if index+1 <= group_size:
                    # set first available size to first set of stimuli
                    stim_size = STIM_SIZE[0] 
                elif group_size < index+1 <= 2*group_size:
                    stim_size = STIM_SIZE[1]
                else: 
                    stim_size = STIM_SIZE[2]

                stim = TextStim(self.display, text=STIM_NAMES[index], pos=position, units=SCREEN_UNITS, height=stim_size, opacity=0.5)
                # stim=ImageStim(self.display, image=r"F:\\Timofey\\P300BCI-main\\24-0.png", pos=position, units=SCREEN_UNITS, size=stim_size)

                if state == 'blink':
                    if index in idx:
                        stim = TextStim(self.display, text=STIM_NAMES[index], pos=position, units=SCREEN_UNITS, height=stim_size, opacity=1)
                        self.photosensor_stim.draw()
                        # stim=ImageStim(self.display, image=r"F:\\Timofey\\P300BCI-main\\24-1.png", pos=position, units=SCREEN_UNITS, size=stim_size)
                    
                stim.draw()
                
            # draw other stimuli
            self.fixation_mark.draw()
            
            # if state=='blink':
            #     self.LSL.push_sample([index], float(time.time()))

            self.display.flip()
            
        else:
            logging.error('Invalid viual mode specified')
            pass

    def visual_stimulation(self, idx):
        '''Run blinking stimulation'''

        self.visual_environment(idx, state='blink')
        self.LSL.push_sample([idx[0]], float(time.time()))
        wait(0.05)
        self.visual_environment(idx)
        wait(0.15)
    
    def take_screenshot(self):
        '''Draw the visual environment and take a screenshot'''

        self.visual_environment()
        self.display.getMovieFrame(buffer='front')
        self.display.saveMovieFrames(r'F:\\Timofey\\P300BCI-main\\environment.jpg')
        self.display.close()

    def create_lsl_outlet(self):
        '''Create stream outlet for sending markers'''
        
        info = StreamInfo(VISUAL_STREAM_NAME, 'Markers', 1, 0, 'int32', '10106CA9-8564-4400-AB07-FFD2B668B86E')
        outlet = StreamOutlet(info)
        return outlet

    def visual_process(self):
        '''Run a desirable visual process'''

        logging.info("Visual process started")

        # while True:
        # for i in range(9):
        #     button = self.mouse.getPressed()
            
        #     if button[0]:
        #         break

        # time1 = datetime.datetime.now()    
        wait(1)

        self.LSL.push_sample([STARTMARKER], float(time.time()))

        # wait(10)

        for i in GROUP1+GROUP2:
            self.visual_stimulation(i)
        self.LSL.push_sample([ENDMARKER], float(time.time()))
        
        self.display.close()
        
        # time2 = datetime.datetime.now()
        # print  time2 - time1


if __name__ == '__main__':
    a=Visual()
    a.visual_process()

   