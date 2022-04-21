"""
Tools for working with EEG and photocell from NVX52.

Includes tools to read streams from NVX52 encephalograph and photocell
in EEG class. 

"""

import logging
import multiprocessing
from pylsl import StreamInlet, resolve_byprop
from CONSTANTS import *
import time    

class EEG:
    """Tools for working with EEG and photocell.

    A class that contains functions to read streams from EEG and
    photocell.

    """

    def __init__(self):
        pass

    def eeg_process(self):
        """Working with EEG"""
        
        logging.info("looking for an EEG stream...")
        streams = resolve_byprop('name', EEG_STREAM)
        inlet = StreamInlet(streams[0])
        # Loop to obtain data from the EEG LSL stream
        for i in range(0, 10):
            # Request data and timestamp from the EEG stream
            sample, timestamp = inlet.pull_sample()
            print('eeg ', timestamp, sample)

    def photocell_process(self):
        """Working with photocell"""

        logging.info("looking for a photosensor stream...")
        streams = resolve_byprop('name', PHOTOSENSOR_STREAM)
        inlet = StreamInlet(streams[0])
        # Loop to obtain data from the photocell LSL stream
        for i in range(0, 20):
            # Request data and timestamp from the photocell stream
            sample, timestamp = inlet.pull_sample()
            print('photo ', timestamp, sample)

