
import multiprocessing
from source import *

#def eyetracking_process(namespace):
#    pass


def streaming_process(namespace):
    eeg = Record(namespace)
    eeg.start_record()

def visuals_process(namespace):
    visuals = Visuals(namespace)
    visuals.procede()

if __name__ == '__main__':
    try:
        manager = multiprocessing.Manager()
        Global = manager.Namespace()
        
        #run_eyetracking = multiprocessing.Process(name = 'Eyetracking', target = eyetracking_process, args=(Global,))
        run_visuals = multiprocessing.Process(name = 'Visuals', target = visuals_process,args=(Global,))
        run_streaming = multiprocessing.Process(name = 'Streaming', target = streaming_process,args=(Global,))
        
        #run_eyetracking.start()
        run_visuals.start()
        run_streaming.start()
    finally:
        run_streaming.join()
        run_visuals.join()
        #run_eyetracking.join()

