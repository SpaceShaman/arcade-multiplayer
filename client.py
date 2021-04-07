from game import *

class ClientGame(Game, arcade.Window):
    """ Extended game class for client """
    def __init__(self, width: int, height: int, title: str):
        arcade.Window.__init__(self, width=width, height=height, title=title)



window = ClientGame(WINDOW_WIDTH, WINDOW_HEIGHT, TITLE)
arcade.run()
