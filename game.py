import arcade
from threading import Timer

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

