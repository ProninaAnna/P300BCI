import multiprocessing
from pylsl import StreamInlet, resolve_byprop

class EEG:
    def __init__(self):
        pass

    def eeg_process(self):
        print("looking for an EEG stream...")
        streams = resolve_byprop('name', 'NVX52_Data')
        inlet = StreamInlet(streams[0])
        for i in range(0, 10):
            sample, timestamp = inlet.pull_sample()
            print(timestamp, sample)

    def photocell_process(self):
        pass