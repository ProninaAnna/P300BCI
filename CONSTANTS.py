# =================
# === STREAMING ===
# =================

EEG_STREAM = 'NVX52_Data' # name of EEG data stream 
PHOTOSENSOR_STREAM = 'NVX52_Events' # name of photosensor data stream
MESSAGE_STREAM = 'Messages'

# ===========
# == DATA ===
# ===========

FILEPATH = r'C:\\Users\\apron\\Documents\\Google Диск\\PROJECTS\\ind-bci\\BCI\\'

# ===============
# === VISUALS ===
# ===============

DIR = r'C:\Users\apron\Documents\GitHub\Gaze-Independent-Speller' #os.getcwd() 

BACKCOL=(-0.5,-0.5,-0.5) #background color
FIXCOL=(1,1,1) #fixation mark color

C1=[(0,-1.500), (-0.964,-1.149), (-1.477,-0.260), (-1.299,0.750), (-0.513,1.410), 
    (0.513,1.410), (1.299,0.750), (1.477,-0.260), (0.964,-1.149)] # coordinates of inner circle, deg
C2=[(0,3.500),(2.250,2.681),(3.447,0.608),(3.031,-1.750),(1.197,-3.289),
    (-1.197,-3.289),(-3.031,-1.750),(-3.447,0.608),(-2.250,2.681)] # coordinates of middle circle, deg
C3=[(0,-7.000), (-4.500,-5.362), (-6.894,-1.216), (-6.062,3.500), (-2.394,6.578),
    (2.394,6.578), (6.062,3.500), (6.894,-1.216), (4.500,-5.362)] # coordinates of outer circle, deg

BLOCK1=['D', 'K', 'O', 'Y', 'N', 'L', '*', 'H', 'P']
BLOCK2=['E', 'F', 'X', 'A', 'M', 'J', 'I', 'W', 'U']
BLOCK3=['S', 'B', 'Z', 'T', 'R', 'V', 'C', 'Q', 'G']

STIM = 0.050 # duration of stimulus (flash), s
ISI = 0.100 # duration of inter-stimulus interval, s
TRIALREPEATS = 20 # cycles of stimulation
TRIALNUMBER = 20 # number of trials 
SIZE = (1920, 1080) #(1680,1050) monitor resolution 
CENTER = (0,0) # fixation mark coordinates, deg
DISTANCE = 75 # distance between subject and screen, cm
WIDTH = 47.4 # screen width , cm (31)
LETTERSIZE = [0.8, 1.85, 3.3] # size of letter images, deg
BACKCOL=(-0.5,-0.5,-0.5) # background color
FIXCOL=(1,1,1) # fixation mark color

CIRCLES={'J':[C1[0], (DIR+r'\Stimuli\10-0.png'), (DIR+r'\Stimuli\10-1.png'), LETTERSIZE[0]], 
              'V':[C1[1], (DIR+r'\Stimuli\22-0.png'), (DIR+r'\Stimuli\22-1.png'), LETTERSIZE[0]], 
              'P':[C1[2], (DIR+r'\Stimuli\16-0.png'), (DIR+r'\Stimuli\16-1.png'), LETTERSIZE[0]], 
              'U':[C1[3], (DIR+r'\Stimuli\21-0.png'), (DIR+r'\Stimuli\21-1.png'), LETTERSIZE[0]], 
              'G':[C1[4], (DIR+r'\Stimuli\7-0.png'), (DIR+r'\Stimuli\7-1.png'), LETTERSIZE[0]], 
              'Y':[C1[5], (DIR+r'\Stimuli\25-0.png'), (DIR+r'\Stimuli\25-1.png'), LETTERSIZE[0]],
              'X':[C1[6], (DIR+r'\Stimuli\24-0.png'), (DIR+r'\Stimuli\24-1.png'), LETTERSIZE[0]], 
              'Z':[C1[7], (DIR+r'\Stimuli\26-0.png'), (DIR+r'\Stimuli\26-1.png'), LETTERSIZE[0]], 
              '*':[C1[8], (DIR+r'\Stimuli\27-0.png'), (DIR+r'\Stimuli\27-1.png'), LETTERSIZE[0]],
              'F':[C2[0], (DIR+r'\Stimuli\6-0.png'), (DIR+r'\Stimuli\6-1.png'), LETTERSIZE[1]], 
              'B':[C2[1], (DIR+r'\Stimuli\2-0.png'), (DIR+r'\Stimuli\2-1.png'), LETTERSIZE[1]], 
              'N':[C2[2], (DIR+r'\Stimuli\14-0.png'), (DIR+r'\Stimuli\14-1.png'), LETTERSIZE[1]], 
              'M':[C2[3], (DIR+r'\Stimuli\13-0.png'), (DIR+r'\Stimuli\13-1.png'), LETTERSIZE[1]], 
              'R':[C2[4], (DIR+r'\Stimuli\18-0.png'), (DIR+r'\Stimuli\18-1.png'), LETTERSIZE[1]], 
              'H':[C2[5], (DIR+r'\Stimuli\8-0.png'), (DIR+r'\Stimuli\8-1.png'), LETTERSIZE[1]], 
              'W':[C2[6], (DIR+r'\Stimuli\23-0.png'), (DIR+r'\Stimuli\23-1.png'), LETTERSIZE[1]],
              'Q':[C2[7], (DIR+r'\Stimuli\17-0.png'), (DIR+r'\Stimuli\17-1.png'), LETTERSIZE[1]], 
              'K':[C2[8], (DIR+r'\Stimuli\11-0.png'), (DIR+r'\Stimuli\11-1.png'), LETTERSIZE[1]],
              'I':[C3[0], (DIR+r'\Stimuli\9-0.png'), (DIR+r'\Stimuli\9-1.png'), LETTERSIZE[2]], 
              'C':[C3[1], (DIR+r'\Stimuli\3-0.png'), (DIR+r'\Stimuli\3-1.png'), LETTERSIZE[2]], 
              'D':[C3[2], (DIR+r'\Stimuli\4-0.png'), (DIR+r'\Stimuli\4-1.png'), LETTERSIZE[2]], 
              'E':[C3[3], (DIR+r'\Stimuli\5-0.png'), (DIR+r'\Stimuli\5-1.png'), LETTERSIZE[2]], 
              'S':[C3[4], (DIR+r'\Stimuli\19-0.png'), (DIR+r'\Stimuli\19-1.png'), LETTERSIZE[2]], 
              'O':[C3[5], (DIR+r'\Stimuli\15-0.png'), (DIR+r'\Stimuli\15-1.png'), LETTERSIZE[2]], 
              'A':[C3[6], (DIR+r'\Stimuli\1-0.png'), (DIR+r'\Stimuli\1-1.png'), LETTERSIZE[2]], 
              'T':[C3[7], (DIR+r'\Stimuli\20-0.png'), (DIR+r'\Stimuli\20-1.png'), LETTERSIZE[2]],
              'L':[C3[8], (DIR+r'\Stimuli\12-0.png'), (DIR+r'\Stimuli\12-1.png'), LETTERSIZE[2]]}

# ================
# === MESSAGES ===
# ================

EXP_START = 666 # Message to be sent to log with the start of experiment
EXP_END = 999 # End of experiment
TRIAL_START = 777 # Start of the new trial
LEARN_END = 888999 # End of learning session
#PLAY_START = 999888 # Start of spelling session

## ===================
## === EYETRACKING ===
## ===================
#
#SMI_HOST_IP = '192.168.0.2' # IP of the machine running the experiment
#HOST_PORT = 4444
#SMI_SERVER_IP = '192.168.0.3' # IP of SMI RED 500 Eyetracker Server
#SERVER_PORT = 5555
