#!/usr/bin/env python
GABE = False

import math
import time
from SimpleServer import *
import rospy


if GABE:
    from std_msgs.msg import String
    from move_base_msgs.msg import MoveBaseActionResult
    from move_base_msgs.msg import MoveBaseGoal
    from move_base_msgs.msg import MoveBaseAction
    from move_base_msgs.msg import MoveBaseActionResult
    from geometry_msgs.msg import Twist
    from ar_track_alvar.msg import AlvarMarkers
    from geometry_msgs.msg import PoseWithCovarianceStamped
    import actionlib
    from multinavigator import *
    from waiter_locations import *
else:
    class MultiNavigator:
        pass

class Waiter(MultiNavigator):
    waiter_ports = {"donatello" : 12346, "leonardo" : 12347}
    DRINKS_ORDERS_LIMIT = {"room1" : 2, "room2" : 2, "room3" : 2}
    # states = "GO_TO_ROOM1", "GO_TO_ROOM2", "GO_TO_ROOM3", "GO_TO_KITCHEN", "WAIT_IN_KITCHEN", "ASK_FOR_DRINK", "GET_DRINK"
    
    def __init__(self, name, start_location = "kitchen", start_drinks_ordered = {"room1" : [], "room2" : [], "room3" : []}, start_action = "WAIT_IN_KITCHEN", debug = False, default_velocity = 0.3, default_angular_velocity = 0.75):
        if GABE:
            MultiNavigator.__init__(self, name, debug, default_velocity, default_angular_velocity)
        else:
            self.debug = True
            self.name = name
        #self.state = (location, drinks_ordered, drinks_on_turtlebot, state_of_pr2, state_of_other_turtlebot)
        
        self.action = start_action
        self.location = start_location # room1, room2, room3, kitchen, pr2, after_pr2
        
        self.drinks_ordered = start_drinks_ordered # 3-Tuple<List<2-Tuple<Integer, Float>>>
        self.drinks_on_turtlebot = 0
        
        self.talk_to_pr2_server = SimpleServer(port = self.waiter_ports[name], threading = True)
        pr2_host = "pr2mm1.csail.mit.edu"
        if (self.debug):
            pr2_host = "localhost"
        self.listen_to_pr2_client = SimpleClient(host = pr2_host, port = 12345) # "pr2mm1.csail.mit.edu"
        
        #self.goToPose(ROOM1_HALLWAY[0], ROOM1_HALLWAY[1])
        
        #if (self.name == "donatello"):
        #    self.goToPose(KITCHEN1[0], KITCHEN1[1])
        #else:
        #    self.goToPose(KITCHEN2[0], KITCHEN2[1])

        #self.eventLoop()

    def eventLoop(self):
        rospy.loginfo("starting event loop! current action = " + self.action)
        while True:
            if (self.action == "GO_TO_ROOM1"):
                if GABE: self.goToRoom1()
                else: self.dummy_action()
                self.action = "GO_TO_KITCHEN"
                #self.transitionToNextState(obs) # GO_TO_KITCHEN, GO_TO_ROOM

            elif (self.action == "GO_TO_ROOM2"):
                if GABE: self.goToRoom2()
                else: self.dummy_action()
                self.action = "GO_TO_KITCHEN"
                #self.transitionToNextState(obs) # GO_TO_KITCHEN, GO_TO_ROOM

            elif (self.action == "GO_TO_ROOM3"):
                if GABE: self.goToRoom3()
                else: self.dummy_action()
                self.action = "GO_TO_KITCHEN"
                #self.transitionToNextState(obs) # GO_TO_KITCHEN, GO_TO_ROOM

            elif (self.action == "GO_TO_KITCHEN"):
                if GABE:  self.goToKitchen()
                else: self.dummy_action()
                self.action = "WAIT_IN_KITCHEN"
                #self.transitionToNextState(obs) # WAIT_IN_KITCHEN, GO_TO_ROOM

            elif (self.action == "WAIT_IN_KITCHEN"):
                obs = self.waitInKitchen()
                if (obs == "come " + self.name):
                    self.action = "GET_DRINK"
                else:
                    self.action = "GO_TO_ROOM2"

                #self.transitionToNextState(obs) # GET_DRINK, GO_TO_ROOM
                #self.wait_until_msg_is("pr2 ready to place can")
                #self.send_msg_to_pr2("can i come")
                #self.wait_until_msg_is("come " + self.name)
                #self.state = self.APPROACHING_PR2

            elif (self.action == "GET_DRINK"):
                if GABE:
                    if (not self.debug):
                        self.approach()
                        #self.turn()
                    else:
                        #XXX raw_input("Hit enter to approach PR2...")
                        print ("Hit enter to approach PR2...")

                else: 
                    self.dummy_action()
                
                self.getDrink()
                self.action = "GO_TO_ROOM2"
                #self.transitionToNextState(obs) # GO_TO_ROOM
                #self.approach()
                #self.send_msg_to_pr2("turtle in place position")
                #self.state = self.WAITING_FOR_DRINK
            #if self.state == self.WAITING_FOR_DRINK:
                #self.wait_until_msg_is("pr2 placed object")
                #self.move(0.5, 0.25)
                #self.send_msg_to_pr2("turtle left pr2")
                #self.state = self.GOING_TO_KITCHEN
    def dummy_action(self):
        #raw_input("self dummy actions for %s"  % self.action)
        print("self dummy actions for %s"  % self.action)
        rospy.sleep(1)

    def transitionToNextAction(self, obs):
        pass

    #####################################################################################
    ################################### MACRO-ACTIONS ###################################
    #####################################################################################
    
    def goToRoom1(self):
        # initial position = room1, room2, room3, kitchen, or pr2
        rospy.loginfo("Going to room1...")
        if (True):
            if (self.location == "kitchen"):
                self.turn(5/6. * math.pi)
            self.wayposeNavigation(PATH_WAYPOSES[(self.location, "room1")])
        else:
            raw_input("Hit enter to go to room 1...")
        self.location = "room1"
        #self.deliverDrinks()
        #rospy.loginfo("STATE = (self.drinks_ordered = " + str(self.drinks_ordered) + " ; self.drinks_on_turtlebot = " + str(self.drinks_on_turtlebot))
        #self.getOrders()
        #rospy.loginfo("STATE = (self.drinks_ordered = " + str(self.drinks_ordered) + " ; self.drinks_on_turtlebot = " + str(self.drinks_on_turtlebot))
        
        
    def goToRoom2(self):
        # initial position = room1, room2, room3, kitchen, or pr2
        rospy.loginfo("Going to room2...")
        if (True):
            if (self.location == "kitchen"):
                self.turn(5/6. * math.pi)
            self.wayposeNavigation(PATH_WAYPOSES[(self.location, "room2")])
        else:
            raw_input("Hit enter to go to room 2...")
        self.location = "room2"
        #self.deliverDrinks()
        #rospy.loginfo("STATE = (self.drinks_ordered = " + str(self.drinks_ordered) + " ; self.drinks_on_turtlebot = " + str(self.drinks_on_turtlebot))
        #self.getOrders()
        #rospy.loginfo("STATE = (self.drinks_ordered = " + str(self.drinks_ordered) + " ; self.drinks_on_turtlebot = " + str(self.drinks_on_turtlebot))
    
    
    def goToRoom3(self):
        # initial position = room1, room2, room3, kitchen, or pr2
        rospy.loginfo("Going to room3...")
        if (True):
            if (self.location == "kitchen"):
                self.turn(5/6. * math.pi)
            self.wayposeNavigation(PATH_WAYPOSES[(self.location, "room3")])
        else:
            raw_input("Hit enter to go to room 3...")
        self.location = "room3"
        #self.deliverDrinks()
        #rospy.loginfo("STATE = (self.drinks_ordered = " + str(self.drinks_ordered) + " ; self.drinks_on_turtlebot = " + str(self.drinks_on_turtlebot))
        #self.getOrders()
        #rospy.loginfo("STATE = (self.drinks_ordered = " + str(self.drinks_ordered) + " ; self.drinks_on_turtlebot = " + str(self.drinks_on_turtlebot))
        
    
    def goToKitchen(self):
        # initial position = room1, room2, room3, kitchen, or pr2
        if (True):
            if (self.name == "donatello"):
                self.wayposeNavigation(PATH_WAYPOSES[(self.location, "kitchen1")])
            elif (self.name == "leonardo"):
                self.wayposeNavigation(PATH_WAYPOSES[(self.location, "kitchen2")])
        else:
            raw_input("Hit enter to go to the kitchen...")
        self.location = "kitchen"
        #self.listenToPR2()
    
    def waitInKitchen(self):
        self.wait_until_msg_is("pr2 ready to place can")
        self.send_msg_to_pr2("can i come")
        return self.wait_until_msg_is("come")
        
    
    def getDrink(self):
        if (not self.debug):
            self.approach()
            #self.turn()
        else:
            print ("Hit enter to approach PR2...")
            #XXX raw_input("Hit enter to approach PR2...")

        self.location = "pr2"
        self.send_msg_to_pr2("turtle in place position")
        if (not self.debug):
            self.turn()
        self.wait_until_msg_is("pr2 placed object")
        self.drinks_on_turtlebot += 1
        rospy.loginfo("STATE = (self.drinks_ordered = " + str(self.drinks_ordered) + " ; self.drinks_on_turtlebot = " + str(self.drinks_on_turtlebot))
        if (not self.debug):
            self.move(0.5, 0.25)
        else:
            print("Hit enter to leave PR2...")
            #XXX raw_input("Hit enter to leave PR2...")
            
        self.send_msg_to_pr2("turtle left pr2")
        
        if (not self.debug):
            self.wayposeNavigation(PATH_WAYPOSES[(self.location, "after_pr2")])
        self.location = "after_pr2"
        
    def goToAfterPR2(self):
        self.wayposeNavigation(PATH_WAYPOSES[(self.location, "after_pr2")])
        self.location = "after_pr2"
    
    
    ######################################################################################
    ################################## HELPER FUNCTIONS ##################################
    ######################################################################################
    
    def listenToPR2(self):
        old_msg = None
        msg = self.receive_msg_from_pr2()
        while (old_msg != msg):
            old_msg = msg
            msg = self.receive_msg_from_pr2()
        return msg
        
    ## self.drinks_ordered = [("roomX", number_of_drinks), ...]
    ## self.drinks_on_turtlebot = 0, 1, or 2
    
    #------------------------------------------------------
    # Integer ROOM := usually 0 (deliver drinks to the room that's been waiting the longest), but 
    #
    # CASES:
    #   self.drinks_on_turtlebot < self.drinks_ordered[ROOM][1]
    #       self.drinks_ordered[ROOM][1] -= self.drinks_on_turtlebot
    #       self.drinks_on_turtlebot = 0
    #   self.drinks_on_turtlebot == self.drinks_ordered[ROOM][1]
    #       self.drinks_ordered.pop(ROOM)
    #       self.drinks_on_turtlebot = 0
    #   self.drinks_on_turtlebot > self.drinks_ordered[ROOM][1]
    #       self.drinks_on_turtlebot -= self.drinks_ordered[ROOM][1]
    #       self.drinks_ordered.pop(ROOM)
    #
    #------------------------------------------------------
    def deliverDrinks(self):
        if (len(self.drinks_ordered[self.location]) > 0 and self.drinks_on_turtlebot > 0):
            drinks_to_deliver = min(self.drinks_ordered[self.location][0][0], self.drinks_on_turtlebot)
            raw_input("Grab " + str(drinks_to_deliver) + " drinks.")
        
            # reward
        
            if (self.drinks_on_turtlebot < self.drinks_ordered[self.location][0][0]):
                self.drinks_ordered[self.location][0][0] -= self.drinks_on_turtlebot
                self.drinks_on_turtlebot = 0
            elif (self.drinks_on_turtlebot == self.drinks_ordered[self.location][0][0]):
                self.drinks_ordered[self.location].pop(0)
                self.drinks_on_turtlebot = 0
            elif (self.drinks_on_turtlebot > self.drinks_ordered[self.location][0][0]):
                self.drinks_on_turtlebot -= self.drinks_ordered[self.location][0][0]
                self.drinks_ordered[self.location].pop(0)
            # Receive message saying that the drinks have been picked up by the people
            #drinks_delivered = 1
            #room_number = int(self.location[-1]) # self.location = "roomX" -> X = int(self.location[-1])
            #self.drinks_ordered[room_number] = max(0, self.drinks_ordered[room_number] - drinks_delivered)
        
    def getOrders(self):
        # Receive message saying how many drinks were ordered
        while (True):
            try:
                ordered_drinks = int(raw_input("How many drinks do you want? "))
                break
            except:
                pass
        open_drinks = sum([x[0] for x in self.drinks_ordered[self.location]])
        drinks_to_add = min(self.DRINKS_ORDERS_LIMIT[self.location] - open_drinks, ordered_drinks)
        if (drinks_to_add > 0):
            self.drinks_ordered[self.location].append([drinks_to_add, time.time()])
        #room_number = int(self.location[-1]) # self.location = "roomX" -> X = int(self.location[-1])
        #self.drinks_ordered[room_number] += 1
    
    def wait_until_msg_is(self, correct_msg):
        rospy.loginfo("waiting to receive following msg from PR2: %s" % correct_msg)
        msg = self.receive_msg_from_pr2()
        while (msg[:len(correct_msg)] != correct_msg):
            msg = self.receive_msg_from_pr2()
        return msg
              
    def send_msg_to_pr2(self, msg):
        rospy.loginfo( "sending message: %s " % msg)
        self.talk_to_pr2_server.update_broadcast(self.name + "," + msg)
        rospy.loginfo( "message sent: %s " % msg)
  
    def receive_msg_from_pr2(self):
        msg_received = False
        while not msg_received:
            try:
                msg = self.listen_to_pr2_client.get_message()
                msg_received = True
                #rospy.loginfo("message received is: %s " % msg)
            except:
                rospy.sleep(1)
        return msg
    
    
    


if __name__=="__main__":
    name = raw_input("Enter name: ")
    rospy.init_node("waiter_"+name)
    waiter = Waiter(name)
    raw_input("Hit enter to start...")
    waiter.eventLoop()

    
    








