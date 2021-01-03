import socket
from Node import Node
from UDPServer import UDPServer
from FlaskServer import FlaskServer
from Utillities import BoostrapRegistrate, BoostrapUnRegistrate, JoinNetwork, LeaveNetwork, AssignFiles, SerachFile

name = input("Please enter name : ")
udpServerPort = int(input("Please enter udp servere port : "))
flaskServerPort = int(input("Please enter flask servere port : "))

AssignFiles()

BootstrapNode = Node("127.0.0.1", 55555)
ClientNode = Node("127.0.0.1", udpServerPort, name)

nodeList = BoostrapRegistrate(BootstrapNode, ClientNode)
JoinNetwork(nodeList, ClientNode)

udpServer = UDPServer("127.0.0.1", udpServerPort)
udpServer.serve()

flaskServer = FlaskServer(name,flaskServerPort)
flaskServer.add_endpoint(endpoint='/<file>', endpoint_name='download file endpoint')
flaskServer.run()

while True:
   user_input  = input("What you need ........")
   if user_input=="exit":
      BoostrapUnRegistrate(BootstrapNode, ClientNode)
      LeaveNetwork(ClientNode)
      break
   else:
      SerachFile(user_input, ClientNode)


