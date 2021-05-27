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

        message_length = int(conn.recv(MESSAGE_LENGTH_SIZE).decode(ENCODING))

        msg = conn.recv(message_length).decode(ENCODING)

        print("[MESSAGE RECEIVED] {}".format(msg))

        if msg == "Login":
            print("[REQUEST] Login")
            send_msg(conn, "Please enter your user name and passcode")
            username_length = int(conn.recv(MESSAGE_LENGTH_SIZE).decode(ENCODING))
            username = conn.recv(username_length).decode(ENCODING)
            password_length = int(conn.recv(MESSAGE_LENGTH_SIZE).decode(ENCODING))
            password = conn.recv(password_length).decode(ENCODING)
            print("username is {}".format(username))
            print("password is {}".format(password))

        if msg == "Register":

            print("[REQUEST] Register")
            send_msg(conn, "Please enter your user name and passcode")
            username_length = int(conn.recv(MESSAGE_LENGTH_SIZE).decode(ENCODING))
            username = conn.recv(username_length).decode(ENCODING)
            password_length = int(conn.recv(MESSAGE_LENGTH_SIZE).decode(ENCODING))
            password = conn.recv(password_length).decode(ENCODING)
            print("username is {}".format(username))
            print("password is {}".format(password))
            register(username,password)

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

def register(username , password):

    List=[username,password]
    with open('accounts.csv', 'a') as f_object:
        # Pass this file object to csv.writer()
        # and get a writer object
        writer_object = csv.writer(f_object)

        # Pass the list as an argument into
        # the writerow()
        writer_object.writerow(List)

        # Close the file object
        f_object.close()




if __name__ == '__main__':
    main()
