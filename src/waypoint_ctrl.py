#!/usr/bin/env python 
# waypoint controller

from time import sleep
from SimpleServer import SimpleServer, SimpleClient
class Node:
    def __init__(self, client=0):
        self.simple_server = SimpleServer((12380 + client), False)
        self.simple_client = SimpleClient(host='localhost', port=(12370 + client)) 
        self.client = client

    def request(self, waypoint):
        self.simple_server.broadcast("request, %s" % waypoint)
        while True:
            try:
                msg = self.simple_client.get_message()# this blocking when message received return
                if msg != None:
                    break
            except:
                sleep(.5)
    def return_waypoint(self, waypoint):
        self.simple_server.broadcast("return, %s" % waypoint)


class Manager:
    def __init__(self, num_waypoints=15, clients =2):
        self.num_waypoints = num_waypoints
        self.resources = [None]*self.num_waypoints
        host = {0:'localhost', 1:'localhost'}
        self.clients = clients
        self.simple_server, self.simple_client = {},  {}
        for client in range(self.clients):
            self.simple_server[client] = SimpleServer((12370+client), False)
            self.simple_client[client] = SimpleClient(host=host[client], port =(12380+client))
        self.loop()


    def request(self, client, waypoint):
        print "request from %s for waypoints %s " % (client, waypoint)

        if self.resources[waypoint]== None:
            self.resources[waypoint] = [client]
            self.respond(client)

        elif self.resources[waypoint][0] == client:
            self.respond(client)

        else:
            self.resources[waypoint].append(client)

    def return_waypoint(self, client, waypoint):
        print "%s returning waypoints %s " % (client, waypoint)
        if self.resources[waypoint] == None:
            print "no resource to return"
        elif self.resources[waypoint][0] != client:
            print "not your resource to return"


        elif len(self.resources[waypoint]) == 1:
            self.resources[waypoint]  = None
        else:
            self.resources[waypoint] = self.resources[waypoint] [1:] # dequeue first element
            self.respond(self.resources[waypoint][0])
        print self.resources

    def respond(self,client):
        print "broadcasting message to client %s " % client
        self.simple_server[client].broadcast("granted")
        print self.resources
        # def send message to client stating permission granted

    def loop(self):
        while True:
            for client in range(self.clients):
                try:
                    msg = self.simple_client[client].get_message()
                    msg_type, waypoint = msg.split(",")
                    waypoint = int(waypoint)
                except:
                    continue
                print ("msg received : %s " % msg)
                if msg_type == "request":
                    print "waypoint %d requested by client %s " % (waypoint, client)
                    self.request(client, waypoint)
                elif msg_type == "return":
                    print "waypoint %d requested by client %s " % (waypoint, client)
                    self.return_waypoint(client, waypoint)
                else:
                    print "%s is not a valid msg type" % msg_type


            

if __name__=="__main__":
    manager = Manager()
    
