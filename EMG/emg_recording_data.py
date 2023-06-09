# This file is an example of how to record EMG data from sensors and write it in a CSV file

# Once you have put the info of your sensor in the resolve_stream function, it will find the stream and create an inlet to access the 
# data

# You can write the filename you want to create and the filepath where it should be created such as:
# 'filepath/filename.csv' (example : 'EMG_data/my_new_EMG_data.csv')

# The results will be written in the CSV file with the filename at the filepath location
# You can add additional informations in the CSV such as the timestamps for example. 
# To do that, add the desired info in the pandas dataframe before the Dataframe.to_csv() function

# This example uses pandas to write the data in an CSV files. Other options exists but pandas is easy and very efficient.

from pylsl import StreamInlet, resolve_stream #import pylsl to use LSL and recover the data from the sensors

import os #import os to modify files and navigate in the system
import pandas as pd #import pandas to use the Dataframe struct to write in csv file (other option are possible)

streams = resolve_stream('type','emg') #recover the list of LSL streams of type = emg

inlet = StreamInlet(streams[0]) #create a inlet from the first stream of the list

output_path='EEG_code/data.csv' #path to filename
df = pd.DataFrame(columns=['val'])

while True:
    sample, timestamp = inlet.pull_sample() #recover the data sample and their timestamp from the inlet
    df.append({'val':sample},ignore_index=True) #add the samples to the dataframe
    df.to_csv(output_path, mode='a', header=not os.path.exists(output_path)) #write the dataframe to the csv file