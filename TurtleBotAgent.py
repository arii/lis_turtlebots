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

    def do_action(self, action):

        if action == ACTIONS.ROOM_1:
            obs = self.turtle_ctrl.goToRoom1()

        elif action == ACTIONS.ROOM_2:
            obs = self.turtle_ctrl.goToRoom2()

        elif action == ACTIONS.ROOM_3:
            obs = self.turtle_ctrl.goToRoom3()

        elif action == ACTIONS.KITCHEN:
            obs = self.turtle_ctrl.goToKitchen()

        elif action == ACTIONS.GET_DRINK:
            obs = self.turtle_ctrl.waitAndGetDrink()
        else:
            print "incorrect action selected: %s " % action
            raise Exception
        return obs

        ###XXX gabe add this function to cleaner_waiter
        """ 
        def waitAndGetDrink(self):
            self.wait_until_msg_is("pr2 ready to place can")
            self.send_msg_to_pr2("can i come")
            self.wait_until_msg_is("come " + self.name)
            self.approach()
            self.getDrink()
        """   
