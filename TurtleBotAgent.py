#!/usr/bin/env python
# Author: Ariel Anders
# Domain classes for beerbots

from BeerBotDomain import AGENTS, ACTIONS, LOC, ORDERS, HOLD, PR2
from cleaner_waiter import Waiter
from Controller import Agent, Controller



class TurtleAgent(Agent):
    def __init__(self, name):
        self.turtle_ctrl = Waiter(name)
        self.num = name == "leonardo"
    
    def get_observation(self):
        print "getting an observation"
        return [0,0,0,0]

    def do_action(self, action):

        if action == ACTIONS.ROOM_1:
            self.turtle_ctrl.goToRoom1()

        elif action == ACTIONS.ROOM_2:
            self.turtle_ctrl.goToRoom2()

        elif action == ACTIONS.ROOM_3:
            self.turtle_ctrl.goToRoom3()

        elif action == ACTIONS.KITCHEN:
            self.turtle_ctrl.goToKitchen()

        elif action == ACTIONS.GET_DRINK:
            self.turtle_ctrl.waitAndGetDrink()
        
        ###XXX gabe add this function to cleaner_waiter
        """ 
        def waitAndGetDrink(self):
            self.wait_until_msg_is("pr2 ready to place can")
            self.send_msg_to_pr2("can i come")
            self.wait_until_msg_is("come " + self.name)
            self.approach()
            self.getDrink()
        """   
