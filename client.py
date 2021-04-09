from game import *
import socket
from threading import Thread

BUFSIZE = 1024
# speed which the client sends data to the server using UDP
SENDING_SPEED = 1/60
ADDRESS = (SERVER_IP, SERVER_PORT)
# initialize global variables
tcp_socket = None
udp_socket = None

class ClientGame(Game, arcade.Window):
    """ Extended game class for client to open window """
    def __init__(self, width: int = WINDOW_WIDTH, height: int = WINDOW_HEIGHT, title: str = TITLE):
        arcade.Window.__init__(self, width=width, height=height, title=title)
        Game.__init__(self)

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

def UDPSend(delta_time):
    # if any value in client_input is equals 1 send client_input to the server
    if 1 in client_input.values():
        # turn client_input into string and encode it
        data = ''
        for values in client_input.values():
            data += str(values) + ';'
        data = data[:-1].encode()
        # send encode data to the server with UDP
        udp_socket.sendto(data, ADDRESS)
        print(f'{data}')

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
    # bind your address from tcp_socket to udp_socket
    udp_socket.bind(tcp_socket.getsockname())
    # create new thread for reciving data with UDP protocol from server
    udp_reciver = UDPRecive()
    # start reciving data with UDP protocol
    udp_reciver.start()
    # run UDPSend every given time
    udp_sender = arcade.schedule(UDPSend, SENDING_SPEED)
    # create arcade window
    window = ClientGame()
    # run the arcade loop of the game
    arcade.run()

if __name__ == '__main__':
    main()