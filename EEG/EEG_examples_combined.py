from pylsl import StreamInlet, resolve_stream #import pylsl to use LSL and recover the data from the sensors

def simple_data_stream():
    streams = resolve_stream('type','eeg') #recover the list of LSL streams of type = eeg

    inlet = StreamInlet(streams[0]) #create a inlet from the first stream of the list

    while True:
        sample, timestamp = inlet.pull_sample() #recover the data sample and their timestamp from the inlet
        print(timestamp, sample) #print them out

def recording_data(pathname):
    import os #import os to write data in csv 
    import pandas as pd #import pandas to use the Dataframe struct to write in csv file (other option are possible)

    streams = resolve_stream('type','eeg') #recover the list of LSL streams of type = eeg

    inlet = StreamInlet(streams[0]) #create a inlet from the first stream of the list

    output_path = pathname #path to filename
    df = pd.DataFrame(columns=['val'])

    while True:
        sample, timestamp = inlet.pull_sample() #recover the data sample and their timestamp from the inlet
        df.append({'val':sample},ignore_index=True) #add the samples to the dataframe
        df.to_csv(output_path, mode='a', header=not os.path.exists(output_path)) #write the dataframe to the csv file

def data_processing(lower_freq,upper_freq):
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

    data = []
    n = 0

    while n < 1000: #take 1000 points of data to create a sample
        sample,timestamp = inlet.pull_sample()
        data.append(sample)
        n+=1
    
    filtered_data = butter_bandpass_filter(data,lowcut=lower_freq,highcut=upper_freq,fs=256) #apply a bandpass filter on the data
    for i in filtered_data:
        print(i)

if __name__ == "__main__":
    print("Choose a task : \n"+
          "1) DataStream \n"+
          "2) Record Data \n"+
          "3) Data processing (bandpass filter) \n")
    choice = input("Your choice : ")
    if choice == 1:
        simple_data_stream()
    if choice == 2:
        pathname = input("Your pathname : ")
        recording_data(pathname)
    if choice == 3:
        lower_freq = input("Low Frequency : ")
        upper_freq = input("High Frequency : ")
        data_processing(lower_freq,upper_freq)
    