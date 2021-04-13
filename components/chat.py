import arcade, arcade.gui

# how many message will be store in chat_list and show on the screen
CHAT_LIST_SIZE = 10

window = None
class ChatInputBox(arcade.gui.UIInputBox):
    """ Entry field for messages to be sent """
    def __init__(self, window):
        super().__init__()
        self.alpha = 0
        self.id = 'chat'
        window_size = window.get_size()
        self.width= window_size[0] * .99
        self.height = 25
        self.center_x= window_size[0] / 2
        self.center_y= self.height / 2 + window_size[0] * .005
        self.set_style_attrs(
            font_size = 12,
            font_color = arcade.csscolor.WHITE,
            font_color_hover = arcade.csscolor.WHITE,
            font_color_focus = arcade.csscolor.WHITE,
            bg_color = arcade.csscolor.BLACK,
            border_width = 1,
            border_color = arcade.csscolor.WHITE,
            border_color_hover = arcade.csscolor.WHITE,
            border_color_focus = arcade.csscolor.WHITE,
            bg_color_hover = arcade.csscolor.BLACK,
            bg_color_focus = arcade.csscolor.BLACK,
            margin_left = 5
        )

class UIChat(arcade.gui.UIManager):
    """ Main component for chat, all elements are kept in it, like text input field and messages """
    def __init__(self, window):
        super().__init__()
        self.window_size = window.get_size()
        # crate input field for massage to send
        self.chat_input = ChatInputBox(window)
        # add chat_input to ui_elements
        self.add_ui_element(self.chat_input)
        # list of messages to show
        self.message_list = []
        self.message_alpha = 255

    def store_message(self, message):
        """ store message in message_list """
        # if message_list is this same size like CHAT_LIST_SIZE remove from it the oldest message
        if len(self.message_list) == CHAT_LIST_SIZE:
            self.message_list.pop(0)
        # add message to list
        self.message_list.append(message)

    def send_message(self, message):
        """ Send message to the server """
        self.store_message(message)

    def on_key_release(self, symbol: int, modifiers: int):
        # if you press 'T' change visiblity chat box
        if symbol == arcade.key.T and not self.chat_input.focused:
            # make chat_input focused
            self.chat_input.text = ''
            self.focused_element = self.chat_input
        # send message if press enter and chat_input is no emty
        if self.chat_input.focused and symbol == arcade.key.ENTER:
            if self.chat_input.text != '':
                self.send_message(self.chat_input.text)
                self.chat_input.text = ''
                # unfocus chat_input
                self.focused_element = None
            # unfocus chat_input if you press ENTER end chat_input.text is empty
            elif self.chat_input.text == '':
                self.focused_element = None

    def on_update(self, dt):
        super().on_update(dt)
        # if chat_input is not focused make it invisible
        if not self.chat_input.focused:
            self.chat_input.alpha = 0
        # if chat_input is focused make it visible
        if self.chat_input.focused:
            self.chat_input.alpha = 255

    def on_draw(self):
        super().on_draw()
        # draw chat messages
        pos_y = self.window_size[1] -19
        for message in self.message_list:
            arcade.draw_text(
                text = message,
                start_x = 5,
                start_y = pos_y,
                color = arcade.csscolor.WHITE,
            )
            pos_y -= 13