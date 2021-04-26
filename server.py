"""
To start the server you need to run this file. 
"""
from game import *
import socket
from threading import Thread

BUFSIZE = 1024
ADDRESS = (SERVER_IP, SERVER_PORT)
# speed which the server sends data to the client via UDP
SENDING_SPEED = 1/15
# initialize global variables
tcp_socket = None
udp_socket = None
game = None

def remove_player(client_socket):
    """ Remove disconected player from player_list and stop socket and thread """
    client_address = client_socket.getpeername()
    for player in players_list:
        if player.address == client_address:
            players_list.remove(player)
            break
    client_socket.close()
    # send to all clients info about disconected client
    for player in players_list:
        player.client_socket.sendall(f'd;{client_address[0]};{client_address[1]}'.encode())
    print (f'{client_address[0]}:{client_address[1]} disconect.')

class ServerPlayer(Player):
    """ Extended player class for server with client_socket extra variable """
    def __init__(self, address, client_socket):
        super().__init__(address)
        # client socket for player
        self.client_socket = client_socket
        # create new thread and start reciving data from client with TCP (chat massage)
        self.tcp_reciver = TCPReciv(self.client_socket)
        self.tcp_reciver.start()

class TCPConnect(Thread):
    """ Wait for TCP connection and if client connected create new player object for connected client """
    def __init__(self):
        super().__init__()

    def run(self):
        while True:
            # wait for TCP connection
            client_socket, client_address = tcp_socket.accept()
            # print info about connected client
            print(f'{client_address[0]}:{client_address[1]} connect to the server')
            # send to all clients message with info about connected client
            for player in players_list:
                player.client_socket.sendall(f'm;{client_address[0]}:{client_address[1]} connect to the server'.encode())
            # create new player object for connected client and assign to him client address
            # and socket for recive and send data via TCP
            player = ServerPlayer(client_address, client_socket)
            players_list.append(player)

class TCPReciv(Thread):
    """ Create new thread for reciving data with TCP from client (chat massage) """
    def __init__(self, client_socket):
        super().__init__()
        self.client_socket = client_socket
        self.client_address = client_socket.getpeername()

    def run(self):
        while True:
            # recive data from client and decode them
            try:
                data = self.client_socket.recv(BUFSIZE).decode('utf-8')
                data = data.split(';', 1)
                # if recived data is chat message reived from client, resend them to all client connected to the server
                if data[0] == 'm':
                    msg = f'{self.client_address[0]}:{self.client_address[1]} {data[1]}'
                    # send to all clients recived message
                    for player in players_list:
                        player.client_socket.sendall(f'm;{msg}'.encode())
                    print(msg)
            except socket.error as e:
                # if the client disconnects from the server stop thread and delete player object 
                break
        remove_player(self.client_socket)

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
                        player.client_input[key] = int(data[count])
                        count += 1
                    print(f'{player.address[0]}:{player.address[1]} {player.client_input} {player.server_output}')
                    break

def UDPSend(delata_time):
    """ Send to all client connected to the server server_output for every each player """
    # turn server_output for every each player to string and encode it
    data = ''
    for player in players_list:
        # clear client_input
        for key in player.client_input.keys():
            player.client_input[key] = 0
        # add client address for this player to data
        data += player.address[0] + ';' + str(player.address[1]) + ';'
        # add all server_output value for this player to data
        for value in player.server_output.values():
            data += str(value) + ';'
        # add extra ; to separate individual players
        data += ';'
    # encode data
    data = data[:-2].encode()
    # send data to all client connected to the server
    for player in players_list:
        udp_socket.sendto(data, player.address)

def main():
    """ Main server function """
    global tcp_socket
    global udp_socket
    global game
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
    # create new thread for reciving data with UDP protocol from client
    udp_reciver = UDPRecive()
    # start reciving data with UDP protocol
    udp_reciver.start()
    # create new thread to wait for TCP connection
    tcp_connector = TCPConnect()
    # start waiting for connection
    tcp_connector.start()
    # run server_update method in loop for game phisics, player movment logic and etc.
    arcade.schedule(game.server_update, 1/60)
    # run UDPSend every given time to send server_output values to all client
    arcade.schedule(UDPSend, SENDING_SPEED)
    # run arcade game loop
    arcade.run()

if __name__ == '__main__':
    main()