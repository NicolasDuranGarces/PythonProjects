import socket
import select
import sys
from thread import *

server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)

if len(sys.argv) != 3:
	print "Error: Debe introducir server.py [IP] [PUERTO]"
	exit()

IP_address = str(sys.argv[1])

Port = int(sys.argv[2])

server.bind((IP_address, Port))

server.listen(100)

list_of_clients = []

nicks = {"admin": "admin"}


def clientthread(conn, addr):
	conn.send("Bienvenido al chat {0}!!!".format(nicks[conn]))

	while True:
		try:
			message = conn.recv(2048)
			if message:
				print "<" + addr[0] + " " + nicks[conn] + " > " + message

				message_to_send = "<" + nicks[conn] + "> " + message
				broadcast(message_to_send, conn)
			else:
				
				remove(conn)

		except:
			continue

def broadcast(message, connection):
	for clients in list_of_clients:
		if clients != connection:
			try:
				clients.send(message)
			except:
				clients.close()
			remove(clients)


def remove(connection):
    	if connection in list_of_clients:
		list_of_clients.remove(connection)


while True:

	conn, addr = server.accept()
	nick = conn.recv(2048)


	list_of_clients.append(conn)

	
	t = True
	for i in nicks:
		if nicks[i] == nick:
			t = True
		else:
			t = False
	if t == False:
		nicks[conn] = nick
		conn.send("1")
	else:
		while t:
			conn.send("0")
			nick = conn.recv(2048)
			if nicks[i] == nick:
				t = True
			else:
				t = False
				nicks[conn] = nick
				conn.send("1")
	print addr[0] + " " + nick + " conectado"

	start_new_thread(clientthread, (conn, addr))
conn.close()
server.close()
