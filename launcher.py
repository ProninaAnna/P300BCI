'''
Run the experiment.

Subsequently launches distinct processes for eyetracking, visual stimuli
demonstration, EEG, photocell ans marker recording.

'''
import multiprocessing
import logging
from eeg import EEG
from eyetracker import Eyetracker
from visual import Visual
from CONSTANTS import *

# Setup logger to print ordered messages in terminal
logging.basicConfig(format='%(levelname)s	%(processName)s	%(message)s',
                    level=logging.INFO)
logging.getLogger()

# Create structures for processes
def visual(queue, pipe_in, pipe_out, lock):
    '''Define what Visual process (see below) should run.'''
    
    Visual_obj = Visual(queue, pipe_in, pipe_out, lock)
    Visual_obj.visual_process()

def marker(queue):
    '''Define what Marker process (see below) should run.'''
    
    EEG_obj = EEG(queue)
    EEG_obj.marker_process()

def eeg(queue):
    '''Define what EEG process (see below) should run.'''
    
    EEG_obj = EEG(queue)
    EEG_obj.eeg_process()

def phtotocell(queue):
    '''Define what Photocell process (see below) should run.'''
    
    EEG_obj = EEG(queue)
    EEG_obj.photocell_process()

def eyetracking(queue, pipe_in, pipe_out):
    '''Define what Eyetracking process (see below) should run'''
    
    Eyetracker_obj = Eyetracker(queue, pipe_in, pipe_out)
    Eyetracker_obj.eyetracking_process()

def get_communication_tools():
    '''Create tools to exchange information between processes.
    
    Returns:
    queue -- Queue object to put data in and get it (used to
             send and detect the end mark to stop all processes)
    pipe_in -- Pipe object to send messages (used to send a mark
               and unlock Visual process)
    pipe_out -- Pipe object to recieve messages (used to receive a 
                mark and unlock Visual process)
    lock -- Lock object to make one process wait until another 
            unlock it (used to make Visual process wait Eyetracking)
    
    '''
    queue = multiprocessing.Queue()
    pipe_in, pipe_out = multiprocessing.Pipe()
    lock = multiprocessing.Lock()
    return(queue, pipe_in, pipe_out, lock)


if __name__ == '__main__':
    
    try:
        # Get tools to communicate between processes
        queue, pipe_in, pipe_out, lock = get_communication_tools()
        
        # Define processes
        run_eyetracking = multiprocessing.Process(name='Eyetracking', 
                target=eyetracking, args=(queue, pipe_in, pipe_out))
        run_eeg = multiprocessing.Process(name='EEG', 
                target=eeg, args=(queue,))
        run_photocell =  multiprocessing.Process(name='Photocell', 
                target=phtotocell, args=(queue,))
        run_marker = multiprocessing.Process(name='Marker',
                target=marker, args=(queue,))
        run_visual = multiprocessing.Process(name='Visual', 
                target=visual, args=(queue, pipe_in, pipe_out, lock,))

        # Run processes
        run_eyetracking.start()
        run_eeg.start()
        run_photocell.start()
        run_marker.start()
        run_visual.start()

    finally:
        
        # End processes
        run_eyetracking.join()
        run_eeg.join()
        run_photocell.join()
        run_marker.join()
        run_visual.join()