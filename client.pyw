"""
This file is used to start game and connect to the server, 
if you want to run it without console, you can change extension to .pyw
"""

from game import *
from components.chat import *
import socket
from threading import Thread
import sys
import time

BUFSIZE = 1024
# speed which the client sends data to the server via UDP
SENDING_SPEED = 1/60
ADDRESS = (SERVER_IP, SERVER_PORT)
# initialize global variables
tcp_socket = None
udp_socket = None
window = None
game = None
# stop threads if change the variable to false 
work = True

def extrapolation(x0, t0, x1, t1):
    d_time = (t1 - t0)
    velocity = (x1 - x0) / d_time
    
    # predicted_position = velocity * d_time + x1
    now = game.time
    x = velocity * (now - t1) + x0

    return x

class Chat(UIChat):
    """ Extend UIChat class for client to send message to the server """
    def __init__(self, window):
        super().__init__(window)

    def send_message(self, message):
        # send message to the server
        tcp_socket.sendall(f'm;{message}'.encode())

class ClientGame(Game, arcade.View):
    """ Extended game class for client to open window """
    def __init__(self):
        arcade.View.__init__(self)
        Game.__init__(self)
        # create chat module from components/chat.py
        self.chat = Chat(window)
        self.time = None

    def update(self, delta_time):
        # Game.update()
        # update time
        self.time = time.time()

        # extrapolat and interpolat data recived from server to reduce letency
        for player in players_list:
            if len(player.server_output_buffer) == 2:
                p0 = player.server_output_buffer[0]
                server_output0 = p0[0]
                x0 = server_output0['x']
                y0 = server_output0['y']
                t0 = p0[1]
                p1 = player.server_output_buffer[1]
                server_output1 = p1[0]
                x1 = server_output1['x']
                y1 = server_output1['y']
                t1 = p1[1]

                x = extrapolation(x0, t0, x1, t1)
                y = extrapolation(y0, t0, y1, t1)

                player.interpolate_output['x'] = x
                player.interpolate_output['y'] = y

def remove_player(address):
    """ Remove a player with the given address from player_list """
    for player in players_list:
        if player.address == address:
            players_list.remove(player)
            break

class TCPReciv(Thread):
    """ Create new thread for reciving data with TCP from server (player_stats and chat massage) """
    def __init__(self):
        super().__init__()
        self.work = True

    def run(self):
        while self.work:
            # recive data from server and decode them
            try:
                data = tcp_socket.recv(BUFSIZE).decode('utf-8')
                data = data.split(';')
                # if recived data is information about disconected player remove this player from player list
                if data[0] == 'd':
                    address = (data[1], int(data[2]))
                    remove_player(address)
                    game.chat.store_message(f'{data[1]}:{data[2]} disconect.')
                # if recived data is chat message reived from server store them and print on the screen
                elif data[0] == 'm':
                    game.chat.store_message(';'.join(data[1:]))
            except socket.error:
                break

class UDPRecive(Thread):
    """ Create new thread for reciving data with UDP from server (server_output with player position and etc.) """
    def __init__(self):
        super().__init__()
        self.work = True

    def update_player(self, player, data):
        """ Update player server_output data """
        count = 2
        for key in player.server_output.keys():
            player.server_output[key] = int(data[count])
            count += 1

        # update the buffer of the last two server_output data, it will be used to reduce latency
        if len(player.server_output_buffer) == 2:
            player.server_output_buffer.pop(0)
        if not game == None:
            player.server_output_buffer.append((copy.copy(player.server_output), game.time))

    def create_player(self, data):
        """ Create new player object if not exist """
        # get player address from recived data
        player_address = (data[0], int(data[1]))
        # crate new player object
        player = Player(player_address)
        # add player to player_list
        players_list.append(player)
        # update player data
        self.update_player(player, data)

    def run(self):
        while self.work:
            # recive data from server and decode them
            try:
                data, address = udp_socket.recvfrom(BUFSIZE)
            except socket.error:
                break
            data = data.decode('utf-8')

            # separate the players
            players = data.split(';;')
            for player_data in players:
                # separate player date
                player_data = player_data.split(';')
                # get player address from recived data
                player_address = (player_data[0], int(player_data[1]))
                # if player exist in player_list uptade server_output, if no create new player object
                player_exist = False
                for _player in players_list:
                    if _player.address == player_address:
                        player_exist = True
                        # update player object
                        self.update_player(_player, player_data)
                        break
                if player_exist == False:
                    # crate new player object
                    self.create_player(player_data)

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

def main():
    """ Main client function """
    global tcp_socket
    global udp_socket
    global window
    global game
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
    arcade.schedule(UDPSend, SENDING_SPEED)
    # create arcade window
    window = arcade.Window(WINDOW_WIDTH, WINDOW_HEIGHT, TITLE)
    game = ClientGame()
    window.show_view(game)
    # run the arcade loop of the game
    arcade.run()
    # close program if arcade stops working
    arcade.unschedule(UDPSend)
    tcp_reciver.work = False
    udp_reciver.work = False
    tcp_socket.close()
    udp_socket.close()
    tcp_reciver.join()
    udp_reciver.join()
    print(f'tcp_reciver: {tcp_reciver.is_alive()}')
    print(f'udp_reciver: {udp_reciver.is_alive()}')
    sys.exit()

if __name__ == '__main__':
    main()