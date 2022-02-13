# Anuraag Venkatapuram Sreenivas
# 1001716458


import socket
from threading import Thread
import datetime

clients = {}
addresses = {}

ip = '127.0.0.1'
PORT = 1234
BUFSIZ = 2048
ADDR = (ip, PORT)

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.bind(ADDR)

s.listen(5)

print('Ip Address of the Server::%s' % ip)

def listner():
    #listerns for incomming connections
    while True:
        client, address = s.accept()
        uname = client.recv(2048).decode('ascii')
        print('%s connected to the server' % str(uname))

        if (client not in clients):
            clients[uname] = client
            Thread(target=clientHandler, args=(client, uname,)).start()




def parse_raw_request(data):
    #parses teh data that has been hardcoded and encapsulated in html headers
        output = {}
        data = data.split("\r\n")
        data = data[1:]
        for i in data:
            key, value = i.split(':')
            output[key.replace(" ","")] = value.replace(" ","")

        data = output.get('Data')
        return data



def clientHandler(client, uname):
    #code to control the flow of ddata between the clients 1-1 or 1-*
    print(clients)
    welcome = 'Welcome %s! If you ever want to quit, type {/quit} to exit.' % uname
    client.send(bytes(welcome, "ascii"))
    keys = clients.keys()
    clientConnected = True
    while clientConnected:
        try:
            msg = client.recv(2048).decode('ascii')
            print(msg)
            response = 'Number of People Online\r\n'
            help = 'There are four commands in Messenger\r\n' \
                   '1::/chatlist : gives you the list of the people currently online\r\n' \
                   '2::/quit : To end your session\r\n' \
                   '3::/all : To broadcast your message to each and every person currently present online\r\n' \
                   '4::Add the name of the person at the end of your message preceded by / to send it to particular person\r\n' \
                   '5::/printrawmessage :to print unparsed message that has been snet to the server'

            found = False
            if '/chatlist' in msg:
                clientNo = 0
                for name in keys:
                    clientNo += 1
                    response = response + str(clientNo) + '::' + name + '/n'
                client.send(response.encode('ascii'))
            elif '/help' in msg:
                 client.send(help.encode('ascii'))
            elif '/printrawmessage' in msg:
                client.send(msg.encode('ascii'))
            elif '/all' in msg:
                msg = parse_raw_request(msg)
                msg = print1(msg)
                msg = msg.replace('/all', uname + ' sent to all: ')
                for k, v in clients.items():
                    v.send(msg.encode('ascii'))
            elif '/quit' in msg:
                response = 'Stopping Session and exiting...'
                client.send(response.encode('ascii'))
                clients.pop(uname)
                print(uname + ' has been logged out')
                clientConnected = False
            else:
                for name in keys:
                    if ('/' + name) in msg:
                        msg = parse_raw_request(msg)
                        msg = msg.replace('/' + name, uname + ': ')
                        clients.get(name).send(msg.encode('ascii'))
                        found = True
                if (not found):
                    client.send('Trying to send message to invalid person.'.encode('ascii'))
        except:
            clients.pop(uname)
            print(uname + ' has been logged out')
            clientConnected = False


def print1(msg):
    #this is the code for html file
    f = open('helloworld.html', 'w')
    print(datetime.datetime.now())
    message = """<html>
    <head></head>
    <body><p>"""+msg+"""</p></body>
    </html>"""
    print (message)
    f.write(message)
    f.close()
    return msg


ACCEPT_THREAD =Thread(target=listner)
ACCEPT_THREAD.start()
ACCEPT_THREAD.join()

s.close()