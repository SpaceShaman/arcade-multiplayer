from threading import Timer


def server_update():
    """ Game logic working on server like game physics or player move """
    Timer(1, server_update).start()
    print('aa')

server_update()