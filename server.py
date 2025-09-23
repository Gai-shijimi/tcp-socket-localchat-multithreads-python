import socket
import os
import signal
import sys 

def handler(signum, _):
    print(f'{signum}を受け取りました。')
    sys.exit(0)


server_address = '/tmp/socket_file'

try:
    os.unlink(server_address)
except FileNotFoundError:
    pass


sock = socket.socket(socket.AF_UNIX, socket.SOCK_STREAM)
print('サーバーを起動しています.....{}'.format(server_address))
sock.bind(server_address)
sock.listen(1)

signal.signal(signal.SIGINT, handler)

