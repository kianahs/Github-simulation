import socket
import os
import datetime
import csv
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
        msg=receive_msg(s)
        if msg=="Login unsuccessful - invalid username or password":
            return


        while True:
            print("select operation")
            request = input()

            if request == "3":
                send_msg(s, "create repository")
                create_repository(s,username)

            if request == "2":
                send_msg(s,"commit & push")
                receive_msg(s)
                value=input()
                send_msg(s,value)
                commit_push(s,username,value)

            if request == "5":
                send_msg(s,"add contributor")
                add_contributor_to_repository(s,username)

            if request == "1":
                send_msg(s,"pull")
                pull(s,username)

            if request == "6":
                print("enter repository name")
                repository=input()
                show_commits(username,repository)

            if request == "7":
                send_msg(s,"sync")
                sync(s,username)

            if request == "4":
                send_msg(s,"create sub directory")
                create_sub_directory(s,username)

            if request == "0":
                break




def create_sub_directory(s,username):
    receive_msg(s)
    send_msg(s,input())

    receive_msg(s)
    value=input()
    send_msg(s, value)

    receive_msg(s)
    send_msg(s, input())

    if value == "1":
        receive_msg(s)
        send_msg(s, input())
        receive_msg(s)

    elif value == "2":
        receive_msg(s)
        send_msg(s, input())
        receive_msg(s)
        send_msg(s, input())

        access = receive_msg(s)
        if access == "access failed":
            return
        receive_msg(s)




def sync(s,username):
    receive_msg(s)
    send_msg(s,input())

    receive_msg(s)
    send_msg(s, input())

    access=receive_msg(s)
    if access=="private repository access failed!":
        return

    receive_msg(s)
    file_name=input()
    send_msg(s, file_name)

    print("enter directory path")
    path=input()

    content=convert_file_to_text(path)
    send_msg(s,content)

    sync_check=receive_msg(s)

    if sync_check == "file is already update!":
        return
    else:
        updated_content =receive_msg(s)
        f=open(path,"w")
        f.write(updated_content)
        f.close()



def pull(s,username):

    receive_msg(s)
    send_msg(s,input())

    receive_msg(s)
    repository=input()
    send_msg(s,repository)

    access=receive_msg(s)

    if access == "private repository access failed!":
        return

    number_folder=int(receive_msg(s))

    parent_directory="client-side"
    parent_directory=os.path.join(parent_directory,username)
    parent_directory=os.path.join(parent_directory,"pulled-Repositories")
    parent_directory=os.path.join(parent_directory,repository)

    for i in range(number_folder):

        folder_name = receive_msg(s)
        number_files = int(receive_msg(s))
        directory = os.path.join(parent_directory, folder_name)

        if not os.path.exists(directory):
            os.makedirs(directory)

        for j in range(number_files):

            file_name=receive_msg(s)
            path = os.path.join(directory, file_name)
            file_content = receive_msg(s)
            f = open(path, 'w')
            f.write(file_content)
            f.close()


def add_contributor_to_repository(s,username):
    receive_msg(s)
    send_msg(s, input())
    receive_msg(s)
    send_msg(s, input())
    receive_msg(s)



def convert_file_to_text(path):
    f = open(path, 'r')
    Lines = f.readlines()
    text = ""
    # num = 0
    for line in Lines:
        # num += 1
        # if num != len(Lines):
        #     text += line + "\n"
        # else:
        text += line

    return text



def commit_push(s,username,value):

    if value == "1":
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
                filename = filename.replace(".txt", "")
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

    elif value == "2":

        receive_msg(s)
        send_msg(s,input())

        receive_msg(s)
        repository = input()
        send_msg(s, repository)

        access=receive_msg(s)

        if access == "access failed":
            return

        print("enter directory path")
        directory = input()

        receive_msg(s)
        # print(len(os.listdir(directory)))
        send_msg(s, str(len(os.listdir(directory))))

        for filename in os.listdir(directory):
            f = os.path.join(directory, filename)
            if os.path.isfile(f):
                print(f)
                filename=filename.replace(".txt","")
                send_msg(s, filename)
                send_msg(s, convert_file_to_text(f))

        receive_msg(s)
        commit = input()
        send_msg(s, commit)
        time = str(datetime.datetime.now().strftime("%d-%b-%Y-%H-%M-%S"))
        receive_msg(s)

        parent_directory = "client-side"
        parent_directory = os.path.join(parent_directory, username)
        directory = os.path.join(parent_directory, "commits")
        repository += ".txt"
        commits_file_path = os.path.join(directory, repository)
        f = open(commits_file_path, 'a')
        f.write(commit + " " + time)
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
    msg = receive_msg(s)
    if msg == "This username is already taken":
        return
    send_msg(s, password)
    directory = username
    parent_dir = "client-side"
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
    return msg

def create_repository(s,username):
    receive_msg(s)
    repositoryName=input()
    send_msg(s,repositoryName)
    receive_msg(s)
    send_msg(s,input())
    receive_msg(s)


def show_commits(username,repository):
    parent_dir="client-side"
    parent_dir=os.path.join(parent_dir,username)
    parent_dir=os.path.join(parent_dir,"commits")
    repository+=".txt"
    dir=os.path.join(parent_dir,repository)
    print(convert_file_to_text(dir))

if __name__ == '__main__':
    main()
