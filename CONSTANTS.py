'''
List of available constants to setup and customize P300 BCI
'''

EEG_STREAM = 'NVX52_Data' # name of the EEG data stream 
PHOTOSENSOR_STREAM = 'NVX52_Events' # name of the photosensor data stream
VISUAL_STREAM = 'VisualProcessMarkerStream'
TRIAL_START = 777 # start marker for LSL
TRIAL_END= 888 # stop marker for LSL

IP_IVIEWX = '192.168.2.43' # static IP of the iViewX laptop
IP_STIM = '192.168.2.173' # static IP of the stimulus PC

MONITOR = 'Dell' # monitor name
MONITOR_N = 1
SIZE = (1680,1050) # screen resolution (2560, 1440), px
WIDTH = 47.5 # monitor screen width, 59.5 cm 
DISTANCE = 56 # distance between subject and screen, cm

SCREEN_UNITS = 'deg' # coordinates units 
CENTER = (0,0) # fixation mark coordinates
PHOTOSENSOR_POS = (25.5, 14.4) # photosensor stimulus coordinates
STIM_NAMES = [item for item in u'qwertyuiopasdfghjklzxcvbnm_1234567890!?.,;:"()+=-~[]\/'.upper()] # available stimuli names, unicode
GROUP1 = {0:(0, 11, 21), 1:(1, 12, 22), 2:(2, 13, 23), 3:(3, 14, 24), 4:(4, 15, 25), 5:(5, 16, 26), 6:(6, 17, 18), 7:(7, 9, 19), 8:(8, 10, 20)} # groups of stims ("rows and colums")
GROUP2 = {9:(0, 17, 24), 10:(1, 9, 25), 11:(2, 10, 26), 12:(3, 11, 18), 13:(4, 12, 19), 14:(5, 13, 20), 15:(6, 14, 21), 16:(7, 15, 22), 17:(8, 16, 23)}
STIM_SIZE = ( 5.5, 3.5, 1.5) # stimuli sizes
STIM_POS = [(0,-12.000), (-7.713,-9.193), (-11.818,-2.084), 
            (-10.392,6.000), (-4.104,11.276), (4.104,11.276), 
            (10.392,6.000), (11.818,-2.084), (7.713,-9.193),
            (0,7.000), (4.500,5.362), (6.894,1.216), 
            (6.062,-3.500), (2.394,-6.578), (-2.394,-6.578), 
            (-6.062,-3.500), (-6.894,1.216), (-4.500,5.362),
            (0,-3.500), (-2.250,-2.681), (-3.447,-0.608), 
            (-3.031,1.750), (-1.197,3.289), (1.197,3.289), 
            (3.031,1.750), (3.447,-0.608), (2.250,-2.681)] # stimuli positions coordinates

FLASH = 0.025 # flashing time, s
ISI = 0.075 # inter stimulus interval, s
TRIAL_LEN = 2 # number of flashes in one trial

BACKCOL=(-1,-1,-1) # background color
FIXCOL=(1,1,1) # fixation mark color
STIMCOL=(1,1,1) # stimuli color
QUECOL=(1.0,-1,-1) # que color

