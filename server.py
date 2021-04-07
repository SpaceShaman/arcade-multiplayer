import socket
from threading import Thread, Timer
from game import *

# time interval in which the server will send data to clients
SEND_SPEED = .1

server_socket = None

class Receiving(Thread):
    """ Recive data from clients and update client_input status """
    def __init__(self):
        super().__init__()

    def run(self):
        while True:
            data, address = server_socket.recvfrom(1024)
            data = data.decode('utf-8').split(';')
            # if player dont exist for recived data create them and add him to player_list dictionary
            if not address in player_list:
                player_list[address] = Player(address)
                # start updating player in thread
                player_list[address].server_update()
                print(f'New player connect from {address[0]}:{address[1]}')
            # update client_input status
            count = 0
            for k, v in player_list[address].client_input.items():
                player_list[address].client_input[k] = data[count]
                count += 1
            
            
def main():
    """ Main server function """
    global server_socket
    # create udp socket
    server_socket = socket.socket(type = socket.SOCK_DGRAM)
    server_socket.bind((SERVER_IP, SERVER_PORT))
    print(f'Server start on {SERVER_IP}:{SERVER_PORT}')
    # start reciving data from clients in new thread
    receiver = Receiving()
    receiver.start()

    for address, player in player_list:
        player.server_update()