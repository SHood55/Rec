from risk import risk
from recommend import recommender
from getApps import getApps
from server import server
import socket
import sys
from thread import *
import traceback
import select
import BaseHTTPServer, SimpleHTTPServer, ssl


def main() :

#    name = "com.hdezninirola.frequency"
#     name = "no.nrk.yr"
#     name = "com.rovio.angrybirds"
#     dir = "/Users/Wschive/Desktop/"
#     name = "com.kabam.underworldandroid"
    getApps.run("com.bitdefender.clueful")
    risk.run("com.bitdefender.clueful")
#     recommender.recommend()

#     server.run()

    print "it ran!"



def hostSocket():
    CONNECTION_LIST = []    # list of socket clients
    RECV_BUFFER = 4096 # Advisable to keep it as an exponent of 2
    HOST = ''   # Symbolic name, meaning all available interfaces
    PORT = 8888 # Arbitrary non-privileged port

    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    # this has no effect, why ?
    server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    server_socket.bind(("0.0.0.0", PORT))
    server_socket.listen(10)

    # Add server socket to the list of readable connections
    CONNECTION_LIST.append(server_socket)

    while 1:
        # Get the list sockets which are ready to be read through select
        read_sockets,write_sockets,error_sockets = select.select(CONNECTION_LIST,[],[])

        for sock in read_sockets:

            #New connection
            if sock == server_socket:
                # Handle the case in which there is a new connection recieved through server_socket
                sockfd, addr = server_socket.accept()
                CONNECTION_LIST.append(sockfd)
                print "Client (%s, %s) connected" % addr

            #Some incoming message from a client
            else:
                # Data recieved from client, process it
                try:
                    #In Windows, sometimes when a TCP program closes abruptly,
                    # a "Connection reset by peer" exception will be thrown
                    data = sock.recv(RECV_BUFFER)
                    data2 = sock.read()
                    print "tries"
                    if data2:
                        print data2
                    # echo back the client message
                    if data:
                        print data
                        sock.send('OK ... ' + data)

                # client disconnected, so remove from socket list
                except:
                    sock.close()
                    CONNECTION_LIST.remove(sock)
                    continue

    server_socket.close()


#
#     s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
#     print 'Socket created'
#
#     #Bind socket to local host and port
#     try:
#         s.bind((HOST, PORT))
#     except socket.error as msg:
#             print 'Bind failed. Error Code : ' + str(msg[0]) + ' Message ' + msg[1]
#             sys.exit()
#
#     print 'Socket bind complete'
#
#     #Start listening on socket
#     s.listen(10)
#     print 'Socket now listening'
#
#     #now keep talking with the client
#     while 1:
#         #wait to accept a connection - blocking call
#         conn, addr = s.accept()
#         print 'Connected with ' + addr[0] + ':' + str(addr[1])
#         #start new thread takes 1st argument as a function name to be run, second is the tuple of arguments to the function.
#         start_new_thread(clientthread ,(conn,))
#
#     s.close()
#
# def clientthread(conn):
#     #Sending message to connected client
#     conn.send('Welcome to the server. Type something and hit enter\n') #send only takes string
#
#     #infinite loop so that function do not terminate and thread do not end.
#     while True:
#
#
#         for sock in read_sockets:
#
#         #Receiving from client
#         try:
#             data = conn.recv(1024)
#             if(data == "exit\r\n"):
#                 conn.close
#                 break
#             reply = 'OK...' + data
#             print data
#             conn.sendall(reply)
#         except:
#             continue
#
#
#
#     #came out of loop
#     conn.close()


if __name__ == "__main__" :
    main()