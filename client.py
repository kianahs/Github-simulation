import socket
import os
import datetime
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
            create_repository(s,username)
        if request == "commit & push":
            send_msg(s,request)
            commit_push(s,username)
        if request == "add contributor":
            send_msg(s,request)
            add_contributor_to_repository(s,username)
        if request == "pull":
            send_msg(s,request)
            pull(s,username)


def pull(s,username):
    pass



def add_contributor_to_repository(s,username):
    receive_msg(s)
    send_msg(s, input())
    receive_msg(s)
    send_msg(s, input())
    receive_msg(s)
    send_msg(s, input())


def convert_file_to_text(path):
    f = open(path, 'r')
    Lines = f.readlines()
    text=""
    for line in Lines:
        text += line+"\n"

    return text



def commit_push(s,username):

    receive_msg(s)
    repository=input()
    send_msg(s, repository)

    print("enter directory path")
    directory = input()

    receive_msg(s)
    # print(len(os.listdir(directory)))
    send_msg(s, str(len(os.listdir(directory))))

    for filename in os.listdir(directory):
        f = os.path.join(directory, filename)
        if os.path.isfile(f):
            print(f)
            send_msg(s,filename)
            send_msg(s,convert_file_to_text(f))



    receive_msg(s)
    commit=input()
    send_msg(s,commit)
    time = str(datetime.datetime.now().strftime("%d-%b-%Y-%H-%M-%S"))
    receive_msg(s)



    parent_directory="client-side"
    parent_directory=os.path.join(parent_directory,username)
    directory=os.path.join(parent_directory,"commits")
    repository+=".txt"
    commits_file_path=os.path.join(directory,repository)
    f=open(commits_file_path , 'a')
    f.write(commit+" "+time)
    f.write("\n")
    f.close()





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
    directory = username
    parent_dir = "C://Users//kiana//Desktop//university//term 6//Network//projects//Git_project//client-side"
    path = os.path.join(parent_dir, directory)
    os.mkdir(path)
    subDir="pulled-Repositories"
    path2=os.path.join(path,subDir)
    os.mkdir(path2)
    subDir="commits"
    path2 = os.path.join(path, subDir)
    os.mkdir(path2)
    subDir = "codes"
    path2 = os.path.join(path, subDir)
    os.mkdir(path2)




def receive_msg(client):

    message_length = int(client.recv(MESSAGE_LENGTH_SIZE).decode(ENCODING))
    msg = client.recv(message_length).decode(ENCODING)
    print(msg)

def create_repository(s,username):
    receive_msg(s)
    repositoryName=input()
    send_msg(s,repositoryName)
    receive_msg(s)






if __name__ == '__main__':
    main()
