"""
Tools for working with SMI eyetracker.

Includes tools to work with SMI eyetracker via iViewX API. Provides
functionality to connect/disconnect to SMI computer, calibrate and validate
the eyetracker, record the data and run the eyetracking process.

To make the code works properly put files iViewXAPI.py, iViewXAPI64.dll,
iViewXAPIL64.dll, iViewXAPIR64.dll in the same directory with this file.

"""

import multiprocessing
from iViewXAPI import  *  #iViewX library
from ctypes import *
import numpy as np
import time
from CONSTANTS import *
import logging


class Eyetracker:
    """Tools for working with SMi eyetracker via iViewX API.
    
    A class that contains functions to work with the eyetracker.
    
    """

    def __init__(self):     
        """Initiate Eyetracker class.
        
        Keypord arguments:
        res -- status of execution of a command from iViewXAPI
        tracker_ip -- ip of computer connected to the eyetracker
        main_ip -- ip of computer with main code and stimulus presentation

        """
        
        self.res = None
        self.tracker_ip = IP_IVIEWX
        self.main_ip = IP_STIM

    def connect(self):
        """Establish a connection to iViewX on SMI computer."""    
        self.res = iViewXAPI.iV_Connect(c_char_p(self.tracker_ip), c_int(4444),
                                        c_char_p(self.main_ip), c_int(5555))
        if self.res == 1:
            print('Connection established')
        else:
            print('Connection failed. Error number: {}'.format(self.res))

    def calibrate(self):
        """Calibrate the eyetracker."""    
        # Initialize variables
        numberofPoints = 9  # Number of points for calibration
        displayDevice = 1  # 0 - primary, 1- secondary
        pointBrightness = 250  # Color of calibration points
        backgroundBrightnress = 0  # Color of background during calibration 
        targetFile = b""  # ???
        calibrationSpeed = 0  # slow
        autoAccept  = 2  # 0 = manual, 1 = semi-auto, 2 = auto 
        targetShape = 1  # 0 = image, 1 = circle1, 2 = circle2, 3 = cross
        targetSize = 20  # Size of calibration points
        WTF = 1  #do not touch -- Unknown parameter
        # Create C structure for calibration 
        calibrationData = CCalibration(numberofPoints, WTF, displayDevice,
                                        calibrationSpeed, autoAccept, pointBrightness,
                                        backgroundBrightnress, targetShape, targetSize, targetFile)
        self.res = iViewXAPI.iV_SetupCalibration(byref(calibrationData))
        self.res = iViewXAPI.iV_Calibrate()
        if self.res == 1:
            print('Eyetracker calibration started')
        else:
            print('Failed to calibrate eyetracker. Error number: {}'.format(self.res))

    def validate(self, n=1):
        """Validate the calibration of the eyetracker n times.

        Keyword arguments:
        n -- integer, how many times should run validation
        accuracy_x -- list of calibration accuracy along X axis from n validations
        accuracy_y -- list of calibration accuracy along Y axis from n validations

        """    
        accuracy_x = []
        accuracy_y = []
        
        for i in range(n):
            self.res = iViewXAPI.iV_Validate()
            if self.res == 1:
                print('Eyetracker validation started {} time'.format(i+1))
            else:
                print('Failed to validate eyetracker. Error number: {}'.format(self.res))
            x,y = self.get_accuracy()  # Get calibration accuracy from eyetracker 
            accuracy_x.append(x)
            accuracy_y.append(y)  
        
        print('Mean deviation x (deg): {}'.format(np.mean(accuracy_x)))
        print('Mean deviation y (deg): {}'.format(np.mean(accuracy_y)))

    def get_accuracy(self):
        """Get accuracy data from the eyetracker.
        
        Keyword arguments:
        dlx(y) -- accuracy data from left eye along X(Y) axis
        drx(y) -- accuracy data from right eye along X(Y) axis

        """
        self.res = iViewXAPI.iV_GetAccuracy(byref(accuracyData), c_int(0))
        if self.res == 1:
            pass
        else:
            print('Failed to get eyetracker accuracy data. Error number: {}'.format(self.res))
        dlx=accuracyData.deviationLX
        dly=accuracyData.deviationLY
        drx=accuracyData.deviationRX
        dry=accuracyData.deviationRY
        # Return mean accuracy along X and Y axes
        return np.mean([dlx,drx]), np.mean([dly, dry])


    def disconnect(self):
        """Stop the connection to iViewX on SMI computer."""
        self.res = iViewXAPI.iV_Disconnect()
        if self.res == 1:
            print("Eyetracker has been disconnected successfully")
        else:
            print("Disconnection failed. Error number: {}".format(self.res))

    def start_record(self):
        """Start recording eyetracking data"""
        self.res = iViewXAPI.iV_StartRecording()
        if self.res == 1:
            print("Eyetracker recording started")
        else:
            print("Failed to start eyetracker recording. Error number: {}".format(self.res))
    
    def stop_record(self):
        """Stop recording eyetracking data"""
        self.res = iViewXAPI.iV_StopRecording()
        if self.res == 1:
            print("Eyetracker recording stopped")
        else:
            print("Failed to stop eyetracker recording. Error number: {}".format(self.res))

    def send_message(self, message):
        """Send a message with a marker to the eyetracker.
        
        Keyword arguments:
        message -- string with a message, should have .jpg extencion (?)

        """
        self.res = iViewXAPI.iV_SendImageMessage(message)
        if self.res == 1:
            print("Message to the eyetracker has been sent successfully")
        else:
            print("Failed to send message to the eyetracker. Error number: {}".format(self.res))

    def save_data(self, filename):
        '''Save eyetracking data on the SMI computer
        
        Keyword arguments:
        filename -- string with the name for the file

        '''
        self.res = iViewXAPI.iV_SaveData(filename, 'description', 'user', 0)
        if self.res == 1:
            print("Eyetracking data saved")
        else:
            print("Failed save eyetracking data. Error number: {}".format(self.res))

    def eyetracking_process(self):
        """Main eyetracking process.
        
        The process used in the experiment.

        """
        self.connect()
        self.calibrate()
        self.validate(3)

        #time.sleep(1)
        #self.send_message('message.jpg')
        #time.sleep(1)

        #self.stop_record()
        #self.save_data('eye_data')
        self.disconnect()


if __name__ == '__main__':
        RED = Eyetracker()
        RED.eyetracking_process()

