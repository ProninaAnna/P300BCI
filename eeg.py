import multiprocessing
from pylsl import StreamInlet, resolve_byprop
from CONSTANTS import *

class EEG:
    def __init__(self):
        pass

    def eeg_process(self):
        print("looking for an EEG stream...")
        streams = resolve_byprop('name', EEG_STREAM)
        inlet = StreamInlet(streams[0])
        for i in range(0, 10):
            sample, timestamp = inlet.pull_sample()
            print('eeg ', timestamp, sample)

    def photocell_process(self):
        print("looking for a photosensor stream...")
        streams = resolve_byprop('name', PHOTOSENSOR_STREAM)
        inlet = StreamInlet(streams[0])
        for i in range(0, 10):
            sample, timestamp = inlet.pull_sample()
            print('photo ', timestamp, sample)

