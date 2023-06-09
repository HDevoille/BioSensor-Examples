# This file is an example of integrating different scripts into a single application


from pylsl import StreamInlet, resolve_stream #import pylsl to use LSL and recover the data from the sensors


def simple_datastream():
    streams = resolve_stream('name','OpenSignals') #recover the list of LSL streams of type = emg

    inlet = StreamInlet(streams[0]) #create a inlet from the first stream of the list

    while True:
        sample, timestamp = inlet.pull_sample() #recover the data sample and their timestamp from the inlet
        print(timestamp, sample) #print them out 

def simple_data_visualisation(): #If you want to do it the hard way rather than using another software (NOT WORKING)
    import matplotlib.pyplot as plt
    from matplotlib.animation import FuncAnimation
    import threading
    import time

    streams = resolve_stream('name','OpenSignals') #recover the list of LSL streams of type = emg

    inlet = StreamInlet(streams[0]) #create a inlet from the first stream of the list
    
    sensor_values = []  # Global list to store sensor values
    lock = threading.Lock()  # Lock to synchronize access to the sensor_values list

    def get_sensor_value():
        sample, timestamp = inlet.pull_sample()
        return sample

    def collect_sensor_values():
        while True:
            # Simulate collecting sensor values
            # Replace this with your actual method to collect sensor values
            new_value = get_sensor_value()
        
            with lock:
                sensor_values.append(new_value)

            time.sleep(0.1)  # Adjust the sleep duration based on your data collection rate

    def live_plot_sensor_values():
        fig, ax = plt.subplots()
        x_data, y_data = [], []
        line, = ax.plot([], [], 'b-')

        def update_plot(frame):
            with lock:
                current_values = sensor_values[:]

            if current_values:
                y_data.append(frame)
                x_data.append(current_values[-1])

            # Trim the data if necessary to keep the same length for x_data and y_data
            max_length = 1  # Maximum length of the data
            if len(y_data) > max_length:
                x_data.pop(0)
                y_data.pop(0)
            line.set_data(x_data, y_data)
            ax.relim()
            ax.set_xlim(0,100)
            ax.set_ylim(0,100)
            return line,

        ani = FuncAnimation(fig, update_plot, frames=range(100), interval=100, blit=True)

        plt.show()

    # Start the data collection thread
    data_collection_thread = threading.Thread(target=collect_sensor_values)
    data_collection_thread.daemon = True  # Set the thread as daemon so that it exits when the main program exits
    data_collection_thread.start()

    live_plot_sensor_values()

def recording_data():
    import os #import os to write data in csv 
    import pandas as pd #import pandas to use the Dataframe struct to write in csv file (other option are possible)

    streams = resolve_stream('type','emg') #recover the list of LSL streams of type = emg

    inlet = StreamInlet(streams[0]) #create a inlet from the first stream of the list

    output_path='EEG_code/data.csv' #path to filename
    df = pd.DataFrame(columns=['val'])

    while True:
        sample, timestamp = inlet.pull_sample() #recover the data sample and their timestamp from the inlet
        df.append({'val':sample},ignore_index=True) #add the samples to the dataframe
        df.to_csv(output_path, mode='a', header=not os.path.exists(output_path)) #write the dataframe to the csv file

def send_data(threshold):
    import socket #import socket to communicate through wifi with other device

    streams = resolve_stream('type','emg') #recover the list of LSL streams of type = emg

    inlet = StreamInlet(streams[0]) #create a inlet from the first stream of the list

    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM) #create a socket that listen to TCP connection using IPv4 communication protocol
        
    server_socket.bind(('localhost', 12345)) #Give the socket a host and an address
        
    server_socket.listen(1) #Listen to entry connection

    while True:
        client_socket, addr = server_socket.accept() #Accept any entry connection

        while True:
            try:
                sample, timestamp = inlet.pull_sample()
                if sample > threshold:
                    client_socket.send(bytes(sample, "utf-8")) #Send the message as a string to the client
            except:
                break  #Exit the loop if the client disconnect

            client_socket.close() #Close the client socket
    

if __name__ == "__main__":
    print("Choose a task :\n"+
          "1) DataStream\n"+
          "2) DataVisualisation (NOT WORKING)\n"+
          "3) DataRecording\n"+
          "4) Send Data based on threshold\n")
    choice = input("Your choice : ")
    if int(choice) == 1:
        simple_datastream()
    if int(choice) == 2:
        simple_data_visualisation()
    if int(choice) == 3:
        recording_data()
    if int(choice) == 4:
        threshold = input("Type your threshold : ")
        send_data(threshold)

