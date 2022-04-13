EEG_STREAM = 'NVX52_Data' # name of the EEG data stream 
PHOTOSENSOR_STREAM = 'NVX52_Events' # name of the photosensor data stream

IP_IVIEWX = '192.168.2.43' # static IP of the iViewX laptop
IP_STIM = '192.168.2.173' # static IP of the stimulus PC

BACKCOL=(-0.5,-0.5,-0.5) # background color
FIXCOL=(1,1,1) # fixation mark color

SIZE = (2560, 1440) # (1680,1050) monitor screen resolution 
WIDTH = 59.5 # monitor screen width, cm
DISTANCE = 50 # distance between subject and screen, cm

CENTER = (0,0) # fixation mark coordinates, deg
PHOTOSENSOR_POS = (0.92,0.83) # photosensor stimulus coordinates, deg

STIM_GROUP_NUMBER = 3 # number of groups in which target shall flash (2 for row-column speller)
STIM_NAMES = [item for item in u'abcdefghijklmnopqrstuvwxyz_1234567890!?.,;:"()+=-~[]{}\/'] # available stimuli names, unicode
STIM_SIZE = None
STIM_POS = None