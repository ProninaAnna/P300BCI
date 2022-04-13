import multiprocessing
import numpy as np
import time
from psychopy import core
from psychopy.monitors import Monitor
from psychopy.visual import Window, ImageStim, Rect
from psychopy.visual.circle import Circle
from psychopy.event import Mouse
from psychopy.core import wait
from CONSTANTS import *

class Visual:
    def __init__(self):
        pass

    def visual_process(self):
        
        monitor = Monitor('Phillips')
        monitor.setSizePix(SIZE)
        monitor.setWidth(WIDTH)
        monitor.setDistance(DISTANCE)
        monitor.saveMon()

        disp=Window(size=SIZE, monitor=monitor, units='deg', color=BACKCOL, screen =0, fullscr=True)

        mouse=Mouse()
        fixmark=Circle(disp, radius=0.05 ,edges=32, pos=CENTER, lineColor=FIXCOL)
        photosensor_stim = Rect(self.win, width=0.065, height=0.09, fillColor = 'white', lineWidth = 0, pos = PHOTOSENSOR_POS)
        
        fixmark.draw()
        disp.flip()
        time.sleep(2)
        
        photosensor_stim.draw()
        disp.flip()
        time.sleep(5)

        disp.close()


if __name__ == '__main__':
    pass