import sys
import socket
import os

"""
auxiliary methods for fileServer.py
"""

def readn(sock, count):
    data = b''
    while len(data) < count:
        packet = sock.recv(count - len(data))
        if packet == '':
            return ''
        data += packet
    return data

"""
auxiliary methods for fileClient.py
"""

def usage2():
    print('Usage: fileClient.py <FILENAME> <SERVER IP>[OPTIONAL] <PORT>[OPTIONAL]')
    print('The Default Server IP is the localhost /(127.0.0.1/)')
    print('The Default Port is 50000')

def verifyInput():
	if sys.argv[1:] == '':
		print('Source file missing.', file=sys.stderr)
		usage2()
		sys.exit(1)
	elif sys.argv[2:] != '':
		server_addr = sys.argv[2:]
		
	elif sys.argv[2:] != '':
		server_port = sys.argv[2:]
		if not server_port.isdecimal():
			print('Server port number contains invalid characters.', file=sys.stderr)
			sys.exit(2)
			
