from game import *
import socket
from threading import Thread, Timer

BUFSIZE = 1024
# speed which the client sends data to the server using UDP
SENDING_SPEED = .1
ADDRESS = (SERVER_IP, SERVER_PORT)
# initialize global variables
tcp_socket = None
udp_socket = None

class RepeatTimer(Timer):
    """ Run the given function every given time """
    def run(self):
        while not self.finished.wait(self.interval):
            self.function(*self.args, **self.kwargs)

class TCPReciv(Thread):
    """ Create new thread for reciving data with TCP from server (player_stats and chat massage) """
    def __init__(self):
        super().__init__()

    def run(self):
        while True:
            # recive data from server and decode them
            data = tcp_socket.recv(BUFSIZE).decode('utf-8')

class UDPRecive(Thread):
    """ Create new thread for reciving data with UDP from server (server_output with player position and etc.) """
    def __init__(self):
        super().__init__()

    def run(self):
        while True:
            # recive data from server and decode them
            data, address = udp_socket.recvfrom(BUFSIZE)
            data = data.decode('utf-8')

def UDPSend():
    # if any value in client_input equals 1 send client_input to the server
    if 1 in client_input.values():
        # turn client_input into string and encode it
        data = ''
        for values in client_input.values():
            data += str(values) + ';'
        data = data[:-1].encode()
        # send encode data to the server with UDP
        udp_socket.sendto(data, ADDRESS)

def main():
    """ Main client function """
    global tcp_socket
    global udp_socket
    # create TCP socket
    tcp_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    # connect to the server
    tcp_socket.connect(ADDRESS)
    # create new thread for reciving data with TCP protocol from server
    tcp_reciver = TCPReciv()
    # start reciving data with TCP protocol
    tcp_reciver.start()
    # create UDP socket
    udp_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    # assign your address from tcp_socket to udp_socket
    udp_socket.bind(tcp_socket.getsockname())
    # create new thread for reciving data with UDP protocol from server
    udp_reciver = UDPRecive()
    # start reciving data with UDP protocol
    udp_reciver.start()
    # create new thread for sending data with UDP protocol to server every given time
    udp_sender = RepeatTimer(SENDING_SPEED, UDPSend)
    # start sending data with UDP protocol
    udp_sender.start()