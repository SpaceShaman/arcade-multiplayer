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

class TCPReciv(Thread):
    """ Create new thread for reciving data with TCP from client (chat massage) """
    def __init__(self):
        super().__init__()

    def run(self):
        while True:
            # recive data from client and decode them
            data = tcp_socket.recv(BUFSIZE).decode('utf-8')

def UDPSend():
    # if any value in client_input is equals 1 send client_input to the server
    if 1 in client_input.values():
        # turn client_input into string and encode it
        data = ''
        for values in client_input.values():
            data += str(values) + ';'
        data = data[:-1].encode()
        # send encode data to the server with UDP
        udp_socket.sendto(data, ADDRESS)
class UDPRecive(Thread):
    """ Create new thread for reciving data with UDP from client (client_input with information witch button client press etc.) """
    def __init__(self):
        super().__init__()

    def run(self):
        while True:
            # recive data from client and decode them
            data, address = udp_socket.recvfrom(BUFSIZE)
            data = data.decode('utf-8')
            data = data.split(';')
            # put recived data to client_input dictionary in Player object
            for player in players_list:
                if player.address == address:
                    count = 0
                    for key in player.client_input.keys():
                        player.client_input[key] = data[count]
                        count += 1
                # print recived data
                print(f'{player.address[0]}:{player.address[1]} {player.client_input}')
                break

def UDPSend():
    pass

def main():
    """ Main client function """
    global tcp_socket
    global udp_socket
    # create TCP socket
    tcp_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    # bind address to tcp_socket
    tcp_socket.bind(ADDRESS)
    # create UDP socket
    tcp_socket.listen()
    udp_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    # bind address to  udp_socket
    udp_socket.bind(ADDRESS)
    # create arcade game object
    game = Game()
    # run server_update method in loop for game phisics, player movment logic and etc.
    arcade.schedule(game.server_update, 1/60)
    # create new thread for reciving data with UDP protocol from client
    udp_reciver = UDPRecive()
    # start reciving data with UDP protocol
    udp_reciver.start()
    # run UDPSend every given time
    udp_sender = arcade.schedule(UDPSend, SENDING_SPEED)
    
    while True:
        # wait for TCP connection
        client_socket, client_address = tcp_socket.accept()
        # print info about connected client
        print(f'{client_address[0]}:{client_address[1]} connect to the server')
        # create new player object for connected client and assign to him client address
        player = Player(client_address)
        players_list.append(player)

if __name__ == '__main__':
    main()