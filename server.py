import socket
import os
import signal
import sys 
import threading

def handler(signum, _):
    print(f'{signum}を受け取りました。')
    sys.exit(0)

def handle_client(connection, ):
    print("クライアントと接続しました。")

    file = connection.makefile('rwb', buffering=0)
    for line in file:
        msg = line.rstrip(b'\n').decode('utf-8')
        print('受信：', msg)
        response = ('サーバーからの応答：' + msg + '\n').encode('utf-8')
        file.write(response)

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

while True:
    connection, _ = sock.accept()

    thread_handle_client = threading.Thread(target=handle_client, args=(connection,), daemon=True)
    thread_handle_client.start()


