# This file is an example of how to send EMG data from sensors to another device using sockets (local network)

# Once you have put the info of your sensor in the resolve_stream function, it will find the stream and create an inlet to access the 
# data

# The results will sent to a client using TCP connection with IPv4 communication protocol

# This is really useful when you want to access the data on a device that can't use LSL but can connect to the local network (an ESP-32 for example)
# It can also be used to send data to other app with the same problem (such as Unity for example)

# I'm using a similar script for the 2D-EMG game (everything is on my GitHub in the 2D-EMG game repo)

# BE AWARE that you will have to create another script on the client side to connect and access the data (it can be in another language such as C#, C, C++ ...)
# There is an example for C# Unity script in the 2D-EMG game

from pylsl import StreamInlet, resolve_stream #import pylsl to use LSL and recover the data from the sensors
import socket #import socket to communicate through wifi with other device

streams = resolve_stream('type','emg') #recover the list of LSL streams of type = emg

inlet = StreamInlet(streams[0]) #create a inlet from the first stream of the list

server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM) #create a socket that listen to TCP connection using IPv4 communication protocol
        
server_socket.bind(('localhost', 12345)) #Give the socket a host and an address
        
server_socket.listen(1) #Listen to entry connection

threshold = 0.6 #Change this to the threshold value you want

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