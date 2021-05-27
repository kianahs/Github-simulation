import socket
import threading

PORT = 7447
MESSAGE_LENGTH_SIZE = 64
ENCODING = 'utf-8'


def main():
    address = socket.gethostbyname(socket.gethostname())
    HOST_INFO = (address, PORT)
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.bind(HOST_INFO)
    print("[SERVER STARTED] Github server starting ....")
    start(s)


def start(server):
    server.listen()

    while True:
        conn, address = server.accept()
        t = threading.Thread(target=handle_client, args=(conn, address))
        t.start()


def handle_client(conn, address):
    print("[NEW CONNECTION] connected from {}".format(address))
    Connected = True

    while Connected:

        message_length = int(conn.recv(MESSAGE_LENGTH_SIZE).decode(ENCODING))

        msg = conn.recv(message_length).decode(ENCODING)

        print("[MESSAGE RECEIVED] {}".format(msg))

        if msg == "Login":
            pass

        if msg == "Register":
            print("[REQUEST] Register")
            username_length = int(conn.recv(MESSAGE_LENGTH_SIZE).decode(ENCODING))
            username = conn.recv(username_length).decode(ENCODING)
            password_length=int(conn.recv(MESSAGE_LENGTH_SIZE).decode(ENCODING))
            password=conn.recv(password_length).decode(ENCODING)
            print("username is {}".format(username))
            print("password is {}".format(password))

        if msg == "DISCONNECT":
            Connected = False

    conn.close()


def send_msg(server, msg):
    message = msg.encode(ENCODING)
    msg_length = len(message)
    msg_length = str(msg_length).encode(ENCODING)
    msg_length += b' ' * (MESSAGE_LENGTH_SIZE - len(msg_length))
    server.send(msg_length)
    server.send(message)



if __name__ == '__main__':
    main()
