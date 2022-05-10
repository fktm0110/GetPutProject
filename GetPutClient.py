import socket
import sys

host = '203.250.133.88'
port = 10112
BUFF_SIZE = 128

sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

server_address = (host, port)
print("connecting to {} port {}".format(server_address[0], server_address[1]))
sock.connect(server_address)


message = input("vsftp > ")
while message !="quit":
    try:
        sock.sendall(message.encode())
        Command = message[0:3]
        FileName = message[4:]

        if Command == "put":
            myFile = open(FileName, "r")
            FileConText = myFile.read()
            print(FileConText)
            sock.sendall(FileConText.encode())
            myFile.close()
            print("서버측에 업로드 완료하였습니다.")

        elif Command == "get":
            FileConText = sock.recv(BUFF_SIZE)
            FileConText = FileConText.decode()
            if FileConText != "FILE NOT FOUND":
                accessMode = "w"
                myFile = open(FileName, accessMode)
                myFile.write(FileConText)
                print(FileConText)
                print("클라이언측 다운로드 완료하였습니다.")
            else:
                print(FileConText)
        else:
            print("명령어가 아닙니다.")

    except FileNotFoundError:
        print("파일이 존재 하지 않습니다.")
        sock.sendall("FILE NOT FOUND".encode())

    message = input("vsftp > ")

sock.close()