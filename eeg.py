"""
Tools for working with EEG and photocell from NVX52.

Includes tools to read streams from NVX52 encephalograph and photocell
in EEG class. 

"""

import logging
import multiprocessing
from pylsl import StreamInlet, resolve_byprop, resolve_stream
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
        for i in range(1):
            # Request data and timestamp from the EEG stream
            sample, timestamp = inlet.pull_sample()
            print('eeg ', timestamp, sample)

    def marker_process(self):
        """Working with visual process marker stream"""
        streams = resolve_byprop('name', VISUAL_STREAM_NAME)
        inlet = StreamInlet(streams[0])
        # Loop to test visual stream process markers
        for i in range(2):
            sample, timestamp = inlet.pull_sample()
            print('marker', timestamp, sample)
    
    def photocell_process(self):
        """Working with photocell"""

        logging.info("looking for a photosensor stream...")
        streams = resolve_byprop('name', PHOTOSENSOR_STREAM)
        inlet = StreamInlet(streams[0])
        # Loop to obtain data from the photocell LSL stream
        for i in range(len(GROUP1+GROUP2)):
            # Request data and timestamp from the photocell stream
            sample, timestamp = inlet.pull_sample()
            print('photo ', timestamp, sample)

