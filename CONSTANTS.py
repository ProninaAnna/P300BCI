EEG_STREAM = 'NVX52_Data' # name of the EEG data stream 
PHOTOSENSOR_STREAM = 'NVX52_Events' # name of the photosensor data stream

IP_IVIEWX = '192.168.2.43' # static IP of the iViewX laptop
IP_STIM = '192.168.2.173' # static IP of the stimulus PC

BACKCOL=(-1,-1,-1) # background color
FIXCOL=(1,1,1) # fixation mark color

SIZE = (1680,1050) # monitor screen resolution (2560, 1440)
WIDTH = 47.5 # (25.41 deg) monitor screen width, 59.5 cm 
DISTANCE = 50 # distance between subject and screen, cm

CENTER = (0,0) # fixation mark coordinates, deg
PHOTOSENSOR_POS = (25, 14.4) # photosensor stimulus coordinates, deg

STIM_GROUP_NUMBER = 3 # number of groups in which target shall flash (2 for row-column speller)
STIM_NAMES = [item for item in u'abcdefghijklmnopqrstuvwxyz_1234567890!?.,;:"()+=-~[]\/'] # available stimuli names, unicode
STIM_SIZE = None
STIM_POS = None
