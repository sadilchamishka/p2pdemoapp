import socket
import threading
from Node import Node
from concurrent.futures import ThreadPoolExecutor
from Utillities import requestBuilder, udpResponseSender

import constants as CONST
import RoutingTable as RT
import FileDirectory as FD

class UDPServer:
	def __init__(self, ip, port):
		self.ip = ip
		self.port = port
		self.server = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
		self.server.bind((self.ip, self.port))
	
	def serve(self):
		threading.Thread(target=self._start).start()

	def _start(self):
		executor = ThreadPoolExecutor(max_workers=3)
		while True:
			msg, addr = self.server.recvfrom(CONST.BUFFER_SIZE)
			executor.submit(self.__processRequest, msg=msg, addr=addr)	

	def __processRequest(self, msg, addr):
		msg = msg.decode("utf-8")
		toks = msg.split()
		if toks[1]=="JOIN":
			newNode = Node(toks[2], int(toks[3]))
			RT.table.append(newNode)
			print([(i.ip, i.port) for i in RT.table])
			msg = requestBuilder("JOINOK", "0")
			data = udpResponseSender(msg, addr)
		
		elif toks[1]=="SER":
			currentHop = int(toks[5])
			filesFound = 0
			fileNames = ""
			
			for file in FD.files:
				if toks[4].replace("-", " ") in file:
					filesFound+=1
					fileNames += " " + file
			
			if filesFound > 0:
				body = str(filesFound) + " " + self.ip + " " + str(self.port) + " " + str(currentHop) + fileNames
				msg = requestBuilder("SEROK", body)
				addr = (toks[2], int(toks[3]))
				udpResponseSender(msg, addr)
			
			elif currentHop > 0:
				body = toks[2] + " " + toks[3] + " " + toks[4] + " " + str(currentHop-1)
				msg = requestBuilder("SER", body)
				for neighbour in RT.table:
					addr = (neighbour.ip, neighbour.port)
					udpResponseSender(msg, addr)
		
		elif toks[1]=="SEROK":
			print(msg)
		
		elif toks[1]=="LEAVE":
			for neighbour in RT.table:
				if neighbour.port==int(toks[3]):
					RT.table.remove(neighbour)
					break
			print([(i.ip, i.port) for i in RT.table])
			msg = requestBuilder("LEAVEOK", "0")
			data = udpResponseSender(msg, addr)

		
