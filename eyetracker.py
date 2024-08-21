'''
Tools for working with SMI eyetracker.

Includes tools to work with SMI eyetracker via iViewX API. Provides
functionality to connect/disconnect to SMI computer, calibrate
the eyetracker, validate calibration record the data and run
the eyetracking process.

To make the code works properly put files iViewXAPI.py, iViewXAPI64.dll,
iViewXAPIL64.dll, iViewXAPIR64.dll in the same directory with this file.

'''
import multiprocessing
from iViewXAPI import  *  #iViewX library
from ctypes import *
import numpy as np
import time
from CONSTANTS import *
import logging
from pylsl import StreamInlet, resolve_byprop, resolve_stream

class Eyetracker:
    '''Tools for working with SMI eyetracker via iViewX API.
    
    A class that contains functions to work with the eyetracker.
    
    '''
    def __init__(self, queue, pipe_in, pipe_out):     
        '''Initiate Eyetracker class.
        
        Keyword arguments:
        queue -- Queue object to put data in and get it (used to
                 send and detect the end mark to stop all processes)
        pipe_in -- Pipe object to send messages (used to send a mark
                   and unlock Visual process)
        pipe_out -- Pipe object to recieve messages (used to receive a 
                    mark and unlock Visual process)
        
        Attributes:
        res -- status of execution of a command from iViewXAPI
        tracker_ip -- string ip of computer connected to the eyetracker
        main_ip -- string ip of computer with main code and stimulus 
                   presentation
        codes -- dictionary with standart error codes from eyetracker
        inlet -- StreamInlet object to listen to particular stream

        '''
        self.res = None
        self.tracker_ip = IP_IVIEWX
        self.main_ip = IP_STIM
        self.queue = queue
        self.pipe_in = pipe_in
        self.pipe_out = pipe_out
        self.inlet = self.create_inlet(VISUAL_STREAM)
        self.codes = {
            1:"SUCCES: intended functionality has been fulfilled",
            2:"NO_VALID_DATA: no new data available",
            3:"CALIBRATION_ABORTED: calibration was aborted",
            100:"COULD_NOT_CONNECT: failed to establish connection",
            101:"NOT_CONNECTED: no connection established",
            102:"NOT_CALIBRATED: system is not calibrated",
            103:"NOT_VALIDATED: system is not validated",
            104:"EYETRACKING_APPLICATION_NOT_RUNNING: no SMI eye tracking application running",
            105:"WRONG_COMMUNICATION_PARAMETER: wrong port settings",
            111:"WRONG_DEVICE: eye tracking device required for this function is not connected",
            112:"WRONG_PARAMETER: parameter out of range",
            113:"WRONG_CALIBRATION_METHOD: eye tracking device required for this calibration method is not connected",
            121:"CREATE_SOCKET: failed to create sockets",
            122:"CONNECT_SOCKET: failed to connect sockets",
            123:"BIND_SOCKET: failed to bind sockets",
            124:"DELETE_SOCKET: failed to delete sockets",
            131:"NO_RESPONSE_FROM_IVIEW: no response from iView X; check iView X connection settings (IP addresses, ports) or last command",
            132:"INVALID_IVIEWX_VERSION: iView X version could not be resolved",
            133:"WRONG_IVIEWX_VERSION: wrong version of iView X",
            171:"ACCESS_TO_FILE: failed to access log file",
            181:"SOCKET_CONNECTION: socket error during data transfer",
            191:"EMPTY_DATA_BUFFER: recording buffer is empty",
            192:"RECORDING_DATA_BUFFER: recording is activated",
            193:"FULL_DATA_BUFFER: data buffer is full",
            194:"IVIEWX_IS_NOT_READY: iView X is not ready",
            201:"IVIEWX_NOT_FOUND: no installed SMI eye tracking application detected",
            220:"COULD_NOT_OPEN_PORT: could not open port for TTL output",
            221:"COULD_NOT_CLOSE_PORT: could not close port for TTL output",
            222:"AOI_ACCESS: could not access AOI data",
            223:"AOI_NOT_DEFINED: no defined AOI found",
            'unknown': "unknown error with decimal code {}; please refer to the iViewX SDK Manual".format(self.res)
            }

    def connect(self):
        '''Establish a connection to iViewX on SMI computer.'''

        self.res = iViewXAPI.iV_Connect(c_char_p(self.tracker_ip), c_int(4444),
                                        c_char_p(self.main_ip), c_int(5555))
        if self.res == 1:
            logging.info('Connection established')
        else:
            logging.error(self.errorstring(self.res))

    def calibrate(self):
        '''Calibrate the eyetracker.'''    
        
        # Initialize variables
        numberofPoints = 9  # Number of points for calibration
        displayDevice = 1  # 0 - primary, 1- secondary
        pointBrightness = 250  # Color of calibration points
        backgroundBrightnress = 0  # Color of background during calibration 
        targetFile = b''  # Unknown paremeter. Better don`t change.
        calibrationSpeed = 0  # slow
        autoAccept  = 1  # 0 = manual, 1 = semi-auto, 2 = auto 
        targetShape = 1  # 0 = image, 1 = circle1, 2 = circle2, 3 = cross
        targetSize = 20  # Size of calibration points
        WTF = 1  # Unknown parameter. Better don`t change.
        
        # Create and apply C structure for calibration 
        calibrationData = CCalibration(numberofPoints, WTF, displayDevice,
                                        calibrationSpeed, autoAccept, pointBrightness,
                                        backgroundBrightnress, targetShape,
                                        targetSize, targetFile)
        self.res = iViewXAPI.iV_SetupCalibration(byref(calibrationData))
        
        # Change coordinates for calibration points 
        new_positions= [(840, 525),(280,60), (280, 990), (1400, 60), (1400,990),
                        (280, 525), (1400, 525), (840, 60), (840, 990)]
        for i in range(len(new_positions)):
            self.res=iViewXAPI.iV_ChangeCalibrationPoint(i+1,new_positions[i][0],
                                                         new_positions[i][1]) 
        
        # Run calibration
        self.res = iViewXAPI.iV_Calibrate()
        if self.res == 1:
            logging.info('Eyetracker calibration started')
        else:
            logging.error(self.errorstring(self.res))

    def validate(self, n=3):
        '''Validate the calibration of the eyetracker n times.

        Keyword arguments:
        n -- integer, how many times should run validation
        
        Variables:
        accuracy_x -- list of calibration accuracy along X axis from n validations
        accuracy_y -- list of calibration accuracy along Y axis from n validations

        '''    
        accuracy_x = []
        accuracy_y = []
        
        for i in range(n):
            # Run validation
            self.res = iViewXAPI.iV_Validate()
            if self.res == 1:
                logging.info('Eyetracker validation started {} time'.format(i+1))
            else:
                logging.error(self.errorstring(self.res))
            # Get calibration accuracy from eyetracker
            x,y = self.get_accuracy()   
            accuracy_x.append(x)
            accuracy_y.append(y)  
        
        logging.info('Mean deviation x (deg): {}'.format(np.mean(accuracy_x)))
        logging.info('Mean deviation y (deg): {}'.format(np.mean(accuracy_y)))

    def get_accuracy(self):
        '''Get accuracy data from the eyetracker.
        
        Variables:
        dlx(y) -- accuracy data from left eye along X(Y) axis
        drx(y) -- accuracy data from right eye along X(Y) axis

        '''
        # Get accuracy from last validation
        self.res = iViewXAPI.iV_GetAccuracy(byref(accuracyData), c_int(0))
        if self.res == 1:
            pass
        else:
            logging.error(self.errorstring(self.res))
        
        # Extract accuracy along axes
        dlx=accuracyData.deviationLX
        dly=accuracyData.deviationLY
        drx=accuracyData.deviationRX
        dry=accuracyData.deviationRY
        
        # Return mean accuracy along X and Y axes
        return np.mean([dlx,drx]), np.mean([dly, dry])


    def disconnect(self):
        '''Stop the connection to iViewX on SMI computer.'''
        
        self.res = iViewXAPI.iV_Disconnect()
        if self.res == 1:
            logging.info('Eyetracker has been disconnected successfully')
        else:
            logging.error(self.errorstring(self.res))

    def start_record(self):
        '''Start recording eyetracking data.'''
        
        self.res = iViewXAPI.iV_StartRecording()
        if self.res == 1:
            logging.info('Eyetracker recording started')
        else:
            logging.error(self.errorstring(self.res))
    
    def stop_record(self):
        '''Stop recording eyetracking data.'''
        
        self.res = iViewXAPI.iV_StopRecording()
        if self.res == 1:
            logging.info('Eyetracker recording stopped')
        else:
            logging.error(self.errorstring(self.res))

    def send_message(self, message):
        '''Send a message with a marker to the eyetracker.
        
        Keyword arguments:
        message -- a string with a message, must have .jpg extencion

        '''
        self.res = iViewXAPI.iV_SendImageMessage(message)
        if self.res != 1:
            logging.error(self.errorstring(self.res))

    def save_data(self, filename):
        '''Save eyetracking data on the SMI computer.
        
        Keyword arguments:
        filename -- string with the name for the file

        '''
        self.res = iViewXAPI.iV_SaveData(filename, 'description', 'user', 0)
        if self.res == 1:
            logging.info('Eyetracking data saved')
        else:
            logging.error(self.errorstring(self.res))

    def create_inlet(self, stream_type):
        '''Create inlet to read a stream.
        
        Keyword arguments:
        stream_type -- name of a stream to read (see CONSTANTS)
        
        Variables:
        streams -- all streams in the environment corresponds to request
        
        Returns:
        inlet -- StreamInlet object to listen to particular stream

        '''
        streams = resolve_byprop('name', stream_type)
        inlet = StreamInlet(streams[0])
        return inlet 
    
    def errorstring(self, returncode):
        '''Returns a string with a description of the error associated with given
           return code. Adapted from PyGaze/libsmi.py.
           
        Keyword arguments:
        returncode -- errorcode from iViewXAPI (res variable)
        
        Returns:
        errorstring -- string describing the error associated with specified code
        
        '''
        if returncode in self.codes.keys():
            return self.codes[returncode]
        else:
            return self.codes['unknown']

    def eyetracking_process(self):
        '''Main eyetracking process.
        
        The process used in the experiment.

        '''
        try:
            logging.info('Eyetraking process started')

            self.connect()
            self.calibrate()
            self.validate(1)

            self.start_record()
            # Release Visual process
            self.pipe_in.send(int(1))
            # Check for the end mark and send marker if available  
            while self.queue.empty():
                sample, timestamp = self.inlet.pull_sample(timeout=5)
                if sample != None:
                    self.send_message('{}, {}.jgp'.format(sample, timestamp))
            # Stop recording and save data
            self.stop_record()
            self.save_data('{}'.format(FILECODE))
            self.disconnect()
        finally:
            pass

        # self.pipe_in.send(int(1)) # If need to skip eyetracking and just record eeg
    
        
if __name__ == '__main__':
        RED = Eyetracker()
        RED.eyetracking_process()

