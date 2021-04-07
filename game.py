import arcade
from threading import Timer

SERVER_IP = '127.0.0.1'
SERVER_PORT = 65000
WINDOW_WIDTH = 1280
WINDOW_HEIGHT = 720
TITLE = 'Multiplayer game'
PLAYER_MOVE_SPEED = 5

player_list = {}
class Player():
    """ Create object for any player connected to the server """
    def __init__(self, address):
        self.address = address
        self.x = WINDOW_WIDTH / 2
        self.y = WINDOW_HEIGHT / 2
        # dictionary of client input status with will be send to the server,
        # if you wont send more data to the server you need add more element to dictionary below
        self.client_input = {
            'left': 0,
            'right': 0,
            'top': 0,
            'bottom': 0,
        }

    def server_update(self, delta_time: float = 0.016666666666666666):
        """ Game logic working on server like game physics or player move """
        Timer(delta_time, self.server_update()).start() # run again function every delta_tieme
        if self.client_input['left'] == 1:
            self.x -= PLAYER_MOVE_SPEED
        if self.client_input['right'] == 1:
            self.x += PLAYER_MOVE_SPEED
        if self.client_input['top'] == 1:
            self.y += PLAYER_MOVE_SPEED
        if self.client_input['bottom'] == 1:
            self.y -= PLAYER_MOVE_SPEED

    def draw(self):
        """ Draw player """
        arcade.draw_circle_filled(self.x, self.y, 30, arcade.csscolor.WHITE)

class Game(arcade.Window):
    """ Main game class """
    def __init__(self, width: int, height: int, title: str):
        super().__init__(width=width, height=height, title=title)
        # create player object for my
        self.my = Player('MY')

    def on_key_press(self, symbol: int, modifiers: int):
        """ If player press kay change client input status """
        if symbol == arcade.key.A:
            self.my.client_input['left'] = 1
        if symbol == arcade.key.D:
            self.my.client_input['right'] = 1
        if symbol == arcade.key.W:
            self.my.client_input['top'] = 1
        if symbol == arcade.key.S:
            self.my.client_input['bottom'] = 1

    def on_key_release(self, symbol: int, modifiers: int):
        """ If player release kay change client input status """
        if symbol == arcade.key.A:
            self.my.client_input['left'] = 0
        if symbol == arcade.key.D:
            self.my.client_input['right'] = 0
        if symbol == arcade.key.W:
            self.my.client_input['top'] = 0
        if symbol == arcade.key.S:
            self.my.client_input['bottom'] = 0

    def on_draw(self):
        """ Draw everything on client screen """
        arcade.start_render()
        # draw player for all player connected to the server
        for player in player_list:
            player.draw()

def test():
    """ Test game without client and server """
    window = Game(WINDOW_WIDTH, WINDOW_HEIGHT, TITLE)
    arcade.run()
if __name__ == '__main__':
    test()