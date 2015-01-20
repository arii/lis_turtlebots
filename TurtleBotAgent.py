#!/usr/bin/env python
# Author: Ariel Anders
# Domain classes for beerbots

import rospy
import roslib
import sys
sys.path.append("../lis_turtlebots/src")
roslib.load_manifest('lis_turtlebots')
from BeerBotDomain import AGENTS, ACTIONS, LOC, ORDERS, HOLD, PR2
from cleaner_waiter import Waiter
from Controller import Agent, Controller



class TurtleAgent(Agent):
    def __init__(self, name):
        self.turtle_ctrl = Waiter(name)
        self.num = int(name == "leonardo")

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
            obs = self.turtle_ctrl.getDrink()
        else:
            print "incorrect action selected: %s " % action
            raise Exception
	print  "observation= ", obs
        return obs


if __name__=="__main__":
    from argparse import ArgumentParser
    parser = ArgumentParser("select which turtle to use.  default is Donatello")
    parser.add_argument("-d", "--donatello", action="store_true",\
            help="select donatello",dest="donatello")
    parser.add_argument("-l", "--leonardo", action="store_true",\
            help="select leonardo", dest="leonardo")
    
    args = parser.parse_args()
    if not (args.leonardo or args.donatello):
        name = "donatello"
    elif args.leonardo:
        name = "leonardo"
    else:
        name = "donatello"
    rospy.init_node("waiter_"+name)

    rospy.loginfo("starting waiter with turtle %s " % name)
    raw_input("hit enter to start") 
    agent = TurtleAgent(name)
    policy = "3node"
    
    ctrl = Controller(agent, policy)

    #initial obs in kitchen without drink or orders
    # initial obs 1 order and robot is in room 
    if name == "leonardo":
        obs = [3, 0,0,1]
    else:
        obs = [0,1,0,3]

    ctrl.run(0, obs, False)

    
    








