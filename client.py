from game import *
import socket

client_socket = None
ADDRESS = (SERVER_IP, SERVER_PORT)
class ClientGame(Game, arcade.Window):
    """ Extended game class for client """
    def __init__(self, width: int, height: int, title: str):
        arcade.Window.__init__(self, width=width, height=height, title=title)

    def update(self, delta_time: float):
        """ Send information about pressed button to the server and update players data recived from server """
        # if input is pressed convert inputs to string and send them to the server
        data = ''
        for input, value in client_input:
            if value == 1:
                for input, value in client_input:
                    data += f'{value};'
                data = data[:-1]
                client_socket.sendto(data, ADDRESS)
                break

def main():
    """ Main function """
    global client_socket
    # create udp socket
    client_socket = socket.socket(type = socket.SOCK_DGRAM)

    # start game
    window = ClientGame(WINDOW_WIDTH, WINDOW_HEIGHT, TITLE)
    arcade.run()

if __name__ == '__main__':
    main()