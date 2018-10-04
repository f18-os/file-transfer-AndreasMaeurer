#! /usr/bin/env python3

"""This code is mostly taken from framedClient.py from the nets-tcp-framed-echo repository
"""
# remember that the usage with Stammering Proxy would be: ./fileClient.py -s localhost:50000

# Echo client program
import socket, sys, re
sys.path.append("../lib")       # for params
import params
from framedSock import framedSend, framedReceive

switchesVarDefaults = (
    (('-s', '--server'), 'server', "127.0.0.1:50001"),
    (('-d', '--debug'), "debug", False), # boolean (set if present)
    (('-?', '--usage'), "usage", False), # boolean (set if present)
    )

#progname = "framedClient"			#is this used anywhere else?
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
    af, socktype, proto, canonname, sa = res			#here also, 4 and 5, how? why?
    try:
        print("creating sock: af=%d, type=%d, proto=%d" % (af, socktype, proto))
        s = socket.socket(af, socktype, proto)
    except socket.error as msg:
        print(" error: %s" % msg)
        s = None
        continue
    try:
        print(" attempting to connect to %s" % repr(sa))
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


print("sending hello world")
framedSend(s, b"hello world", debug)
print("received:", framedReceive(s, debug))

print("sending hello world")
framedSend(s, b"hello world", debug)
print("received:", framedReceive(s, debug))

