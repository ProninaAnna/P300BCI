"""
Tools for working with EEG and photocell from NVX52.

Includes tools to read streams from NVX52 encephalograph and photocell
in EEG class. 

"""

import logging
import multiprocessing
from pylsl import StreamInlet, resolve_byprop, resolve_stream
from CONSTANTS import *
import time, os, psutil

class EEG:
    """Tools for working with EEG and photocell.

    A class that contains functions to read streams from EEG and
    photocell.

    """

    def __init__(self):
        pass

    def create_inlet(self, stream_type):
        '''Create inlet to read a stream'''

        streams = resolve_byprop('name', stream_type)
        inlet = StreamInlet(streams[0])
        return inlet 
    
    def write_data(self, filename, inlet):
        '''Read data from stream and write it to file'''
        
        with open(filename, 'w') as f:
            while True:
                sample, timestamp = inlet.pull_sample()
                name = multiprocessing.current_process().name
                f.write('{}: {} {}\n'.format(name, timestamp, sample))   
            
    def eeg_process(self):
        """Working with EEG"""
        
        logging.info("looking for an EEG stream...")
        inlet = self.create_inlet(EEG_STREAM)
        self.write_data(r'F:\\Timofey\\test_write_eeg.txt', inlet)
       
    def marker_process(self):
        """Working with visual process marker stream"""

        logging.info("looking for a marker strean")
        inlet = self.create_inlet(VISUAL_STREAM_NAME)
        self.write_data(r'F:\\Timofey\\test_write_marker.txt', inlet)
        
    def photocell_process(self):
        """Working with photocell"""

        logging.info("looking for a photosensor stream...")
        inlet = self.create_inlet(PHOTOSENSOR_STREAM)
        self.write_data(r'F:\\Timofey\\test_write_photocell.txt', inlet)


