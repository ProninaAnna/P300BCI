import psychopy.visual 
import multiprocessing
import logging
import numpy as np
import time
from psychopy import core
from psychopy.monitors import Monitor
from psychopy.visual import Window
from psychopy.visual.circle import Circle
from psychopy.visual.rect import Rect
from psychopy.visual import TextStim
from psychopy.event import Mouse
from psychopy.core import wait
from CONSTANTS import *

class Visual:
    def __init__(self):
        self.monitor = Monitor(MONITOR, currentCalib={'sizePix':SIZE, 'width': WIDTH, 'distance':DISTANCE})
        self.display = Window(size=SIZE, monitor=self.monitor, units=SCREEN_UNITS, color=BACKCOL, screen=MONITOR_N, fullscr=True)
        self.mouse = Mouse()
        self.mode = VIS_MODE
        self.fixation_mark = Circle(self.display, radius=0.05 ,edges=32, pos=CENTER, lineColor=FIXCOL)
        self.photosensor_stim = Rect(self.display, size = (5.5,5.5), fillColor = FIXCOL, lineWidth = 0, pos = PHOTOSENSOR_POS)
        
    def visual_environment(self):
        '''
        '''
        if self.mode == 'rc':
            pass
        elif self.mode == 'spiral':
            # draw all main stimuli
            for position in STIM_POS:
                
                index = STIM_POS.index(position)
                group_size = len(STIM_POS)/len(STIM_SIZE)
                
                if index+1 < group_size:
                    # set first available size to first set of stimuli
                    stim_size = STIM_SIZE[0] 
                elif group_size <= index+1 < 2*group_size:
                    stim_size = STIM_SIZE[1]
                else: 
                    stim_size = STIM_SIZE[2]
                    
                stim = TextStim(self.display, text=STIM_NAMES[index], pos=position, units=SCREEN_UNITS, height=stim_size)
                stim.draw()
                
            # draw other stimuli
            self.fixation_mark.draw()
            self.photosensor_stim.draw()
            
            self.disp.flip()
            
        else:
            logging.error('Invalid viual mode specified')

    def visual_process(self):
        '''
        '''
        logging.info("Visual process started")

        while True:
            
            button = self.mouse.getPressed()
            
            if button[0]:
                break
            
            self.visual_environment()
            
        self.disp.close()


if __name__ == '__main__':
    a=Visual()
    a.visual_process()
   