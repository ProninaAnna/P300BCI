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
        pass

    def visual_process(self):
        logging.info("Visual process started")

        monitor = Monitor('Dell') # Monitor('Phillips')
        monitor.setSizePix(SIZE)
        monitor.setWidth(WIDTH)
        monitor.setDistance(DISTANCE)
        monitor.saveMon()

        disp=Window(size=SIZE, monitor=monitor, units='deg', color=BACKCOL, screen=2, fullscr=True)

        mouse=Mouse()
        fixmark=Circle(disp, radius=0.05 ,edges=32, pos=CENTER, lineColor=FIXCOL)
        photosensor_stim = Rect(disp, size = (5.5,5.5), fillColor = 'white', lineWidth = 0, pos = PHOTOSENSOR_POS)

        while True:
            button = mouse.getPressed()
            if button[0]:
                break

            for letter in [zip(BLOCK1, C1, LS1), zip(BLOCK2, C2, LS2), zip(BLOCK3, C3, LS3)]:
                for stimul in letter:
                    stim = TextStim(disp, text=stimul[0], pos=stimul[1], units='deg', height=stimul[2], opacity=0.4)
                    stim.draw()
                

            fixmark.draw()
            disp.flip()
        # time.sleep()
        
        # for i in range(0,10):
        #     photosensor_stim.draw()
        #     disp.flip()
        #     print int(time.time()), 'FLASH!' 
        #     time.sleep(0.05)
        #     disp.flip()
        #     time.sleep(0.1)
        
        
        time.sleep(2)
        disp.close()


if __name__ == '__main__':
    #print np.rad2deg(np.arctan(23.75/50))
    a=Visual()
    a.visual_process()
    pass
   