import socket

PORT = 7447
MESSAGE_LENGTH_SIZE = 64
ENCODING = 'utf-8'


def main():
    address = socket.gethostbyname(socket.gethostname())
    SERVER_INFO = (address, PORT)
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.connect(SERVER_INFO)

    choose_operation(s)

    send_msg(s, "DISCONNECT")


def send_msg(client, msg):
    message = msg.encode(ENCODING)
    msg_length = len(message)
    msg_length = str(msg_length).encode(ENCODING)
    msg_length += b' ' * (MESSAGE_LENGTH_SIZE - len(msg_length))
    client.send(msg_length)
    client.send(message)

def choose_operation(s):

    print("Enter operation Login or Register")
    request=input()

    if request == "Register":
        print("username")
        username=input()
        print("password")
        password=input()
        send_msg(s,request)
        send_msg(s,username)
        send_msg(s,password)


if __name__ == '__main__':
    main()
