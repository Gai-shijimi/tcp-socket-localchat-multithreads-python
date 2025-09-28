import socket
import os
import signal
import sys 
import threading



SERVER_PATH = '/tmp/socket_file'
stop_event = threading.Event()

def handler(signum, _):
    print(f'{signum}を受け取りました。')
    stop_event.set()


def handle_client(connection):
    print("クライアントと接続しました。")
    file = connection.makefile('rwb', buffering=0)
    connection.settimeout(10)
    try:
        while not stop_event.is_set():
            
            try:
                line = file.readline()
                if not line:
                    break
                msg = line.rstrip(b'\n').decode('utf-8')
                print('受信：', msg)
                response = ('サーバーからの応答：'+msg+'\n').encode('utf-8')
                file.write(response)

            except socket.timeout:
                pass

    except Exception as e:
        pass

    finally:
        try:
            file.close()
        except:
            pass
        try:
            connection.close()
        except:
            pass
        print('クライアントとの接続を切断します')


def main():

    try:
        os.unlink(SERVER_PATH)
    except FileNotFoundError:
        pass

    sock = socket.socket(socket.AF_UNIX, socket.SOCK_STREAM)
    try:
        print('サーバーを起動しています.....{}'.format(SERVER_PATH))
        sock.bind(SERVER_PATH)
        sock.listen(1)
        sock.settimeout(0.5)

        signal.signal(signal.SIGINT, handler)

        threads = []

        while not stop_event.is_set():
            try:
                connection, _ = sock.accept()
            except socket.timeout:
                continue

            t_handle_client = threading.Thread(target=handle_client, args=(connection,))
            t_handle_client.start()
            threads.append(t_handle_client)
        
        print("スレッドの終了まち…")
        for t in threads:
            t.join()
        
    finally:
        try:
            sock.close()
        finally:
            if os.path.exists(SERVER_PATH):
                os.unlink(SERVER_PATH)
        print('サーバー終了')
       

if __name__ == '__main__':
    main()


