# This file is an example of how to recover EEG data from sensors

# Once you have put the info of your sensor in the resolve_stream function, it will find the stream and create an inlet to access the 
# data

# The results will be printed in the console with the corresponding timestamps

from pylsl import StreamInlet, resolve_stream #import pylsl to use LSL and recover the data from the sensors

streams = resolve_stream('type','eeg') #recover the list of LSL streams of type = eeg

inlet = StreamInlet(streams[0]) #create a inlet from the first stream of the list

while True:
    sample, timestamp = inlet.pull_sample() #recover the data sample and their timestamp from the inlet
    print(timestamp, sample) #print them out