'''
List of available constants to setup and customize P300 BCI
'''

EEG_STREAM = 'NVX52_Data' # name of the EEG data stream 
PHOTOSENSOR_STREAM = 'NVX52_Events' # name of the photosensor data stream

IP_IVIEWX = '192.168.2.43' # static IP of the iViewX laptop
IP_STIM = '192.168.2.173' # static IP of the stimulus PC

MONITOR = 'Dell' # monitor name
MONITOR_N = 2
SIZE = (1680,1050) # screen resolution (2560, 1440), px
WIDTH = 47.5 # monitor screen width, 59.5 cm 
DISTANCE = 56 # distance between subject and screen, cm

VIS_MODE = 'spiral' # can be 'rc' row-column visuals or 'spiral' for spiral visuals
SCREEN_UNITS = 'deg' # units 
CENTER = (0,0) # fixation mark coordinates
PHOTOSENSOR_POS = (25, 14.4) # photosensor stimulus coordinates
STIM_NAMES = [item for item in u'qwertyuiopasdfghjklzxcvbnm_1234567890!?.,;:"()+=-~[]\/'] # available stimuli names, unicode
STIM_SIZE = ( 5.5, 3.5, 1.5) # stimuli sizes
STIM_POS = [(0,-12.000), (-7.713,-9.193), (-11.818,-2.084), (-10.392,6.000), (-4.104,11.276),
            (4.104,11.276), (10.392,6.000), (11.818,-2.084), (7.713,-9.193),
            (0,7.000), (4.500,5.362), (6.894,1.216), (6.062,-3.500), (2.394,-6.578),
            (-2.394,-6.578), (-6.062,-3.500), (-6.894,1.216), (-4.500,5.362),
            (0,-3.500), (-2.250,-2.681), (-3.447,-0.608), (-3.031,1.750), (-1.197,3.289),
            (1.197,3.289), (3.031,1.750), (3.447,-0.608), (2.250,-2.681)] # stimuli positions coordinates
STIM_GROUPS = [(),(),()]

BACKCOL=(-1,-1,-1) # background color
FIXCOL=(1,1,1) # fixation mark color
STIMCOL=(1,1,1) # stimuli color