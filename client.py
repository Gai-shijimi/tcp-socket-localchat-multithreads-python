import socket
import signal
import sys
import threading
import select 

print_lock = threading.Lock()
PROMPT = 'message >>>>'

SERVER_PATH = '/tmp/socket_file'
stop_event = threading.Event()


def handler(signum, _):
    print(f"{signum}を受信しました。終了します。")
    stop_event.set()

def sender(file):
    try:
        while not stop_event.is_set():
            r, _, _ = select.select([sys.stdin], [], [], 10)
            if stop_event.is_set():
                break
            if r:
                line = sys.stdin.readline()
                if line == '':
                    stop_event.set()
                    break
            file.write(line.encode('utf-8'))
    
    except Exception as e:
        print('sender エラー', e)
    finally:
        pass

def receiver(file):
    try:
        while not stop_event.is_set():
            data = file.readline()
            if not data:
                with print_lock:
                    print('\nサーバーが切断しました。')
                stop_event.set()
                break
            msg = data.decode('utf-8').rstrip('\n')
            with print_lock:
                sys.stdout.write('\r')
                sys.stdout.write(' ' * 80 + '\r')
                print(msg, flush=True)
                raw_prompt()
    
    except Exception as e:
        print('receiverエラー', e)

def raw_prompt():
    sys.stdout.write(PROMPT)
    sys.stdout.flush()
    


def main():
    sock = socket.socket(socket.AF_UNIX, socket.SOCK_STREAM)

    try:
        sock.connect(SERVER_PATH)
    except socket.error as err:
        print(err)
        sys.exit(1)

    file = sock.makefile('rwb', buffering=0)

    signal.signal(signal.SIGINT, handler)

    t_sender = threading.Thread(target=sender, args=(file, ))
    t_receiver = threading.Thread(target=receiver, args=(file,))

    raw_prompt()

    t_sender.start()
    t_receiver.start()

    try:
        t_sender.join()
        t_receiver.join()
    finally:
        try:
            file.close()
            print("fileを閉じました。")
        except:
            pass
        try:
            sock.close()
            print("socketを閉じました。")
        except:
            pass
        

if __name__ == '__main__':
    main()
