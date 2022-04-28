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

logging.basicConfig(format='%(levelname)s	%(processName)s	%(message)s', level=logging.INFO)
logging.getLogger()

# Create structures for processes

def visual():
    Visual_obj = Visual()
    Visual_obj.visual_process()

def eeg():
    EEG_obj = EEG()
    EEG_obj.eeg_process()

def phtotocell():
    EEG_obj = EEG()
    EEG_obj.photocell_process()

def eyetracking():
    Eyetracker_obj = Eyetracker()
    Eyetracker_obj.eyetracking_process()

if __name__ == '__main__':
    
    try:
        
        # Define processes
        
        # run_eyetracking = multiprocessing.Process(name='Eyetracking', 
        #         target=eyetracking, args=())
        run_visual = multiprocessing.Process(name='Visuals',
                target=visual, args=())
        run_eeg = multiprocessing.Process(name='EEG', 
                target=eeg, args=())
        run_photocell =  multiprocessing.Process(name='Photocell', 
                target=phtotocell, args=())

        # Run processes

        # run_eyetracking.start()
        run_eeg.start()
        run_photocell.start()
        run_visual.start()

    finally:
        
        # End processes
        
        run_photocell.join()
        run_eeg.join()
        run_visual.join()
        # run_eyetracking.join()