import re

"""This code is mostly taken from framedSock.py from the nets-tcp-framed-echo repository
"""

filename = 'file001.jpg'	#random_filename()
            try:
				with open(filename, 'wb') as file_handle:
					while file_size > 0:
						buffer = lsock.recv(FILE_BUFFER_SIZE)		#Todo: MUSS GEGOOGLED WERDEN
						print(len(buffer), 'bytes received.')			#cool print line
						if buffer == '':
							print('End of transmission.')				#cool print line
							break
						#hash_algo.update(buffer)
						file_handle.write(buffer)
						file_size -= len(buffer)
					if file_size > 0:
						print('Failed to receive file,', file_size, 'more bytes to go.')
			except socket.error as e:
				print('Failed to receive data:', e, file=sys.stderr)
				lsock.close()  #clnt_sock.close()
				# serv_sock.close()
				sys.exit(3)
			except IOError as e:
				print('Failed to write file:', e, file=sys.stderr)
				lsock.close()  #clnt_sock.close()
				# serv_sock.close()
				sys.exit(3)
			else:
				print('File transmission completed.')
			#clnt_sock.shutdown(socket.SHUT_RD)
			lsock.shutdown(socket.SHUT_RD)
			#clnt_sock.close()
			lsock.close()			
			#serv_sock.close()
			print('Server shutdown.')
			#print('SHA256 digest:', hash_algo.hexdigest())

			#sys.exit(0) #Darf woll hier nicht raus






#in hier fuer Datei blah blah
def framedSend(sock, payload, debug=0):
     if debug: print("framedSend: sending %d byte message" % len(payload))
     #change string to file
     msg = str(len(payload)).encode() + b':' + payload
     while len(msg):
         nsent = sock.send(msg)
         msg = msg[nsent:]
     
rbuf = b""                      # static receive buffer

def framedReceive(sock, debug=0):
    global rbuf
    state = "getLength"
    msgLength = -1
    while True:
         if (state == "getLength"):
             #match = re.match(b'([^:]+):(.*)', rbuf) # look for colon							 #OLD 
             match = re.match(b'([^:]+):(.*)', rbuf, re.DOTALL | re.MULTILINE) # look for colon	 #NEW
             if match:
                  lengthStr, rbuf = match.groups()
                  try: 
                       msgLength = int(lengthStr)
                  except:
                       if len(rbuf):
                            print("badly formed message length:", lengthStr)
                            return None
                  state = "getPayload"
         if state == "getPayload":
             if len(rbuf) >= msgLength:
                 payload = rbuf[0:msgLength]
                 rbuf = rbuf[msgLength:]
                 return payload
         r = sock.recv(100)
         rbuf += r
         if len(r) == 0:
             if len(rbuf) != 0:
                 print("FramedReceive: incomplete message. \n  state=%s, length=%d, rbuf=%s" % (state, msgLength, rbuf))
             return None
         if debug: print("FramedReceive: state=%s, length=%d, rbuf=%s" % (state, msgLength, rbuf))
