from game import *
import socket

server_socket = None
ADDRESS = (SERVER_IP, SERVER_PORT)

def main():
    """ Main server function """
    # create UDP socket
    server_socket = socket.socket(type = socket.SOCK_DGRAM)
    server_socket.bind(ADDRESS)
    print('Server start')
    while True:
        data, address = server_socket.recvfrom(1024)
        print(f'{address[0]}:{address[1]} {data}')

if __name__ == '__main__':
    main()