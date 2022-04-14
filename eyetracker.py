"""
Tools for working with SMI eyetracker.

Includes tools to work with SMI eyetracker via iViewX API. Provides
functionality to connect/disconnect to SMI computer, calibrate and validate
the eyetracker, record the data and run the eyetracking process.

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
        self.res = None
        self.tracker_ip = IP_IVIEWX
        self.main_ip = IP_STIM

    def connect(self):
        """Establish a connection to iViewX on SMI computer.
        """    
        self.res = iViewXAPI.iV_Connect(c_char_p(self.tracker_ip), c_int(4444), c_char_p(self.main_ip), c_int(5555))
        if self.res == 1:
            print 'Connection established'
        else:
            print 'Connection failed. Error number: {}'.format(self.res)

    def calibrate(self):
            
        numberofPoints = 9
        displayDevice = 1 # 0 - primary, 1- secondary (?)
        pointBrightness = 250
        backgroundBrightnress = 0
        targetFile = b""
        calibrationSpeed = 0 # slow
        autoAccept  = 2 # 0 = manual, 1 = semi-auto, 2 = auto 
        targetShape = 1 # 0 = image, 1 = circle1, 2 = circle2, 3 = cross
        targetSize = 20
        WTF = 1 #do not touch -- preset?
        calibrationData = CCalibration(numberofPoints, WTF, displayDevice, calibrationSpeed, autoAccept, pointBrightness,backgroundBrightnress, targetShape, targetSize, targetFile)
        self.res = iViewXAPI.iV_SetupCalibration(byref(calibrationData))
        self.res = iViewXAPI.iV_Calibrate()

    def validate(self):
            
        self.res = iViewXAPI.iV_Validate()
        accuracy_x = []
        accuracy_y = []
        x,y = self.get_accuracy()
        accuracy_x.append(x)
        accuracy_y.append(y)  
        print 'Mean deviation x (deg): {}'.format(np.mean(accuracy_x))
        print 'Mean deviation y (deg): {}'.format(np.mean(accuracy_y))

    def get_accuracy(self):
        'updates AccuracyStruct data structure'
        self.res = iViewXAPI.iV_GetAccuracy(byref(accuracyData), c_int(0))
        dlx=accuracyData.deviationLX
        dly=accuracyData.deviationLY
        drx=accuracyData.deviationRX
        dry=accuracyData.deviationRY
        return np.mean([dlx,drx]), np.mean([dly, dry])


    def disconnect(self):

        self.res = iViewXAPI.iV_Disconnect()
        if self.res == 1:
                print("Eyetracker has been disconnected successfully")
        else:
                print("Disconnection failed. Error number: {}".format(res))

    def start_record(self):
        self.res = iViewXAPI.iV_StartRecording()
    
    def stop_record(self):
        self.res = iViewXAPI.iV_StopRecording()

    def send_message(self, message):
        self.res = iViewXAPI.iV_SendImageMessage(message)

    def save_data(self, filename):
        ''' Description
        '''
        self.res = iViewXAPI.iV_SaveData(filename, 'description', 'user', 0)

    def eyetracking_process(self):

        self.connect()
        #self.calibrate()
        #self.validate()

        #time.sleep(1)
        #self.send_message('message.jpg')
        #time.sleep(1)

        #self.stop_record()
        #self.save_data('eye_data')
        self.disconnect()


if __name__ == '__main__':
        RED = Eyetracker()
        RED.connect()
        RED.disconnect()


