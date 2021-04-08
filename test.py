""" Test without server """
from game import *

class Player(Player):
    def __init__(self):
        super().__init__()
class ClientGame(Game, arcade.Window):
    """ Extended game class for test """
    def __init__(self, width: int, height: int, title: str):
        arcade.Window.__init__(self, width=width, height=height, title=title)
        # create player object for me
        self.me = Player()
        # add me to the player list
        players_list.append(self.me)

    def on_key_press(self, symbol: int, modifiers: int):
        """ If client press kay change client input status """
        if symbol == arcade.key.A:
            self.me.client_input['left'] = 1
        if symbol == arcade.key.D:
            self.me.client_input['right'] = 1
        if symbol == arcade.key.W:
            self.me.client_input['top'] = 1
        if symbol == arcade.key.S:
            self.me.client_input['bottom'] = 1

    def on_key_release(self, symbol: int, modifiers: int):
        """ If client release kay change client input status """
        if symbol == arcade.key.A:
            self.me.client_input['left'] = 0
        if symbol == arcade.key.D:
            self.me.client_input['right'] = 0
        if symbol == arcade.key.W:
            self.me.client_input['top'] = 0
        if symbol == arcade.key.S:
            self.me.client_input['bottom'] = 0

window = ClientGame(WINDOW_WIDTH, WINDOW_HEIGHT, TITLE)
arcade.run()
