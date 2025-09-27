import socket
import signal
import sys
import threading

def handler(signum, _):
    print(f"{signum}を受信しました。終了しました。")
    sys.exit(0)

def handle_message(file):
    try:
        while True:
            message = input('message >>>> ')
            file.write((message + '\n').encode('utf-8'))

            data = file.readline()
            print('サーバーからの応答：', data.decode('utf-8').rstrip('\n'))

            if not data:
                print('サーバーが切断しました。')
                break
    finally:
        print('ソケットを閉じます。')
        sock.close()


server_address = '/tmp/socket_file'

sock = socket.socket(socket.AF_UNIX, socket.SOCK_STREAM)

try:
    sock.connect(server_address)
except socket.error as err:
    print(err)
    sys.exit(1)


file = sock.makefile('rwb', buffering=0)

signal.signal(signal.SIGINT, handler)


thread_handle_message = threading.Thread(target=handle_message, args=(file,), daemon=True)
thread_handle_message.start()
