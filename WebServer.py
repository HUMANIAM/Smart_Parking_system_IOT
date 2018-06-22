#import the socket package
import socket
import os
import time
from urllib.request import urlopen
"""
TCP guarantees connection_oriented , reliable transfer
and congestion flow
"""
class WebServer(object):
	def __init__(self):
		self.parkingName = 'zefta'
		self.mysock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)         #create socket with Tcp connection
		serverAddress = ('192.168.1.7', 8110)                                   #server address
		try:
			#bind mysock with serverAddress
			self.mysock.bind(serverAddress)
		except:
			print("Address already in use")
			exit(1)
		#is how many connections the OS may accept on behalf of the application. 
		self.mysock.listen(3)
		pass
		
	def StartSevices(self):
		#waits requests from clients
		while True:
			#accept connection with the client
			(clientSocket, addr) = self.mysock.accept()    #accept connections
			request = clientSocket.recv(1024).decode()
			#send response
			response, slots = self.GetResponse(request)
			if(response != ''):
                                self.InformServer(slots)
                                clientSocket.sendall(response.encode())
                                
			clientSocket.close()                            # Close the connection
		#close the server socket
		self.mysock.close()               
		pass
	
	
	def GetHeader(self, statusCode, length = 0, filepath = ''):
                #response header
                header = "HTTP/1.1 200 OK\n"
                header += 'Server : SimpleTcpServer\n'
                header += ("Date : " + time.strftime("%c") + "\n")
                header += "Content_Type : plain_txt\n"
                header += "Content_Length  : " + str(length) + "\n"
                header += 'Connection : Close\n\n'
                return header

		
	def GetResponse(self, request):
		#split it to get the desired path
		if(request):
			request_parts = request.split()
			slots = request_parts[1][1:]  
		else: 
			return ''
			
		header = self.GetHeader(200, len(slots), '')
		responsData =  header + '1'
		return responsData, slots

	
	def InformServer(self, slots):
                try:
                        serverurl = 'http://192.168.1.7:8100/'+self.parkingName+'|'+slots
                        res = urlopen(serverurl).read().decode()
                except Exception as e:
                        print('an exception during send state change to the server:\n', e)


def main():
	webserver = WebServer()
	webserver.StartSevices()
	
if __name__=="__main__":
	main()
