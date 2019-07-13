import socket
import json

def talk(question, userid='anon'):
    global sock
    query = {
        "userid": userid,
        "question" : question
    }
    sock = socket.socket()
    sock.connect(('localhost', 80))
    sock.send(json.dumps(query).encode())
    data = json.loads(sock.recv(16384).decode('utf-8'))
    sock.close()
    return(data['answer']['text'])

while True:
    a = input()
    if len(a) == 0: break
    else:
        print(talk(a))
