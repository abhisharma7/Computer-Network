#!/usr/bin/python
## Created by Abhishek Sharma
import os
import socket
import time
import os.path
import datetime
import sys
import httplib

class http_:

	def recv_packet(self,sock,packet_size):			# Method will Analyse the HTTP Request Packet
		cwd = os.getcwd()
		request_receive =  sock.recv(int(packet_size))
		request_receive = str(request_receive)
		request_receive = request_receive.strip("\n")
                request_receive = request_receive.split("\n")

		for requested_file in request_receive:						# Extracting file Name from GET request.
			if requested_file.count("GET"):
				file_name_start_position = requested_file.find("/")
				file_name_end_position = requested_file.find("HTTP")
				file_name = requested_file[file_name_start_position + 1:file_name_end_position]	
				file_path = os.path.join(cwd, file_name)
				file_path = file_path.encode('ascii', 'ignore')
				file_path = file_path.strip()
			else:
				pass
		if file_name == ' ':								# Welcome Page of Web Server
			print "Requested:Welcome Page"
			HTML = ("<!DOCTYPE HTML PUBLIC -//IETF//DTD HTML 2.0//EN>"
				+"<html>"
				+"<head>"
 				+"<title>Default Page: Python Webserver 1.0.</title>"
				+"</head>"
				+"<body>"
   				+"<h1>Welcome</h1>"
   				+"<p>This is the default welcome page used to test the correct operation of the Python Webserver 1.0 after installation on systems..<p>"
				+"</body>"
				+"</html>");

			print "Response:HTTP/1.1 200 ( Welcome Page )"
			sock.send("HTTP/1.1 200 Ok\n"						# HTTP 200 Request for Default Web Browser Page.
        	        +"Date: " + str(datetime.datetime.now())
               		+"Server: Python Webserver/1.0"
               		+"Content-Type: text/html"
			+"Connection: Closed\n"
               		+"\n"
               		+HTML
               		+"\n");
			return
		else:
			print "Requested: " + file_name 
			try:
				(name, extension) = file_name.split(".")			# Sending Requested file to browser with HTTP 200 Header.
				if os.path.isfile(file_path):
    					file_read = open(file_path)
    					outputdata = file_read.read()
                                	sock.send("HTTP/1.1 200 Ok\n"
                                        	+"Date: " + str(datetime.datetime.now())
                                        	+"Server: Python Webserver/1.0"
                                        	+"Content-Type: text/html"
						+outputdata);
					#sock.send(outputdata)
					print "Response:HTTP/1.1 200 ( File Found on Server )\n"
					print "Data of File:\n"
					print outputdata
					return
			
	                        else:
        	      
                	                HTML = ("<!DOCTYPE HTML PUBLIC -//IETF//DTD HTML 2.0//EN>"		# If file not found on Server with HTTP 404 Header.
                        	                +"<html>"
                                	        +"<head>"
                                        	+ "<title>404 Not Found</title>"
                                       	 	+"</head>"
                                        	+"<body>"
                                        	+"<h1>Not Found</h1>"
                                        	+"<p>The requested page " + file_name + " was not found on this server.</p>"
                                        	+"</body>"
                                        	+"</html>");

                                	sock.send("HTTP/1.1 404 Not Found\n"
                                        	+"Date: " + str(datetime.datetime.now())
                                        	+"Server: Python Webserver/1.0"
                                        	+"Content-Type: text/html"
						+"Connection: Closed\n"
                                        	+"\n"
                                        	+HTML
                                        	+"\n");
					print "Response HTTP/1.1 404 ( File not found on Server )"
					return

			except Exception as error:								# HTTP 404 Bad Request Packet.
		        	HTML = ("<!DOCTYPE HTML PUBLIC -//IETF//DTD HTML 2.0//EN>"			
                                	+"<html>"
                                	+"<head>"
                                	+"<title>400 Bad Request</title>"
                                	+"</head>"
                                	+"<body>"
                                	+"<h1>Bad Request</h1>"
                                	+"<p>Your browser sent a request that this server could not understand.<p>"
                                	+"<p>The request line contained invalid characters following the protocol string.<p>"
                                	+"</body>"
                                	+"</html>");

                        	sock.send("HTTP/1.1 400 Bad Request\n"
                        		+"Date: " + str(datetime.datetime.now())
                        		+"Server: Python Webserver/1.0"
                        		+"Content-Type: text/html"
					+"Connection: Closed\n"
                        		+"\n"
                        		+HTML
                        		+"\n");	
				print "Response HTTP/1.1 400 ( Bad Request )"
				return
class Server(http_):
	
	def server_(self,HOST,PORT):
		HOST = str(HOST)
		PORT = int(PORT)
		s.setsockopt(socket.SOL_SOCKET,socket.SO_REUSEADDR,1)
		s.bind((HOST,PORT))
		s.listen(5)
		while True:	
			print "Listening at", s.getsockname()
			sc, sockname = s.accept()

			print "\n\nClient Request Received:"
			print "Accepted Connection from:", sockname
			print "Socket Connects", sc.getsockname(), 'and', sc.getpeername()		
			self.recv_packet(sc,MAX_SIZE)
			sc.close()
			print "Connection Closed!!!\n"		
	
class Client(http_):		
	
	def client_(self,HOST,PORT):
		HOST = str(HOST)
                PORT = int(PORT)
		if HOST == "127.0.0.1":
        	        HOST = "localhost"

		print "\nWelcome to Python Webserver 1.0 Client\n"
		print "Select any one of the following:"
		print "1.Welcome Page"
		print "2.File Name\n"
		
		option_selected = raw_input("Enter:")
		
		if option_selected == "1":
			start = time.time()
			http_connection = httplib.HTTPConnection(HOST,PORT)
	                http_connection.connect()
			http_connection.request("GET", "/")
			response = http_connection.getresponse()
			print "\nHTTP Response: " + str(response.status)
			data = response.read()
			print "\nData Received:\n\n" + str(data)
			http_connection.close()
			roundtriptime = time.time() - start
			print "Round trip time:"  + str(roundtriptime)
			save_file = raw_input("\nDo you want to save data?(Yes/No, Default:No):")
			if save_file == "Yes" or save_file == "yes":
				file_save = open("welcome",'w')
				file_save.write(data)
				file_save.close()
			else:
				print "\nConnection Closed!!!!"

		elif option_selected == "2":
			file_to_access = raw_input("Enter File Name(format filename.extension):")
                      	start = time.time()
			http_connection = httplib.HTTPConnection(HOST,PORT)
                        http_connection.connect()
		      	http_connection.request("GET", "/" + file_to_access)
                        response = http_connection.getresponse()	
                        print "\nHTTP Response: " + str(response.status)
                        data = response.read()
                        print "\nData Received:\n\n" + str(data)
			http_connection.close()
                        roundtriptime = time.time() - start
                        print "Round trip time:"  + str(roundtriptime)
			
                        save_file = raw_input("\nDo you want to save data?(Yes/No, Default:No):")
                        if save_file == "Yes" or save_file == "yes":
                                file_save = open(file_to_access,'w')
                                file_save.write(data)
                                file_save.close()
                        else:
                                print "\nConnection Closed!!!!"

		
		else:
			print "Bad Choice"
			sys.exit()

try:
	script = sys.argv[1]
except Exception as error:
	print "Syntax: python webserver.py client/server"
	sys.exit()

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
#HOST = '127.0.0.1'
#PORT = 8080
MAX_SIZE = '65535'

if script == "server":

	HOST = raw_input("Enter HOST IP:")
	PORT = raw_input("Enter PORT:")
	object = Server()
	object.server_(HOST,PORT)
		
elif script == "client":

        HOST = raw_input("Enter HOST IP:")
        PORT = raw_input("Enter PORT:")
        object = Client()
        object.client_(HOST,PORT)
else:
	print "Syntax: python webserver.py client/server"
