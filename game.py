import arcade
############
# SETTINGS #
############
SERVER_IP = '127.0.0.1'
SERVER_PORT = 65000
WINDOW_WIDTH = 1280
WINDOW_HEIGHT = 720
TITLE = 'Multiplayer game'
PLAYER_MOVE_SPEED = 5

# dictionary of client input status with will be send to the server by UDP,
# if you wont send more data to the server you need add more element to dictionary below
client_input = {
    'left': 0,
    'right': 0,
    'top': 0,
    'bottom': 0,
}
# dictionary of server output data that will be assigned to each player and send to all client by UDP
server_output = {
    'x': 0,
    'y': 0
}
# dictionary of player stats that will be assigned to each player and send to all client by TCP
player_stats = {
    'kill': 0,
    'death': 0
}
# list of all player connected to the server
players_list = []

class Player():
    """ Player class to create an object for each client """
    def __init__(self):
        # assign client input and server output to player
        self.client_input = client_input
        self.server_output = server_output
        self.player_stats = player_stats
        self.address = None

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

    def update(self, delta_time: float):
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