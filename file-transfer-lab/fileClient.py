#! /usr/bin/env python3

"""taken from framedClient.py from the nets-tcp-framed-echo repository
"""
# the usage with Stammering Proxy: ./fileClient.py -s localhost:50000		is hardcoded below (for now)

import os
import sys
import struct
import socket
import re
sys.path.append("../lib")       # for params
import params
from framedSock import framedSend, framedReceive
import argparse

#info about input arguments get opt and more from:
#https://www.tutorialspoint.com/python/python_command_line_arguments.htm
#and:
#https://codereview.stackexchange.com/questions/197462/large-file-transmission-over-socket-in-python
#info about argparse from:
#https://www.youtube.com/watch?v=cdblJqEUDNo
#and:
#https://docs.python.org/3/library/argparse.html

#trying to figure out parameters to send the filename
"""
parser = argparse.ArgumentParser(description='Usage: fileClient.py <FILENAME> <SERVER IP> <PORT>')
parser.add_argument('filename', type=str, help='Source file to send')
parser.add_argument('serverIP', type=str, help='Server address')				#the ip address is a number separated by dots. does that make it a string?
parser.add_argument('port', type=str, help='Server port number')
args = parser.parse_args()

print(args.filename)
print(args.serverIP)
print(args.port)
"""
FILE_BUFFER_SIZE = 100

switchesVarDefaults = (
    (('-s', '--server'), 'server', "127.0.0.1:50001"),
    (('-d', '--debug'), "debug", False), # boolean (set if present)
    (('-?', '--usage'), "usage", False), # boolean (set if present)
    )

paramMap = params.parseParams(switchesVarDefaults)
server, usage, debug  = paramMap["server"], paramMap["usage"], paramMap["debug"]

if usage:
    params.usage()

try:
    serverHost, serverPort = re.split(":", server)
    serverPort = int(serverPort)
except:
    print("Can't parse server:port from '%s'" % server)
    sys.exit(1)

s = None
for res in socket.getaddrinfo(serverHost, serverPort, socket.AF_UNSPEC, socket.SOCK_STREAM):
    af, socktype, proto, canonname, sa = res			#here also, 4 and 5, how? why?  canonname seems meaningless
    try:
        print("creating sock: af=%d, type=%d, proto=%d" % (af, socktype, proto))
        s = socket.socket(af, socktype, proto)
    except socket.error as msg:
        print(" error: %s" % msg)
        s = None
        continue
    try:
        print(" attempting to connect to %s" % repr(sa))	#str() is used for creating output for end user while repr() is mainly used for debugging and development. repr’s goal is to be unambiguous and str’s is to be readable.  from: https://www.geeksforgeeks.org/str-vs-repr-in-python/
        s.connect(sa)
    except socket.error as msg:
        print(" error: %s" % msg)
        s.close()
        s = None
        continue
    break

if s is None:
    print('could not open socket')
    sys.exit(1)

#For Debugging:
source_file = 'HelloWikipediaCropped.jpg'
server_addr = '127.0.0.1'	
server_port = '50000'   # stammerProxy listens on 50000			#   forwards to 127.0.0.1:50001

#also here trying to figure out how to send the filename from Client to Server.
#source_file = args.filename
#server_addr = args.serverIP
#server_port = args.port

file_size = os.path.getsize(source_file)
print('Sending file size to remote server.')
buffer = b''
buffer = struct.pack('!I', file_size)
print('File size packed into binary format:', buffer)

try:
	s.sendall(buffer)
except socket.error as e:
	print('Failed to send file size:', e)
	sys.exit(3)
else:
	print('File size sent.')
	
print('Start to send file content.')
try:
	with open(source_file, 'rb') as file_handle:
		buffer = file_handle.read(FILE_BUFFER_SIZE)
		while len(buffer) > 0:			
			s.sendall(buffer)
			buffer = file_handle.read(FILE_BUFFER_SIZE)        
except IOError as e:
	print('Failed to open source file', source_file, ':', e, file=sys.stderr)
	sys.exit(3)
	
s.shutdown(socket.SHUT_WR)
s.close()
print('File sent, connection closed.')
sys.exit(0)
