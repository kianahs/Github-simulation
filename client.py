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
    send_msg(s, request)

    if request == "Register":
        register(s)

    elif request == "Login":
        username=login(s)
        receive_msg(s)
        request=input()

        if request == "create repository":
            send_msg(s, request)
            print("sent cr")
            create_repository(s,username)


def login(s):

    receive_msg(s)
    print("username")
    username = input()
    print("password")
    password = input()
    send_msg(s, username)
    send_msg(s, password)
    return username

def register(s):
    receive_msg(s)
    print("username")
    username = input()
    print("password")
    password = input()
    send_msg(s, username)
    send_msg(s, password)


def receive_msg(client):

    message_length = int(client.recv(MESSAGE_LENGTH_SIZE).decode(ENCODING))
    msg = client.recv(message_length).decode(ENCODING)
    print(msg)

def create_repository(s,username):
    receive_msg(s)
    repositoryName=input()
    repositoryName=username+" "+repositoryName
    send_msg(s,repositoryName)
    receive_msg(s)






if __name__ == '__main__':
    main()
