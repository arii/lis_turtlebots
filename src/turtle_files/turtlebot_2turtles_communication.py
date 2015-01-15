#!/usr/bin/env python

import rospy
from SimpleServer import SimpleServer, SimpleClient
from argparse import ArgumentParser
import time
from waiters import *
from basic_turtlebot import *

class interface:
  GOING_TO_KITCHEN, WAITING_FOR_PR2, APPROACHING_PR2, WAITING_FOR_DRINK= range(4)
  def __init__(self, name, init_state=None, debug=False):
      self.name = name
      
      waiter_port = {"donatello" : 12346, "leonardo" : 12347}
      
      self.server = SimpleServer(waiter_port[name], threading=True)
      self.client = SimpleClient(host="localhost",port=12345) #10.68.0.171 #pr2mm1.csail.mit.edu
      
      if init_state == None:
          self.state = self.START
      else: 
          self.state = init_state

      self.event_loop()
      
  def event_loop(self):
      raw_input("Hit enter to start...")
      while True:
          rospy.loginfo("starting event loop!  current state = %d" % self.state)

          if self.state == self.GOING_TO_KITCHEN:
              #raw_input("Hit enter to go to the kitchen...")
              self.go_to_kitchen()
              #goToKitchen()
              self.state = self.WAITING_FOR_PR2
          
          if self.state == self.WAITING_FOR_PR2:
              self.wait_until_msg_is("pr2 ready to place can")
              self.send_msg_to_pr2("can i come")
              self.wait_until_msg_is("come " + self.name)
              self.state = self.APPROACHING_PR2
          
          if self.state == self.APPROACHING_PR2:
              raw_input("Hit enter to approach the PR2...")
              self.approach()
              #approach()
              self.send_msg_to_pr2("turtle in place position")
              self.state = self.WAITING_FOR_DRINK

          if self.state == self.WAITING_FOR_DRINK:
              self.wait_until_msg_is("pr2 placed object")
              time.sleep(1)
              #move(0.5, 0.25)
              #raw_input("Hit enter to leave the PR2...")
              self.send_msg_to_pr2("turtle left pr2")
              self.state = self.GOING_TO_KITCHEN

  def wait_until_msg_is(self,correct_msg):
      rospy.loginfo("waiting to receive following msg from PR2: %s"\
      % correct_msg)
      msg = self.receive_msg_from_pr2()
      while msg != correct_msg:
          msg = self.receive_msg_from_pr2()
              
  def send_msg_to_pr2(self, msg):
      rospy.loginfo( "sending message: %s " % msg)
      self.server.update_broadcast(self.name + "," + msg)
      rospy.loginfo( "message sent: %s " % msg)
  
  def receive_msg_from_pr2(self):
      msg_received = False
      while not msg_received:
          try:
              msg = self.client.get_message()
              msg_received = True
              #rospy.loginfo("message received is: %s " % msg)
          except:
              rospy.sleep(1)
      return msg

  def go_to_kitchen(self):
      rospy.loginfo("going to kitchen")
      rospy.sleep(1) # dummy action 

  def approach(self):
      rospy.loginfo("approaching PR2")
      rospy.sleep(1) # dummy action

def awesome_parse_arguments():
    parser = ArgumentParser("Select initial state")
    parser.add_argument("--waiting", action="store_true",
        help="wait for msg then approach PR2")
    parser.add_argument("--ready", action="store_true",
        help="in place position")

    args = parser.parse_args()
    init_state = 0
    if args.waiting:
        init_state=  1
    if args.ready:
        init_state = 3
    return init_state
if __name__=="__main__":
  rospy.init_node("turtlebot_2turtles_communication")
  init_state = awesome_parse_arguments()
  name = raw_input("Enter turtlebot's name: ")
  interface(name, init_state)


