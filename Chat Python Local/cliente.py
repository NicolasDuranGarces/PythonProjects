import socket
import select
import sys

server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
if len(sys.argv) != 3:
	print "Error: Debe introducir client.py IP PUERTO"
	exit()
IP_address = str(sys.argv[1])
Port = int(sys.argv[2])
server.connect((IP_address, Port))
nick = raw_input("Por favor introduce tu nick > ")
print("\n")
server.send(nick)
truck = server.recv(1)
while (truck == "0"):
    
	nick = raw_input("\nEse nick ya esta en uso, por favor introduce otro > ")
	server.send(nick)
	truck = server.recv(1)

while True:
	sockets_list = [sys.stdin, server]
	read_sockets, write_socket, error_socket = select.select(sockets_list, [], [])

	for socks in read_sockets:
		if socks == server:
			message = socks.recv(2048)
			print message
		else:
			message = sys.stdin.readline()
			server.send(message)
			CURSOR_UP = '\033[F'
			ERASE_LINE = '\033[K'
			print(CURSOR_UP + ERASE_LINE)
			sys.stdout.write("<Tu>")
			sys.stdout.write(message)
			sys.stdout.flush()
server.close()
