"""
This is a basic example of how to record data in an csv file from a LSL stream.
You can use several option to id your stream such as the name, the type or the hostname.
This script can be used with all kind of sensors. Althought, you might want to modify the way data will be written in the csv file.
To do that, you can look up how to use pandas DataFrame to write the data your way in the csv file.
Being able to record data is very important for a large number of applications. Make sure that you store your file in the right place.
"""

from pylsl import StreamInlet, resolve_stream #import StreamInlet and resolve_stream from pylsl to recover the data

import os #import os to modify files and navigate in the system
import pandas as pd #import pandas to use the Dataframe struct to write in csv file (other option are possible)

streams = resolve_stream('name','StreamName') #find the list of streams with this informations

inlet = StreamInlet(streams[0]) #create an inlet from the first stream of the list

output_path='EMG_code/data.csv' #path to filename
df = pd.DataFrame(columns=['val']) #you can modify this to reorganize the data

while True:
    sample,timestamp = inlet.pull_sample() #recover the data sample and their timestamp from the inlet
    df.append({'val':sample},ignore_index=True) #add the samples to the dataframe
    df.to_csv(output_path, mode='a', header=not os.path.exists(output_path)) #write the dataframe to the csv file
