"""
You cen test your game without starting server using this file. 
"""
from game import *
from components.chat import *

window = None
view = None
class TestGame(Game, arcade.View):
    """ Extended game class for test """
    def __init__(self):
        Game.__init__(self)
        arcade.View.__init__(self)
        # create player object for me
        self.me = Player('test')
        # add me to the player list
        players_list.append(self.me)
        # create chat module from components/chat.py
        self.ui_chat = UIChat(window)

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

    def on_update(self, delta_time: float):
        self.server_update(delta_time)

def main():
    global window
    global view
    # create arcade window
    window = arcade.Window(WINDOW_WIDTH, WINDOW_HEIGHT, TITLE)
    view = TestGame()
    window.show_view(view)
    # run the arcade loop of the game
    arcade.run()

if __name__ == '__main__':
    main()