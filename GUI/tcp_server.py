from socket import *
from numpy import random
import struct
import time
from threading import Thread
import glob
from get_data_from_distance_sensor import GetDataFromDistanceSensor

global get_data
get_data = GetDataFromDistanceSensor()
get_data.start()

class TCP_server(Thread):
    """
    Creating a tcp socket server on Raspberry PI to send data to a GUI client
    """

    def __init__(self):
        """
        Initializing and opening the connection on ip address '' and on port 50007.
        """
        Thread.__init__(self)
        HOST = ''
        PORT = 50007
        # setting the BUFFER size to 1024, the maximum size of data what the server can receive
        # form the client, and what it can send
        self.BUFFER = 1024
        address = (HOST, PORT)
        # creating the socket
        self.server_socket = socket(AF_INET, SOCK_STREAM)
        self.server_socket.bind(address)
        self.server_socket.listen(1)

        print('Waiting to receive connection request...')

    def run(self):
        """
        This will be exeduted, when the thread will be started
        """
        global get_data
        # accepts a request, from the client
        conn, addr = self.server_socket.accept()
        # and waits to receive messege from it
        print('Waiting to receive messages...')
        while True:
            # receives a request from client which is a get or an exit command
            data = conn.recv(self.BUFFER).decode('utf-8')
            print('Received message: ' + data)
            if data == 'exit':
                # on exit the server stopt working
                break
            if data == 'get':
                # on get the server will send data received from distance sensors, and the actual image of the camera
                for i in range(6):
                    # sends the data from sensors
                    num = get_data.get_data_about_a_sensor(i)
                    conn.send(bytearray(struct.pack('d', num)))
                # choosing the newest image
                print(sorted(glob.glob('/etc/img/*.png')))
                name = sorted(glob.glob('/etc/img/*.png'))[-1]
                # printing it's name
                print(name)
                # opening the image
                with open(name, 'rb') as imageFile:
                    # reading the data from it
                    f = imageFile.read()
                    # converting data into bytearray
                    b = bytearray(f)
                    # it can send the data in 1024 byte blocks
                    # so length is the number of blocks, which it can send the data and +1 if it can't be divided by 1024
                    length = int(len(b) / self.BUFFER)
                    # sending the blocks
                    for i in range(length):
                        conn.send(b[i * self.BUFFER : (i + 1) * self.BUFFER])
                    if len(b) > length * self.BUFFER:
                        conn.send(b[length * self.BUFFER:])
                    # waiting 0.5 seconds before sending end, which marks the end of the file data
                    # else sometimes 'end' command will be attached to the last block of data 
                    time.sleep(.5)
                    conn.send(b'end')
        # closing the socket connection
        self.server_socket.close()

if __name__ == "__main__":
    th = TCP_server()
    th.start()
    get_data.join()
    th.join()
