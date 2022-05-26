"""
Run the experiment.

Subsequently launches distinct processes for eyetracking, visual stimuli
demonstration, EEG and photocell recording.

"""

import multiprocessing
import logging
from eeg import *
from eyetracker import *
from visual import *
from CONSTANTS import*
import time

logging.basicConfig(format='%(levelname)s	%(processName)s	%(message)s', level=logging.INFO)
logging.getLogger()

# Create structures for processes

def visual(queue, pipe_in, pipe_out, lock):
    Visual_obj = Visual(queue, pipe_in, pipe_out, lock)
    Visual_obj.visual_process()

def marker(queue):
    EEG_obj = EEG(queue)
    EEG_obj.marker_process()

def eeg(queue):
    EEG_obj = EEG(queue)
    EEG_obj.eeg_process()

def phtotocell(queue):
    EEG_obj = EEG(queue)
    EEG_obj.photocell_process()

def eyetracking(queue, pipe_in, pipe_out):
    Eyetracker_obj = Eyetracker(queue, pipe_in, pipe_out)
    Eyetracker_obj.eyetracking_process()

if __name__ == '__main__':
    
    try:
        queue = multiprocessing.Queue() # can have multiple endpoints
        pipe_in, pipe_out = multiprocessing.Pipe() #duplex=False) # only have 2 endpoints, 3 times faster than queue
        lock = multiprocessing.Lock()
        # Define processes
        
        run_eyetracking = multiprocessing.Process(name='Eyetracking', 
                target=eyetracking, args=(queue, pipe_in, pipe_out))
        run_visual = multiprocessing.Process(name='Visuals',
                target=visual, args=(queue, pipe_in, pipe_out, lock,))
        run_eeg = multiprocessing.Process(name='EEG', 
                target=eeg, args=(queue,))
        run_photocell =  multiprocessing.Process(name='Photocell', 
                target=phtotocell, args=(queue,))
        run_marker = multiprocessing.Process(name='Marker',
                target=marker, args=(queue,))

        # Run processes

        run_eyetracking.start()
        run_eeg.start()
        run_photocell.start()
        run_marker.start()
        run_visual.start()

    finally:
        
        # End processes
        
        run_photocell.join()
        run_eeg.join()
        run_visual.join()
        run_marker.join()
        run_eyetracking.join()

    # run_visual.terminate()
    # run_eyetracking.terminate()
    # run_eeg.terminate()
    # run_photocell.terminate()
    # run_marker.terminate()