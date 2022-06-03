import multiprocessing
import logging
import time
import numpy as np
#import psychopy.visual # ?
from psychopy.monitors import Monitor
from psychopy.visual import Window
from psychopy.visual.circle import Circle
from psychopy.visual.rect import Rect
from psychopy.visual import TextStim
#from psychopy.visual import ImageStim # probably not needed anymore
from psychopy.event import Mouse, waitKeys
from psychopy.core import wait
from pylsl import StreamInfo, StreamOutlet
from CONSTANTS import *

def create_lsl_outlet():
    '''
    Create stream outlet for sending marker
    '''
    
    info = StreamInfo(VISUAL_STREAM, 'Markers', 1, 0, 'int32', '10106CA9-8564-4400-AB07-FFD2B668B86E') # contains necessary information about the stream
    outlet = StreamOutlet(info) # StreamOutlet object to stream data samples/chunks
    return outlet

def merge_two_dicts(x, y):
    z = x.copy()   # start with keys and values of x
    z.update(y)    # modifies z with keys and values of y
    return z

class Visual:
    '''
    Visual stimulation class. Contains methods and attributes needed for
    stimulation purposes, between-process communication and lsl streaming.

    Attributes:
        monitor -- instance of psychopy Monitor object
            setting up monitor for stimulation 
        display -- instance of psychopy Window object
            setting up psychopy stimulation window 
        mouse -- instance of psychopy Mouse object
        fixation_mark -- instance of psychopy Monitor object
        photosensor_stim -- instance of psychopy Circle object
        lsl -- instance of lsl Stream outlet object
        lock, queue, pipe_in, pipe_out -- instances of multiprocessing objects

    Methods:
        visual_environment:
        visual_stimulation:
        take_screenshot:
        visual_process:
    '''
    def __init__(self, queue, pipe_in, pipe_out, lock):
        self.monitor = Monitor(MONITOR, currentCalib={'sizePix':SIZE, 'width': WIDTH, 'distance':DISTANCE})
        self.display = Window(size=SIZE, monitor=self.monitor, units=SCREEN_UNITS, color=BACKCOL, screen=MONITOR_N, fullscr=True)
        self.mouse = Mouse()
        self.fixation_mark = Circle(self.display, radius=0.05 ,edges=32, pos=CENTER, lineColor=FIXCOL)
        self.photosensor_stim = Rect(self.display, size = (5.5,5.5), fillColor = FIXCOL, lineWidth = 0, pos = PHOTOSENSOR_POS)
        self.LSL = create_lsl_outlet()
        self.lock = lock
        self.queue = queue
        self.pipe_in = pipe_in
        self.pipe_out = pipe_out

        wait(5) # preventing the psychopy window from opening too early      


    def visual_environment(self, flash_group=(), state=""):
        '''Draw the visual environment'''

        # Loop over all stimuli positions
        for position in STIM_POS:

            # extracting indeces to give each stimulus a proper size 
            index = STIM_POS.index(position)
            group_size = len(STIM_POS)/len(STIM_SIZE)

            if index+1 <= group_size:
                stim_size = STIM_SIZE[0] 
            elif group_size < index+1 <= 2*group_size:
                stim_size = STIM_SIZE[1]
            else: 
                stim_size = STIM_SIZE[2]

            # Draw stimulus
            stim = TextStim(self.display, text=STIM_NAMES[index], pos=position, units=SCREEN_UNITS, height=stim_size, opacity=0.5)
            
            # Make target stimuli flash
            if state == 'flash':
                if index in flash_group:
                    stim = TextStim(self.display, text=STIM_NAMES[index], pos=position, units=SCREEN_UNITS, height=stim_size, opacity=1)
                    self.photosensor_stim.draw()

            if state == 'que':
                if index == flash_group:
                    stim = TextStim(self.display, text=STIM_NAMES[index], pos=position, units=SCREEN_UNITS, height=stim_size, opacity=1, color=QUECOL)

            stim.draw()
            
        # drawing other stimuli
        self.fixation_mark.draw()

        self.display.flip()
        

    def visual_stimulation(self, flash_group, group_number):
        '''Run stimulation'''

        self.visual_environment(flash_group = flash_group, state='flash')
        self.LSL.push_sample([group_number], float(time.time()))
        wait(FLASH)
        self.visual_environment(flash_group)
        wait(ISI)
    
    def show_target(self, letter):
        '''Show target stimulus with multiple flashes
        
        Keyword arguments:
        letter -- target letter to show to user

        '''
        wait(1)
        self.visual_environment(STIM_NAMES.index(letter), state='que')
        wait(2)

    def take_screenshot(self, filepath):
        '''Draw the visual environment and take a screenshot'''

        self.visual_environment()
        self.display.getMovieFrame(buffer='front')
        self.display.saveMovieFrames(filepath)
        self.display.close()


    def visual_process(self, sequence='', lockable = True):
        '''
        Run visual process.
        Arguments:
        
        sequence -- list of lists or similar containers with indeces of target stimuli
        '''
        np.random.seed=42
        groups=merge_two_dicts(GROUP1, GROUP2) # make stimulus groups dict
        order=np.random.shuffle([i for i in range(len(groups))]) # generate random order of flashse
        try:
            
            # Lock Visual process if necessary 
            if lockable:
                self.lock.acquire()
                logging.info("Visual process locked ")

                while self.lock:
                    if self.pipe_out.recv() == int('1'):
                        self.lock.release()
                        break
                
            logging.info("Visual process started")

            waitKeys() # pressing any key starts the stimulation

            # loop over all target words 
            for word in ['BCI']:
                # loop over all target letters
                for letter in word:
                    # Show target stimulus
                    self.show_target(letter)
                    # loop over random flashes
                    self.LSL.push_sample([TRIAL_START], float(time.time()))
                    for i in range(TRIAL_LEN):
                        for j in order:
                            self.visual_stimulation(groups[j], j)
                    self.LSL.push_sample([TRIAL_END], float(time.time()))

            self.display.close()
            
            self.queue.put(int(1))
                
        finally:
            self.display.close()



if __name__ == '__main__':

    queue = multiprocessing.Queue()
    pipe_in, pipe_out = multiprocessing.Pipe()
    lock = multiprocessing.Lock()
    a=Visual(queue, pipe_in, pipe_out, lock)
    a.visual_process(lockable = False)
