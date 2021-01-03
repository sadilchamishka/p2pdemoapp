import socket
import random
from Node import Node

import constants as CONST
import RoutingTable as RT
import FileDirectory as FD

def requestBuilder(protocol, body):
    message = protocol + " " + body
    return bytes(message_with_length(message),"utf-8")

def udpRequestSender(msg, addr):
    client_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    client_socket.sendto(msg, addr)
    message, address = client_socket.recvfrom(CONST.BUFFER_SIZE)
    client_socket.close()
    return message.decode("utf-8")

def udpResponseSender(msg, addr):
    client_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    client_socket.sendto(msg, addr)
    client_socket.close()

def message_with_length(message):
    '''
    Helper function to prepend the length of the message to the message itself
    Args:
        message (str): message to prepend the length
    Returns:
        str: Prepended message
    '''
    message = " " + message
    message = str((10000+len(message)+5))[1:] + message
    return message

def BoostrapRegistrate(bs, client):
    '''
    Register node at bootstrap server.
    Args:
        bs (Node): Bootstrap server node
        client (Node): This node
    Returns:
        list(Node) : 0-2 neighbours in the distributed system
    Raises:
        RuntimeError: If server sends an invalid response or if registration is unsuccessful
    '''
    body = client.ip + " " +str(client.port) +" " + client.name
    msg = requestBuilder("REG", body)
    addr = (bs.ip, bs.port)
    data = udpRequestSender(msg, addr)
    toks = data.split()
    
    if (len(toks) < 3):
        raise RuntimeError("Invalid message")
    
    if (toks[1] != "REGOK"):
        raise RuntimeError("Registration failed")
    
    num = int(toks[2])
    if (num < 0):
        raise RuntimeError("Registration failed")

    if (num == 0):
        return []
    elif (num == 1):
        return [Node(toks[3], int(toks[4]), "")] 
    elif (num == 2):
        return [Node(toks[3], int(toks[4]), ""), Node(toks[5], int(toks[6]), "")] 
    
    
def BoostrapUnRegistrate(bs, client):
    '''
    Unregister node at bootstrap server.
    Args:
        bs (tuple(str, int)): Bootstrap server IP address and port as a tuple.
        me (tuple(str, int)): This node's IP address and port as a tuple.
        myname (str)        : This node's name
    Returns:
        list(tuple(str, int)) : List of other nodes in the distributed system
    Raises:
        RuntimeError: If unregistration is unsuccessful
    '''
    body = client.ip + " " +str(client.port) +" " + client.name
    msg = requestBuilder("UNREG", body)
    addr = (bs.ip, bs.port)
    data = udpRequestSender(msg, addr)
    toks = data.split()
    print(data)

    if (toks[1] != "UNROK"):
        raise RuntimeError("Unreg failed")


def JoinNetwork(nodeList, clientNode):
    for node in nodeList:
        newNode = Node(node.ip, node.port)
        RT.table.append(newNode)
        body = clientNode.ip + " " +str(clientNode.port)
        msg = requestBuilder("JOIN", body)
        addr = (node.ip, node.port)
        data = udpRequestSender(msg, addr)
        print(data)

def LeaveNetwork(clientNode):
    for neighbour in RT.table:
        body = clientNode.ip + " " +str(clientNode.port)
        msg = requestBuilder("LEAVE", body)
        addr = (neighbour.ip, neighbour.port)
        data = udpRequestSender(msg, addr)
        print(data)

def SerachFile(fileName, clientNode):
    fileName = fileName.replace(" ", "-")
    body = clientNode.ip + " " +str(clientNode.port) + " " + fileName + " " + str(CONST.NUM_HOPS)
    msg = requestBuilder("SER", body)
    addr = (clientNode.ip, clientNode.port)
    udpResponseSender(msg, addr)

def AssignFiles():
    file = open("fileNames.txt")
    filmList = file.readlines()
    randomList = random.sample(range(0, len(filmList)), 5)
    for i in randomList:
        FD.files.append(filmList[i].replace("\n",""))
    print(FD.files)