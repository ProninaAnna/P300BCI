import psychopy.visual 
import multiprocessing
from turtle import color, fillcolor
import numpy as np
import time
from psychopy import core
from psychopy.monitors import Monitor
from psychopy.visual import Window
from psychopy.visual.circle import Circle
from psychopy.visual.rect import Rect
from psychopy.event import Mouse
from psychopy.core import wait
from CONSTANTS import *

class Visual:
    def __init__(self):
        pass

    def visual_process(self):
        
        monitor = Monitor('Dell') # Monitor('Phillips')
        monitor.setSizePix(SIZE)
        monitor.setWidth(WIDTH)
        monitor.setDistance(DISTANCE)
        monitor.saveMon()

        disp=Window(size=SIZE, monitor=monitor, units='deg', color=BACKCOL, screen =1, fullscr=True)

        mouse=Mouse()
        fixmark=Circle(disp, radius=0.05 ,edges=32, pos=CENTER, lineColor=FIXCOL)
        photosensor_stim = Rect(disp, size = (5.5,5.5), fillColor = 'white', lineWidth = 0, pos = PHOTOSENSOR_POS)

        fixmark.draw()
        disp.flip()
        time.sleep(1)
        
        for i in range(0,10):
            photosensor_stim.draw()
            disp.flip()
            print int(time.time()), 'FLASH!' 
            time.sleep(0.05)
            disp.flip()
            time.sleep(0.1)
        
        
        time.sleep(2)
        disp.close()


if __name__ == '__main__':
    #print np.rad2deg(np.arctan(23.75/50))
    a=Visual()
    a.visual_process()
    pass