"""
This is a basic example of how to print the data of an LSL stream in your console.
You can use several option to id your stream such as the name, the type or the hostname.
This script can be used with all kind of sensors. It's the most basic script you will need to start working with sensors and LSL.
You should always print the data you receive when you start working with the sensors to have a better understanding of the type of data.
"""

from pylsl import StreamInlet, resolve_stream #import StreamInlet and resolve_stream from pylsl to recover the data

streams = resolve_stream('name','StreamName') #find the list of streams with this informations

inlet = StreamInlet(streams[0]) #create an inlet from the first stream of the list

while True:
    sample, timestamp = inlet.pull_sample() #recover the sample and the corresponding timestamp from the inlet
    print(timestamp,sample) #print them out
