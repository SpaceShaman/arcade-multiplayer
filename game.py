import arcade
###########
# SETTING #
###########
SERVER_IP = '127.0.0.1'
SERVER_PORT = 65000
WINDOW_WIDTH = 1280
WINDOW_HEIGHT = 720
TITLE = 'Multiplayer game'
PLAYER_MOVE_SPEED = 5

# dictionary of client input status with will be send to the server,
# if you wont send more data to the server you need add more element to dictionary below
client_input = {
    'left': 0,
    'right': 0,
    'top': 0,
    'bottom': 0,
}
# dictionary of server output data that will be assigned to each player and send to all client
server_output = {
    'x': 0,
    'y': 0
}
# player list in dictionary
# key = client address
# value = for the server it will be client_input data, for the client it will be server_output data
player_list = {}

class Game():
    """ Main game class """

    def on_key_press(self, symbol: int, modifiers: int):
        """ If player press kay change client input status """
        if symbol == arcade.key.A:
            client_input['left'] = 1
        if symbol == arcade.key.D:
            client_input['right'] = 1
        if symbol == arcade.key.W:
            client_input['top'] = 1
        if symbol == arcade.key.S:
            client_input['bottom'] = 1

    def on_key_release(self, symbol: int, modifiers: int):
        """ If player release kay change client input status """
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
        if client_input['left'] == 1:
            server_output['x'] -= PLAYER_MOVE_SPEED
        if client_input['right'] == 1:
            server_output['x'] += PLAYER_MOVE_SPEED
        if client_input['top'] == 1:
            server_output['y'] += PLAYER_MOVE_SPEED
        if client_input['bottom'] == 1:
            server_output['y'] -= PLAYER_MOVE_SPEED

    def on_draw(self):
        """ Draw everything on client screen """
        arcade.start_render()
        # draw all players
        for _address, _server_output in player_list:
            arcade.draw_rectangle_filled(
                center_x = _server_output['x'],
                center_y = _server_output['y'],
                width = 20,
                height = 20,
                color = arcade.csscolor.WHITE
            )