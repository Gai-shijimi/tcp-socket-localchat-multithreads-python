import socket
import signal
import sys
import threading

SERVER_PATH = '/tmp/socket_file'
stop_event = threading.Event()


def handler(signum, _):
    print(f"{signum}を受信しました。終了します。")
    stop_event.set()

def sender(file):
    try:
        while not stop_event.is_set():
            try:
                msg = input('message >>>>')
            except EOFError:
                stop_event.set()
                break
            file.write((msg + '\n').encode('utf-8'))
    except Exception as e:
        print('sender エラー', e)
    finally:
        pass

def receiver(file):
    try:
        while not stop_event.is_set():
            data = file.readline()
            if not data:
                print('サーバーが切断しました。')
                stop_event.set()
                break
            print('',data.decode('utf-8').rstrip('\n'))
    
    except Exception as e:
        print('receiverエラー', e)
    


def main():
    sock = socket.socket(socket.AF_UNIX, socket.SOCK_STREAM)

    try:
        sock.connect(SERVER_PATH)
    except socket.error as err:
        print(err)
        sys.exit(1)

    file = sock.makefile('rwb', buffering=0)

    signal.signal(signal.SIGINT, handler)

    t_sender = threading.Thread(target=sender, args=(file,))
    t_receiver = threading.Thread(target=receiver, args=(file,))

    t_sender.start()
    t_receiver.start()

    try:
        t_sender.join()
        t_receiver.join()
    finally:
        try:
            file.close()
        except:
            pass
        try:
            sock.close()
        except:
            pass
        print('クライアント終了')

if __name__ == '__main__':
    main()
