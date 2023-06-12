# This is an example of a script to measure the heart rate of an user

# Once you have put the info of your sensor in the resolve_stream function, it will find the stream and create an inlet to access the 
# data

from pylsl import StreamInlet,resolve_stream #import pylsl to use LSL and recover the data from the sensors
import numpy as np #import numpy to create the peak filter
import matplotlib.pyplot as plt #import matplotlib to plot the graph


streams = resolve_stream('name','OpenSignals') #recover the list of LSL stream of type 'ecg'

inlet = StreamInlet(streams[0]) #create an inlet from the first stream of the list

v = np.linspace(0.5 * np.pi, 1.5 * np.pi, 15) #create a linear vector between pi/2 and 3pi/2
peak_filter = np.sin(v) #create a sin wave on the linear space

n=0
calibration_data = [] #create an empty list to recover the data
calibration_time = [] #create an empty list to recover the timestamp

print("start")
while n < 1000: #collect 1000 datapoint
    sample, timestamp = inlet.pull_sample() #recover the data and their timestamp
    calibration_data.append(sample[1]) #add the sample to the data
    calibration_time.append(timestamp) #add the timestamp to the time data
    n+=1
print("end")

ecg_transform = np.correlate(calibration_data,peak_filter,mode='same') #correlate the peak filter with the signal to highlight the peak
print("length: ",len(ecg_transform))

peak = float(abs(max(ecg_transform))) * 0.95 #create the threshold for the max peak
print("max: ",peak)
time = calibration_time[-1] - calibration_time[0] #compute the total time of the data
peak_count = 0 #create a counter for the peak in the data

for i in ecg_transform: #look at the number of peak in the data
    if i > peak:
        print(i)
        peak_count+=1

heart_rate = (peak_count/time)*60 #to compute the heart rate divide the number of peak by the time and multiply it by 60 to have the bpm

print("number of peak: ",peak_count)
print("time: ",time)
print("heart rate: ",heart_rate)

plt.plot(ecg_transform)
plt.show()
