"""
Multiplayer-Arcade is a freamwork designed to make it easier for you to write multiplayer games so that
you don't have to worry about all the difficult issues related to communication between players.
With this framework you can write your own multiplayer game almost as easily as if you were writing
a regular game in the Arcade library.

Everything you need to write your own multiplayer game is in this file.

To start the server you need run the server.py file.
(you don't need to know how it works but of course it would be better if you knew how it works)

The client.py file is used to start game and connect to the server, 
if you want run it without console, you can change extension to .pyw

    Author: Stanik
    Email: stanik@tuta.io
    GitHub: https://github.com/stanik120
    License: GPL 3
    Python Version: 3.9.1

"""
import arcade
import copy
############
# SETTINGS #
############
SERVER_IP = '127.0.0.1'
SERVER_PORT = 65000
WINDOW_WIDTH = 500
WINDOW_HEIGHT = 300
TITLE = 'Multiplayer game'
PLAYER_MOVE_SPEED = 5

# dictionary of client input status witch will be send to the server with UDP protocol,
# if you won't send more data to the server you need add more element to dictionary below
client_input = {
    'left': 0,
    'right': 0,
    'top': 0,
    'bottom': 0,
}
# dictionary of server output data that will be assigned to each player and send to all client with UDP protocol
server_output = {
    'x': 0,
    'y': 0
}
# dictionary of player stats that will be assigned to each player and send to all client with TCP protocol
# (It's not working yet)
player_stats = {
    'kill': 0,
    'death': 0
}
# list of all player connected to the server
players_list = []

class Player():
    """ Player class to create an object for each client """
    def __init__(self, address):
        # copy client input and server output to player
        self.client_input = copy.copy(client_input)
        self.server_output = copy.copy(server_output)
        self.player_stats = copy.copy(player_stats)
        self.address = address

    def draw(self):
        """ Draw player """
        arcade.draw_rectangle_filled(
            center_x = self.server_output['x'],
            center_y = self.server_output['y'],
            width = 20,
            height = 20,
            color = arcade.csscolor.WHITE
        )

class Game():
    """ Main game class """
    def __init__(self):
        """ Here you can initialize variables that will be used on the server like PhysicsEngineSimple """
        pass

    def on_key_press(self, symbol: int, modifiers: int):
        """ If client press kay change client input status """
        if symbol == arcade.key.A:
            client_input['left'] = 1
        if symbol == arcade.key.D:
            client_input['right'] = 1
        if symbol == arcade.key.W:
            client_input['top'] = 1
        if symbol == arcade.key.S:
            client_input['bottom'] = 1

    def on_key_release(self, symbol: int, modifiers: int):
        """ If client release kay change client input status """
        if symbol == arcade.key.A:
            client_input['left'] = 0
        if symbol == arcade.key.D:
            client_input['right'] = 0
        if symbol == arcade.key.W:
            client_input['top'] = 0
        if symbol == arcade.key.S:
            client_input['bottom'] = 0

    def server_update(self, delta_time):
        """ Game logic working on server like game physics or player move """
        for player in players_list:
            if player.client_input['left'] == 1:
                player.server_output['x'] -= PLAYER_MOVE_SPEED
            if player.client_input['right'] == 1:
                player.server_output['x'] += PLAYER_MOVE_SPEED
            if player.client_input['top'] == 1:
                player.server_output['y'] += PLAYER_MOVE_SPEED
            if player.client_input['bottom'] == 1:
                player.server_output['y'] -= PLAYER_MOVE_SPEED

    def on_draw(self):
        """ Draw everything on client screen """
        arcade.start_render()
        # draw all players connected to the server
        for player in players_list:
            player.draw()