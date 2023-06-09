# This file is an example of how to process EEG data from sensors

# Once you have put the info of your sensor in the resolve_stream function, it will find the stream and create an inlet to access the 
# data

# This script allow to apply a band filter on the data, you must choose the lower and upper bound of the bandpass filter

# The results will be printed in the console

from pylsl import StreamInlet, resolve_stream #import pylsl to use LSL and recover the data from the sensors
from scipy.signal import butter, sosfilt, sosfreqz #import scipy for bandpass filtering 

def butter_bandpass(lowcut, highcut, fs, order=5):
    nyq = 0.5 * fs #define the Nyquist Frequency
    low = lowcut / nyq
    high = highcut / nyq
    sos = butter(order, [low, high], analog=False, btype='band', output='sos') 
    return sos

def butter_bandpass_filter(data, lowcut, highcut, fs, order=5):
    sos = butter_bandpass(lowcut, highcut, fs, order=order) #create the filter
    y = sosfilt(sos, data) #apply the filter on the data
    return y
    
streams = resolve_stream('type','eeg') #recover the list of LSL streams of type = eeg

inlet = StreamInlet(streams[0]) #create a inlet from the first stream of the list

lower_freq = 1 #lower bound of the bandpass filter (you can change it)
upper_freq = 45 #upper bound of the bandpass filer (you can change it too)

data = [] #create an empty list for the new data sample
n = 0 

while n < 1000: #take 1000 points of data to create a sample
    sample,timestamp = inlet.pull_sample()
    data.append(sample)
    n+=1
    
filtered_data = butter_bandpass_filter(data,lowcut=lower_freq,highcut=upper_freq,fs=256) #apply a bandpass filter on the data
for i in filtered_data:
    print(i)