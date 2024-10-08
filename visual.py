import multiprocessing
import logging
import time
import numpy as np
import random
# import psychopy.visual
from psychopy.monitors import Monitor
from psychopy.visual import Window
from psychopy.visual.circle import Circle
from psychopy.visual.rect import Rect
from psychopy.visual import TextStim
# from psychopy.visual import ImageStim # probably not needed anymore
from psychopy.event import Mouse, waitKeys, getKeys, clearEvents
from psychopy.core import wait
from pylsl import StreamInfo, StreamOutlet
from CONSTANTS import *



def merge_two_dicts(x, y):
    '''Merge two dictionaries in one.'''
    
    z = x.copy()   # start with keys and values of x
    z.update(y)    # modifies z with keys and values of y
    return z

class Visual:
    '''
    Visual stimulation class. Contains methods and attributes needed for
    stimulation purposes, between-process communication and lsl streaming.

    Attributes:
        mode -- which visual environment should be used, can be 'spiral'
                or 'sqare'
        screen_units -- which screen units need to be used to create a
                        visual environment, can be 'pix' or 'deg'
        monitor -- instance of psychopy Monitor object
                   setting up monitor for stimulation 
        display -- instance of psychopy Window object
                   setting up psychopy stimulation window 
        mouse -- instance of psychopy Mouse object
        fixation_mark -- instance of psychopy Monitor object
        photosensor_stim -- instance of psychopy Circle object
        lsl -- instance of lsl Stream outlet object
        lock, queue, pipe_in, pipe_out -- instances of multiprocessing objects
        groups -- groups of stimuli to flash simultaniously

    Methods:
        visual_environment:
        visual_stimulation:
        take_screenshot:
        visual_process:
    '''
    def __init__(self, queue, pipe_in, pipe_out, lock, mode='spiral'):
        '''Initialize Visual class.
        
        Keyword arguments:
        queue -- Queue object to put data in and get it (used to
                 send and detect the end mark to stop all processes)
        pipe_in -- Pipe object to send messages (used to send a mark
                   and unlock Visual process)
        pipe_out -- Pipe object to recieve messages (used to receive a 
                    mark and unlock Visual process)
        lock -- Lock object to lock the process until another process
                unlocks it
        mode -- which visual environment should be used, can be 'spiral'
                or 'sqare' 
        
        '''
        self.mode = mode
        self.screen_units = SCREEN_UNITS[self.mode]
        self.stim_pos = STIM_POS[self.mode]
        self.monitor = Monitor(MONITOR, currentCalib={'sizePix': SIZE,
                                                      'width': WIDTH,
                                                      'distance': DISTANCE})
        self.display = Window(size=SIZE, monitor=self.monitor, units=self.screen_units,
                              color=BACKCOL, screen=MONITOR_N, fullscr=True)
        self.mouse = Mouse()
        self.fixation_mark = Circle(self.display, radius=0.05 ,edges=32,
                                    pos=CENTER, lineColor=FIXCOL)
        self.photosensor_stim = Rect(self.display, size = (5.5,5.5), fillColor = FIXCOL,
                                     lineWidth = 0, pos = PHOTOSENSOR_POS[self.mode]) # TODO: size for square mode
        self.pause_mark = TextStim(self.display, text='PAUSE', pos=PAUSE_POS,
                                   units=self.screen_units, height=STIM_SIZE[1]) # TODO: height and pos for square mode
        self.LSL = self.create_lsl_outlet()
        self.lock = lock
        self.queue = queue
        self.pipe_in = pipe_in
        self.pipe_out = pipe_out
        self.get_groups() # create groups attribute

        wait(5) # Preventing the psychopy window from opening too early

    def get_groups(self):
        '''Create dictionary with groups of stimuli.'''
        
        if self.mode == 'spiral':
            self.groups = merge_two_dicts(GROUP1, GROUP2)
        else:
            self.groups = merge_two_dicts(ROWS, COLS)
    
    def create_lsl_outlet(self):
        '''Create stream outlet for sending markers.
        
        Returns:
        outlet -- StreamOutlet object to stream markers
        
        '''
        # Create info with necessary information about the stream
        info = StreamInfo(VISUAL_STREAM, 'Markers', 1, 0, 'int32',
                          '10106CA9-8564-4400-AB07-FFD2B668B86E') 
        # Create outlet
        outlet = StreamOutlet(info)
        return outlet
    
    def visual_environment(self, flash_group=(), state=""):
        '''Draw the visual environment (GUI).
        
        Keyword arguments:
        flash group -- tuple with coordinates of stimuli
        state -- string with the mode of visual environment
                 can be 'flash', 'que', 'pause'...

        '''
        # Loop over all stimuli positions
        for position in self.stim_pos:

            # Extracting indeces and proper size for each stimulus 
            index, stim_size = self.get_stim_size(position)

            # Draw stimulus
            stim = TextStim(self.display, text=STIM_NAMES[index], pos=position,
                            units=self.screen_units, height=stim_size, opacity=0.5)
            
            # Make target stimuli flash
            if state == 'flash':
                if index in flash_group:
                    stim = TextStim(self.display, text=STIM_NAMES[index], pos=position,
                                    units=self.screen_units, height=stim_size, opacity=1)
                    self.photosensor_stim.draw()

            # Mark target stimulus
            if state == 'que':
                if index == flash_group:
                    stim = TextStim(self.display, text=STIM_NAMES[index], pos=position,
                                    units=self.screen_units, height=stim_size, opacity=1, color=QUECOL)
            
            stim.draw()
            
        # Drawing other stimuli
        if self.mode == 'spiral':
            self.fixation_mark.draw()
        # Pause screen
        if state == 'pause':
            self.pause_mark.draw()
            
        self.display.flip()
        
    def get_stim_size(self, position):
        '''Give proper size to stimulus.
        
        Keyword arguments:
        position -- position of a stimulus on the screen
        
        Returns:
        stim_size -- size of a stimulus
        index -- index of a stimulus in STIM_NAMES (see CONSTANTS) 
        
        '''
        index = self.stim_pos.index(position)
        if self.mode == 'spiral':
            group_size = len(self.stim_pos)/len(STIM_SIZE)

            if index+1 <= group_size:
                stim_size = STIM_SIZE[0] 
            elif group_size < index+1 <= 2*group_size:
                stim_size = STIM_SIZE[1]
            else: 
                stim_size = STIM_SIZE[2]
        else:
            stim_size = 75
        return(index, stim_size)
    
    def visual_stimulation(self, flash_group, group_number):
        '''Run stimulation.
        
        Keyword arguments:
        flash_group -- tuple with coordinates of stimuli
        group_number -- key of a group in groups dicts (see CONSTANTS)

        '''
        self.visual_environment(flash_group = flash_group, state='flash')
        self.LSL.push_sample([group_number], float(time.time()))
        wait(FLASH)
        self.visual_environment(flash_group)
        wait(ISI)
    
    def show_target(self, letter):
        '''Show target stimulus with multiple flashes.
        
        Keyword arguments:
        letter -- target letter to show to user

        '''
        wait(1)
        self.visual_environment(STIM_NAMES.index(letter.upper()), state='que')
        wait(2)

    def take_screenshot(self, filepath):
        '''Draw the visual environment and take a screenshot.'''

        self.visual_environment()
        self.display.getMovieFrame(buffer='front')
        self.display.saveMovieFrames(filepath)
        self.display.close()

    def create_sequence(self, seed=None):
        '''Create sequence of words to be used in the experiment.
        
        Returns:
        sequence -- list of words
        
        '''
        filename = os.path.join(os.path.dirname(os.path.realpath(__file__)), '5_letter_words.txt')
        with open(filename, 'r') as f:
            lines=f.readlines()
        words=[]
        for line in lines:
            words.extend(line.split())
        list_of_words=[]
        for word in words:
            list_of_words.append(word)

        if seed:
            random.seed(seed)            
        sequence=random.sample(list_of_words, 4)

        target_file = os.path.join(FILEPATH, FILECODE, FILECODE+'_aims.txt')

        with open(target_file, 'w') as f:
             f.write(str(sequence))

        return sequence
        
    def pause(self):
        '''Pause the stimulation.'''
        
        # Track pause start in logging and send marker
        logging.info('Pause. Press space to continue.')
        self.LSL.push_sample([PAUSE_START], float(time.time()))
        # Draw pause screen
        self.visual_environment(state='pause')
        # Wait until user release pause
        waitKeys(maxWait=60, keyList=['space'])
        clearEvents()
        # Track pause end in logging and send marker
        logging.info('Continue stimulation...')
        self.LSL.push_sample([PAUSE_END], float(time.time()))
    
    def visual_process(self, sequence=[], lockable = True):
        '''
        Run visual process.
        
        Keyword arguments:
        sequence -- list of lists or similar containers with indeces of target stimuli
        lockable -- bool, True if need to wait for another process to unlock it

        '''
        
        order=[i for i in range(len(self.groups))] # define order of flashes
        
        if not sequence:
            sequence=self.create_sequence()
        try:
            
            # Lock Visual process if necessary 
            if lockable:
                self.lock.acquire()
                logging.info("Visual process locked")

                while self.lock:
                    if self.pipe_out.recv() == int('1'):
                        self.lock.release()
                        break
                
            logging.info("Visual process started")
            self.visual_environment()
            
            waitKeys() # pressing any key starts the stimulation

            # Loop over all target words 
            for word in sequence:
                self.LSL.push_sample([WORD_START], float(time.time()))
                # Loop over all target letters
                for letter in word:
                    logging.info('Letter {} in word {}'.format(letter, word))
                    # Show target stimulus
                    self.show_target(letter)
                    # Loop over random flashes
                    self.LSL.push_sample([TRIAL_START], float(time.time()))
                    for i in range(TRIAL_LEN):
                        random.shuffle(order) # randomize flash order
                        for j in order:
                            self.visual_stimulation(self.groups[j], j)
                        # Check if need to pause stimulation
                        if 'p' in getKeys(['p']):
                            self.pause()
                            self.show_target(letter) # Remind target letter
                    self.LSL.push_sample([TRIAL_END], float(time.time()))
                self.LSL.push_sample([WORD_END], float(time.time()))
                waitKeys() # Wait key press before going to next word
            self.display.close()
            
            self.queue.put(int(1))
                
        finally:
            self.display.close()



if __name__ == '__main__':

    logging.basicConfig(format='%(levelname)s	%(processName)s	%(message)s',
                        level=logging.INFO)
    logging.getLogger()
    queue = multiprocessing.Queue()
    pipe_in, pipe_out = multiprocessing.Pipe()
    lock = multiprocessing.Lock()
    a=Visual(queue, pipe_in, pipe_out, lock)
    a.visual_process(sequence=['B'], lockable = False)
    