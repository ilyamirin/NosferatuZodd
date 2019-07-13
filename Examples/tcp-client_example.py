import socket
import json

sock = socket.socket()
sock.connect(('localhost', 80))

def talk(question, userid='anon'):
    global sock
    query = {
        "userid": userid,
        "question" : question
    }
    sock.send(json.dumps(query).encode())
    data = json.loads(sock.recv(16384).decode('utf-8'))
    return(data['answer']['text'])

while True: #падает на знаках препинания
    a = input()
    if len(a) == 0: break
    else:
        print(talk(a))
sock.close()