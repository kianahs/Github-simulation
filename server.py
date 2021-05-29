import socket
import threading
import csv
import os
import datetime
import time
import operator
from distutils.dir_util import copy_tree

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



def load_users_information():
    rows = []
    mydict = {}
    with open('accounts.csv', 'r') as csvfile:
        csvreader = csv.reader(csvfile)
        for row in csvreader:
            rows.append(row)

    for row in rows[:]:
        if len(row) > 1:
            mydict[row[0]] = row[1]

    return mydict


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
            # if i == -1:
            #     conn.close()

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
    dictionary=load_users_information()


    if username in dictionary.keys() and password == dictionary[username]:

        send_msg(conn,"login successfull \nchoose your operation \n0.exit\n1.pull\n2.commit & push\n3.create repository\n4.create sub directory\n5.add contributor\n6.show commits\n7.sync\n")

        while True:
            operation=receive_msg(conn)
            if operation == "create repository":
                print("[REQUEST] create repository")
                create_repository(conn,username)
            if operation == "commit & push":
                print("[REQUEST] commit & push")
                send_msg(conn,"1.owner of repository 2.contributor")
                value=receive_msg(conn)
                commit_push(conn,username,value)
            if operation == "add contributor":
                print("[REQUEST] add contributor")
                add_contibutor_to_repository(conn,username)
            if operation == "pull":
                print("[REQUEST] pull")
                pull(conn,username)
            if operation == "sync":
                print("[REQUEST] Sync")
                check_sync(conn,username)
            if operation == "create sub directory":
                print("[REQUEST] create sub directory")
                create_sub_directory(conn,username)
            if operation == "exit":
                return
            # end while
    else:
        send_msg(conn,"Login unsuccessful - invalid username or password")
        print("invalid username or password")





def create_sub_directory(conn,username):
    send_msg(conn,"enter directory name")
    directory=receive_msg(conn)
    send_msg(conn,"1.owner 2.contributor")
    value=receive_msg(conn)
    send_msg(conn, "1.directory 2.file")
    choose = receive_msg(conn)

    if value == "1":
        parent_dir="server-side"
        parent_dir=os.path.join(parent_dir,username)
        send_msg(conn,"enter repository name")
        repository=receive_msg(conn)
        parent_dir=os.path.join(parent_dir,repository)
        directory = os.path.join(parent_dir, directory)

        if choose=="1":
            if not os.path.exists(directory):
                os.makedirs(directory)
            send_msg(conn,"sub directory created!")
        elif choose == "2":
            f=open(directory,"w")
            f.close()
            send_msg(conn, "file created!")

    elif value == "2":
        send_msg(conn,"enter owner username")
        owner=receive_msg(conn)
        parent_dir = "server-side"
        parent_dir = os.path.join(parent_dir, owner)
        send_msg(conn,"enter repository name")
        repository = receive_msg(conn)
        access=check_access(owner,username,repository)
        if access == 0 :
            send_msg(conn, "access granted")
            parent_dir = os.path.join(parent_dir, repository)
            directory = os.path.join(parent_dir, directory)
            if choose == "1":
                if not os.path.exists(directory):
                    os.makedirs(directory)
                send_msg(conn,"sub directory created!")
            elif choose == "2":
                f = open(directory, "w")
                f.close()
                send_msg(conn, "file created!")

        elif access == 1:
            print("access failed")
            send_msg(conn,"access failed")





def check_sync(conn,username):

    folder_modify={}
    send_msg(conn,"enter owner of repository")
    owner=receive_msg(conn)
    send_msg(conn,"enter repository name")
    repository=receive_msg(conn)
    type=check_access(owner,"private",repository)
    access=check_access(owner,username,repository)
    if type==0 and access==1:
        send_msg(conn,"private repository access failed!")
        return
    else:
        send_msg(conn,"private repository access granted")
    send_msg(conn,"enter the file name for checking")
    filename=receive_msg(conn)

    parent_dir="server-side"
    parent_dir=os.path.join(parent_dir,owner)
    parent_dir=os.path.join(parent_dir,repository)

    for foldername in os.listdir(parent_dir):

        if filename in foldername:
            path=os.path.join(parent_dir,foldername)
            folder_modify[foldername]=time.ctime(os.path.getmtime(path))

    max_folder_name = max(folder_modify, key=folder_modify.get)
    print(max_folder_name)
    directory=os.path.join(parent_dir,max_folder_name)
    elements =os.listdir(directory)
    maximum = elements[0]
    for file in os.listdir(directory):

       if time.ctime(os.path.getmtime(os.path.join(directory,file))) > time.ctime(os.path.getmtime(os.path.join(directory,maximum))):
           maximum = file

    print(maximum)
    target_file_content=convert_file_to_text(os.path.join(directory,maximum))
    # print("target {}".format(target_file_content))
    receive_file_content=receive_msg(conn)
    # print("receive {}".format(receive_file_content))
    if target_file_content == receive_file_content:
        send_msg(conn,"file is already update!")

    else:
        send_msg(conn,"file is not update - sync")
        send_msg(conn,target_file_content)



def pull(conn,username):

    send_msg(conn,"please enter owners username ")
    owner_username=receive_msg(conn)
    send_msg(conn,"please enter requested repository name")
    requested_repository=receive_msg(conn)
    type=check_access(owner_username,"private",requested_repository)
    access=check_access(owner_username,username,requested_repository)
    if type == 0 and access == 1 :
        send_msg(conn,"private repository access failed!")
        return
    else:
        send_msg(conn, "private repository access granted")
    parent_dir="server-side"
    parent_dir=os.path.join(parent_dir,owner_username)
    directory=os.path.join(parent_dir,requested_repository)

    send_msg(conn , str(len(os.listdir(directory))))

    for foldername in os.listdir(directory):
        # print("folder name {}".format(foldername))
        f = directory
        f = os.path.join(directory, foldername)
        send_msg(conn , foldername)
        send_msg(conn, str(len(os.listdir(f))))

        for filename in os.listdir(f):
            # print("innnnnnnnnn {}".format(filename))
            f2 = os.path.join(f, filename)
            if os.path.isfile(f2):
                print(f2)
                send_msg(conn, filename)
                send_msg(conn, convert_file_to_text(f2))


    send_msg(conn,"repository pulled successfully")


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

def add_contibutor_to_repository(conn,username):
    send_msg(conn,"enter repository name")
    repository=receive_msg(conn)
    send_msg(conn,"enter contributor username")
    c_username=receive_msg(conn)
    parent_dir="server-side"
    parent_dir=os.path.join(parent_dir,username)
    filename="access "+repository+".txt"
    directory=os.path.join(parent_dir,filename)
    f=open(directory,'a')
    f.write(c_username+"\n")
    f.close()
    send_msg(conn,"contributor added successfully")

def commit_push(conn,username,value):
    if value=="1":
        parent_directory="server-side"
        parent_directory=os.path.join(parent_directory,username)
        commit_path=parent_directory

        send_msg(conn,"please choose your repository")
        repository = receive_msg(conn)
        parent_directory = os.path.join(parent_directory,repository)
        send_msg(conn,"enter number of push files")
        number = int(receive_msg(conn))
        time = str(datetime.datetime.now().strftime("%d-%b-%Y-%H-%M-%S"))

        for i in range(number):

            file_name = receive_msg(conn)
            directory=os.path.join(parent_directory,file_name)

            if not os.path.exists(directory):
                os.makedirs(directory)
            destination_file_name = "version " + time + ".txt"
            path=os.path.join(directory,destination_file_name)
            file_content = receive_msg(conn)
            f=open(path,'w')
            f.write(file_content)
            f.close()


        send_msg(conn,"please enter your commit")
        commit = receive_msg(conn)
        commitFileName="commit"+"-"+repository+".txt"
        commitFileName=os.path.join(commit_path,commitFileName)
        commit+=" "
        list=[commit,time]
        f=open(commitFileName, 'a')
        for item in list:
            f.write(item)
        f.write("\n")
        f.close()

        send_msg(conn,"commit and push done successfully!")

    elif value=="2":

        send_msg(conn,"enter owner of repository")
        owner=receive_msg(conn)
        send_msg(conn, "enter repository name")
        repository=receive_msg(conn)
        access=check_access(owner,username,repository)
        if access == 1:
            send_msg(conn,"access failed")
            print("user doesnt have access to this repository")
        elif access == 0:
            send_msg(conn, "access granted")
            parent_directory = "server-side"
            parent_directory = os.path.join(parent_directory, owner)
            commit_path = parent_directory
            parent_directory = os.path.join(parent_directory, repository)
            send_msg(conn, "enter number of push files")
            number = int(receive_msg(conn))
            time = str(datetime.datetime.now().strftime("%d-%b-%Y-%H-%M-%S"))
            for i in range(number):

                file_name = receive_msg(conn)
                file_name = username+"-"+file_name
                directory = os.path.join(parent_directory,file_name)

                if not os.path.exists(directory):
                    os.makedirs(directory)
                destination_file_name = "version " + time + ".txt"
                path=os.path.join(directory,destination_file_name)
                file_content = receive_msg(conn)
                f=open(path,'w')
                f.write(file_content)
                f.close()
            send_msg(conn, "please enter your commit")
            commit = receive_msg(conn)
            commitFileName = username + "-commit" + "-" + repository + ".txt"
            commitFileName = os.path.join(commit_path, commitFileName)
            commit += " "
            list = [commit, time]
            f = open(commitFileName, 'a')
            for item in list:
                f.write(item)
            f.write("\n")
            f.close()
            send_msg(conn, "commit and push done successfully!")

def create_repository(conn,username):
    send_msg(conn, "please enter your repository name")
    directory=receive_msg(conn)
    send_msg(conn, "public or private")
    show = receive_msg(conn)
    parent_dir="server-side"
    path1 = os.path.join(parent_dir, username)
    path = os.path.join(path1,directory)
    os.mkdir(path)
    username+="\n"
    access_file="access "+directory+".txt"
    access_file=os.path.join(path1,access_file)
    f=open(access_file,"w")
    if show == "private":
        f.write(show+"\n")
    f.write(username)
    # f.write("\n")
    f.close()
    send_msg(conn,"repository created successfully")

def register(conn):

    dictionary=load_users_information()
    print("[REQUEST] Register")
    send_msg(conn, "Please enter your user name and passcode")
    username = receive_msg(conn)
    if username not in dictionary.keys():
        send_msg(conn, "username available!")
        password = receive_msg(conn)
        print("username is {}".format(username))
        print("password is {}".format(password))
        parent="server-side"
        path=os.path.join(parent,username)
        os.mkdir(path)

        List=[username,password]
        with open('accounts.csv', 'a') as f_object:
            writer_object = csv.writer(f_object)
            writer_object.writerow(List)
            f_object.close()
    else:
        send_msg(conn,"This username is already taken")

def receive_msg(conn):
    message_length = int(conn.recv(MESSAGE_LENGTH_SIZE).decode(ENCODING))
    msg = conn.recv(message_length).decode(ENCODING)
    return msg

def check_access(owner,username,repository):
    parent_dir="server-side"
    parent_dir=os.path.join(parent_dir,owner)
    repository="access "+repository+".txt"
    dir=os.path.join(parent_dir,repository)
    content=convert_file_to_text(dir)
    if username in content:
        return 0
    else:
        return 1


if __name__ == '__main__':
    main()
