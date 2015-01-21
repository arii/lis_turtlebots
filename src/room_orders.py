#!/usr/bin/env python 
# waypoint controller
import numpy as np

from time import sleep
from SimpleServer import SimpleServer, SimpleClient
from threading import Thread
class Node:
    def __init__(self, client=0):
        self.simple_server = SimpleServer((12380 + client), False)
        self.simple_client = SimpleClient(host='localhost', port=(12370 + client)) 
        self.client = client
    
    def action_complete(self):
        self.simple_server.broadcast("completed action")

    def at_room(self, room_number, holding):
        self.simple_server.broadcast("at room, %s, %s" % (room_number, holding))
        while True:
            try:
                msg = self.simple_client.get_message()# this blocking when message received return
                print msg
                if msg != None:
                    break
            except:
                sleep(.5)
        try:
            order, holding =[ int(resp) for resp in  msg.split(",")]
            return order, holding
        except:
            print "msg %s does not split" % msg



class RoomOrders:
    NO_ORDERS, WANTS_TO_PLACE_ORDER, ORDER_PLACED = range(3)

    def __init__(self, clients =2):
        self.num_rooms = 3
        self.rooms = [self.NO_ORDERS]*self.num_rooms
        host = {0:'localhost', 1:'localhost'}
        self.clients = clients
        self.simple_server, self.simple_client, self.msg = {},  {}, {}
        self.continue_loop = True
        for client in range(self.clients):
            self.simple_server[client] = SimpleServer((12370+client), False)
            self.simple_client[client] = SimpleClient(host=host[client], port =(12380+client))
            self.msg[client] = []
            t = Thread(target=self.msg_queue, args=(client,))
            t.start()
        self.loop()

    def macro_action_completed(self):
        print "action completed, room states are %s " % self.rooms
        for i,room in enumerate(self.rooms):
            if room == self.NO_ORDERS:
                if  np.random.rand() < 0.4:
                    self.rooms[i] = self.WANTS_TO_PLACE_ORDER
     
    def turtle_at_room(self, client, room_number, holding):
        print "current state is "
        print self.rooms


        state = self.rooms[room_number]
        if holding:
            self.rooms[room_number] = self.NO_ORDERS
            if state == self.NO_ORDERS:
                return_msg =  "0, 1"
            elif state == self.WANTS_TO_PLACE_ORDER:
                return_msg =  "0, 0"
            elif state == self.ORDER_PLACED:
                return_msg =  "0, 0"
        else:
            if state == self.NO_ORDERS:
                return_msg =  "0, 0"
            elif state == self.WANTS_TO_PLACE_ORDER:
                return_msg = "1, 0"
                self.rooms[room_number] = self.ORDER_PLACED
            elif state == self.ORDER_PLACED:
                return_msg =  "0, 0"
        print "current room number = %s, holding = %s.  return order, holding = %s " % (room_number, holding, return_msg) 
        self.respond(client, return_msg)
        print "new state is " 
        print self.rooms


    def respond(self,client,msg):
        print "broadcasting message to client %s msg = %s" % (client, msg)
        self.simple_server[client].broadcast(msg)
        # def send message to client stating permission granted
   
    def msg_queue(self, client):
        while self.continue_loop:
            try:
                msg = self.simple_client[client].get_message()
                self.msg[client].append(msg)
            except:
                sleep(.5)

    def quit_keypress(self):
        print "q to quit"
        while self.continue_loop:
            stop = raw_input()
            if stop == "q":
                self.continue_loop = False
                break
            

    def loop(self):
        self.continue_loop = True
        t = Thread(target=self.quit_keypress)
        t.start()

        while self.continue_loop:
            for client in range(self.clients):
                try:
                    if len(self.msg[client]) > 0:
                        msg = self.msg[client].pop(0)
                    else:
                        continue
                    msg_parsed = msg.split(",")
                    print "msg_parsed is %s " % msg_parsed
                    if len(msg_parsed) == 1:
                        print "action completed by client %s " % (client)
                        self.macro_action_completed()
                    elif len(msg_parsed) == 3:
                        room_number = int(msg_parsed[1])
                        holding = int(msg_parsed[2])
                        print "about to call"
                        self.turtle_at_room(client, room_number, holding)
                    else:
                        print "%s is not a valid msg type" % msg_type
                except:
                    continue

def node_test(node):

    while True:
        num = raw_input("input a for action completed, action r for room followed by room_number and holding status, q to quit")
        if num == "q":
            break
        elif num == "a":
            node.action_complete()
        else:
            try:
                room, holding = [int(resp) for resp in num.split(",")]
                #         node.at_room(room, holding)
            except:
                print "%s wrong form" % num
                continue
            node.at_room(room, holding)
        
if __name__=="__main__":
    from argparse import ArgumentParser 
    parser = ArgumentParser()
    parser.add_argument("type", type=str)
    args = parser.parse_args()
    if args.type == "m":
        manager = RoomOrders()
    elif args.type == "1":
        node = Node(1)
        node_test(node)
    elif args.type == "0":
        node = Node(0)
        node_test(node)
    else:
        print "m, 0, or 1 "
        raise Exception

