from socket import *
import sys
import os
ASCIIFORMAT = 'ASCII'
BYTEFORMAT = 'utf-8'

def __main__():

	if len(sys.argv) != 2:
		print('invalid number of arguments')
		exit(1)

	serverName = sys.argv[1]

	commandch = socket(AF_INET, SOCK_STREAM)
	commandch.connect((serverName, 21))
	print('Connected to ' + serverName)
	response = commandch.recv(1024)
	print(response.decode())
	user = input('User: ')
	command = 'USER ' + user + '\r\n'
	commandch.send(command.encode())
	response = commandch.recv(1024)
	print(response.decode())
	password = input('Password: ')
	command = 'PASS ' + password + '\r\n'
	commandch.send(command.encode())
	response = commandch.recv(1024)
	print(response.decode())

	while(True):

		command = input('ftp> ')

		if command.upper() == 'QUIT':
			command = 'QUIT\r\n'
			send(command, commandch)
			response = commandch.recv(1024)
			print(response.decode())
			commandch.close()
			quit()

		if command[:3].upper() == 'CD ':
			command = 'CWD '+ command[3:] +'\r\n'
			send(command,commandch)
			response = commandch.recv(1024)
			print(response.decode())

		if command[:3].upper() == 'GET':
			file = command[4:]
			datach = PASV(commandch, serverName)
			command = 'RETR ' + file + '\r\n'
			send(command, commandch)
			response = commandch.recv(1024)
			print(response.decode())
			file_data = datach.recv(1024).decode()
			f = open(file, 'w')
			for line in file_data:
				f.write(line)
			f.close()
			datach.close()
			response = commandch.recv(1024)
			print(response.decode())
			size = os.path.getsize(file)
			print('ftp: Successful file transfer. (' + str(size) + ' bytes received)')

		if command[:3].upper() == 'PUT':
			file = command[4:]
			datach = PASV(commandch, serverName)
			command = 'STOR ' + file + '\r\n'
			send(command, commandch)
			response = commandch.recv(1024)
			print(response.decode())
			f = open(file)
			file_data = f.read()
			datach.send(file_data.encode())
			f.close()
			datach.close()
			response = commandch.recv(1024)
			print(response.decode())
			size = os.path.getsize(file)
			print('ftp: Successful file transfer. (' + str(size) + ' bytes sent)')


		if command[:6].upper() == R'DELETE':

			command = 'DELE ' + command[7:] + '\r\n'
			send(command, commandch)
			response = commandch.recv(1024)
			print(response.decode())

		
		if command.upper() == 'LS':
			datach = PASV(commandch, serverName)
			command = 'LIST\r\n'
			send(command, commandch)
			response = commandch.recv(2048)
			print(response.decode()) 
			response = datach.recv(2048)
			print(response.decode())
			response = commandch.recv(2048)
			print(response.decode())
			datach.close()

			
def send(msg,channel):
	message = msg.encode(BYTEFORMAT)
	channel.send(message)
			
#returns port for data socket
def parsePASV(message):
	message = message.decode()
	m = message[message.find('(')+1:message.find(')')]
	m = m.split(',')	
	port = int(m[4]) * 256 + int(m[5])
	return port

def PASV(command_channel, server):
	command = 'PASV\r\n' 
	command_channel.send(command.encode())
	response = command_channel.recv(1024)
	dport = parsePASV(response) 
	datach = socket(AF_INET, SOCK_STREAM)
	datach.connect((server, dport))
	return datach

if __name__ == '__main__':

	__main__()
