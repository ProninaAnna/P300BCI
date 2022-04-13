import multiprocessing
import logging
from eeg import *
from eyetracker import *
from visual import *
from CONSTANTS import*

logging.basicConfig(level=logging.INFO)

if __name__ == '__main__':
    
    EEG_obj = EEG()
    Visual_obj = Visual()
    Eyetracker_obj = Eyetracker()

    try:
        run_eyetracking = multiprocessing.Process(name = 'Eyetracking', target = Eyetracker_obj.eyetracking_process, args=())
        run_visual = multiprocessing.Process(name = 'Visuals', target = Visual_obj.visual_process, args=())
        run_eeg = multiprocessing.Process(name = 'EEG', target = EEG_obj.eeg_process, args=())
        run_photocell =  multiprocessing.Process(name = 'Photocell', target = EEG_obj.photocell_process, args=())

        run_eyetracking.start()
        run_visual.start()
        run_eeg.start()
        run_photocell.start()
        
    finally:
        run_photocell.join()
        run_eeg.join()
        run_visual.join()
        run_eyetracking.join()