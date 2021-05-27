import socket
import threading
import csv


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
        t = threading.Thread(target=handle_client, args=(conn, address, server))
        t.start()


def handle_client(conn, address ,server):
    print("[NEW CONNECTION] connected from {}".format(address))
    Connected = True

    while Connected:
        msg=receive_msg(conn)

        print("[MESSAGE RECEIVED] {}".format(msg))

        if msg == "Login":
            login(conn)

        if msg == "Register":
            register(conn)


        if msg == "DISCONNECT":
            Connected = False

    conn.close()


def send_msg(conn, msg):
    message = msg.encode(ENCODING)
    msg_length = len(message)
    msg_length = str(msg_length).encode(ENCODING)
    msg_length += b' ' * (MESSAGE_LENGTH_SIZE - len(msg_length))
    conn.send(msg_length)
    conn.send(message)

def login(conn):
    print("[REQUEST] Login")
    send_msg(conn, "Please enter your user name and passcode")
    username = receive_msg(conn)
    password = receive_msg(conn)
    print("username is {}".format(username))
    print("password is {}".format(password))
    send_msg(conn, "login successfull \n choose your operation \n pull-push-commit-create repository")
    operation=receive_msg(conn)
    if operation == "create repository":
        print("[REQUEST] create repository")
        create_repository(conn)

def create_repository(conn):
    send_msg(conn, "please enter your repository name")
    repositoryName=receive_msg(conn)
    repositoryName+=".txt"
    f = open(repositoryName, "w")
    f.close()
    send_msg(conn,"repository created successfully")


def register(conn):
    print("[REQUEST] Register")
    send_msg(conn, "Please enter your user name and passcode")
    username = receive_msg(conn)
    password = receive_msg(conn)
    print("username is {}".format(username))
    print("password is {}".format(password))

    List=[username,password]
    with open('accounts.csv', 'a') as f_object:
        writer_object = csv.writer(f_object)
        writer_object.writerow(List)
        f_object.close()

def receive_msg(conn):
    message_length = int(conn.recv(MESSAGE_LENGTH_SIZE).decode(ENCODING))
    msg = conn.recv(message_length).decode(ENCODING)
    return msg


if __name__ == '__main__':
    main()
