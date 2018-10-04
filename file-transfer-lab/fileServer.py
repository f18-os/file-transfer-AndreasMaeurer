#! /usr/bin/env python3

"""taken from framedForkServer.py from the nets-tcp-framed-echo repository
"""
import sys, os, socket
import struct
sys.path.append("../lib")       # for params
import params

FILE_BUFFER_SIZE = 100

switchesVarDefaults = (
	(('-l', '--listenPort') ,'listenPort', 50001),
	(('-d', '--debug'), "debug", False), # boolean (set if present)
	(('-?', '--usage'), "usage", False), # boolean (set if present)
	)
	
paramMap = params.parseParams(switchesVarDefaults)

debug, listenPort = paramMap['debug'], paramMap['listenPort']

if paramMap['usage']:
	params.usage()

lsock = socket.socket(socket.AF_INET, socket.SOCK_STREAM) # listener socket
bindAddr = ("127.0.0.1", listenPort)
lsock.bind(bindAddr)
lsock.listen(5)
print("listening on:", bindAddr)

while True:
	sock, addr = lsock.accept()
	
	from framedSock import framedSend, framedReceive
	from aux import readn
	
	if not os.fork():
		print("new child process handling connection from", addr)
		while True:
			
			size_buff = readn(sock, 4)
			if size_buff == '':
				print('Failed to receive file size.', file=sys.stderr)
				lsock.close()
				sys.exit(3)
			
			size_unpacked = struct.unpack('!I', size_buff)
			file_size = size_unpacked[0]
			print('Will receive file of size', file_size, 'bytes.')
			filename = 'file001.jpg'
			with open(filename, 'wb') as file_handle:
				while file_size > 0:
					buffer = sock.recv(FILE_BUFFER_SIZE)	#recv(buflen[, flags]) -- receive data  (from python help() socket)
					print(len(buffer), 'bytes received.')	#nice print line
					if buffer == '':
						print('End of transmission.')		#nice print line
						break					
					file_handle.write(buffer)
					file_size -= len(buffer)
				if file_size > 0:
					print('Failed to receive file,', file_size, 'more bytes to go.')			
				print('File transmission completed.')			
			sock.shutdown(socket.SHUT_RD)			
			lsock.close()			
			print('Server shutdown.')			
			sys.exit(0) #or not ?
			
