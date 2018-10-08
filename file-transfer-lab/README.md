[Usage:]
open a terminal,
navigate to the stammer-proxy directory 
and run the stammering proxy:
./stammerProxy.py

open another terminal
navigate to the file-transfer-lab directory
and run the fileServer:
./fileServer.py

open yet another terminal 
navigate to the file-transfer-lab directory
and run the fileServer:
./fileServer.py


[It works with or without the stammering proxy]

[Your assignment is to write fileClient.py and fileServer.py which can transfer a file ("put") from a client to the server. Your programs should:]

    be in the file-transfer-lab subdir 							
    work with and without the proxy								
    support multiple clients simultaneously using fork()
    gracefully deal with scenarios such as:
        zero length files
        user attempts to transmit a file which does not exist
        file already exists on the server
        the client or server unexpectedly disconnect
