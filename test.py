from game import *

class ClientGame(Game, arcade.Window):
    """ Extended game class for client """
    def __init__(self, width: int, height: int, title: str):
        arcade.Window.__init__(self, width=width, height=height, title=title)

    def on_draw(self):
        """ Draw everything on client screen """
        arcade.start_render()
        # draw player
        arcade.draw_rectangle_filled(
            center_x = server_output['x'],
            center_y = server_output['y'],
            width = 20,
            height = 20,
            color = arcade.csscolor.WHITE
        )

window = ClientGame(WINDOW_WIDTH, WINDOW_HEIGHT, TITLE)
arcade.run()
