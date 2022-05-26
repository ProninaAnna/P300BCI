from visual import Visual
from CONSTANTS import *
from pylsl import StreamInlet, resolve_byprop
from multiprocessing import Process

a = Visual()

def readstream():

    streams = resolve_byprop('name', PHOTOSENSOR_STREAM)
    inlet = StreamInlet(streams[0])
    for i in range(0, 20):
            # Request data and timestamp from the photocell stream
            sample, timestamp = inlet.pull_sample()
            print('photo ', timestamp, sample)


if __name__ == '__main__':
    p1 = Process(target=readstream)
    p1.start()
    p2 = Process(target=a.visual_process())
    p2.start()
    p1.join()
    p2.join()