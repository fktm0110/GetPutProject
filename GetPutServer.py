#!/usr/bin/python3

import os
import sys
import errno
import signal
import socket

BACKLOG = 5
host = ''
port = 10112
BUFF_SIZE = 1024

def collect_zombie(signum, frame):
    while True:
        try:
            pid, status = os.waidpid(-1, os.WNOHANG)
            if pid == 0:
                break
        except:
            break

def do_echo(sock):
    while True:
        message = sock.recv(BUFF_SIZE)
        try:
            if message:
                message = message.decode()
                Command = message[0:3]
                FileName = message[4:]
                if (Command == "get"):
                    myFile = open(FileName,"r")
                    FileConText = myFile.read()
                    print(FileConText)
                    sock.sendall(FileConText.encode())
                    myFile.close()
                    print("클라이언측 다운로드 완료하였습니다.")

                elif (Command == "put"):
                    FileConText = sock.recv(BUFF_SIZE)
                    FileConText = FileConText.decode()
                    if FileConText !="FILE NOT FOUND":
                        accessMode = "w"
                        myFile = open(FileName, accessMode)
                        myFile.write(FileConText)
                        myFile.close()
                        print("파일이 서버에 정상 탑재되었습니다.")
                    else:
                        print(FileConText)
                else:
                    print("명령어를 다시입력하시오")
        except FileNotFoundError:
            print("파일명을찾 을 수 없습니다.")
            sock.sendall("FILE NOT FOUND".encode())


signal.signal(signal.SIGCHLD, collect_zombie)

conn_sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
conn_sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
conn_sock.bind((host, port))
conn_sock.listen(BACKLOG)

print('Listening on port {}'.format(port))

while True:
    try:
        data_sock, client_address = conn_sock.accept()
        print('Got request from {} port{}'.format(client_address[0], client_address[1]))
    except IOError as e:
        code, msg = e.args
        if code == errno.EINTR:
            continue
        else:
            raise
    pid = os.fork()

    if pid == 0:
        conn_sock.close()
        do_echo(data_sock)
        os._exit(0)
    data_sock.close()
