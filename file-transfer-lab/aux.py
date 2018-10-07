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
