import rospy
import roslib; roslib.load_manifest("pr2_awesomeness")

from SimpleServer import SimpleServer, SimpleClient
from argparse import ArgumentParser
import time
import random
import os
from threading import Thread

ARIEL =  True
if ARIEL:
  from pick_and_place import pick_and_place

class interface:
  START, PICKING, WAITING_TO_PLACE, PLACING= range(4)
  def __init__(self, init_state=None, debug=False):
      self.server  = SimpleServer(port=12345, threading=True)
      if  True or ARIEL:
          host_D="10.68.0.171"
          host_L="10.68.0.175"
      else:
          host_D = "localhost"
          host_L = "localhost"
      self.clientD = SimpleClient(host=host_D,port=12346) # D for Donatello
      self.clientL = SimpleClient(host=host_L,port=12347) # L for Leonardo
      self.turtle_being_attended = None

      if ARIEL:
          self.awesome = pick_and_place()
      
      if init_state == None:
          self.state = self.START
      else:
          self.state = init_state

      self.event_loop()
  
  def event_loop(self):
      while True:
          #rospy.loginfo("starting event loop!  current state = %d" % self.state)

          if self.state == self.START:
              if not ARIEL:
                  pass
              #raw_input("Hit enter to start...")
              self.send_msg_to_turtle("not_serving: picking")
              self.t = Thread (target = self.pick_up)
              self.t.start()
              self.wait_until_msg_is("can i come", "generic_turtle")
              self.server.update_broadcast("serving_turtlebot: %s "\
                    % self.turtle_being_attended)
              
          if self.state == self.WAITING_TO_PLACE:
              #raw_input("waiting to place")
              self.send_msg_to_turtle("serving_turtlebot: come "\
                    + self.turtle_being_attended)
              rospy.loginfo("Waiting for " + self.turtle_being_attended)
              self.wait_until_msg_is("turtle in place position", \
                    self.turtle_being_attended)
              self.state = self.PLACING
          
          if self.state == self.PLACING:
              #raw_input("placing")
              self.send_msg_to_turtle("serving_turtlebot: placing")
              self.place()
              self.send_msg_to_turtle("serving_turtlebot: pr2 placed object")
              #raw_input("placed object on %s " % self.turtle_being_attended)
              self.wait_until_msg_is("turtle left pr2",\
                    self.turtle_being_attended)
              self.turtle_being_attended = None
              self.state = self.START

              
  def wait_until_msg_is(self,correct_msg, name="turtle"):
      rospy.loginfo("waiting to receive following msg from turtle: %s"\
      % correct_msg)
      msg = self.receive_msg_from(name)
      while msg != correct_msg:
          msg = self.receive_msg_from(name)
      info =  "message received is %s from %s" \
            % (msg, self.turtle_being_attended)
      self.robot_speak(info)
      
  def send_msg_to_turtle(self, msg):
      rospy.loginfo( "sending message: %s " % msg)
      self.server.update_broadcast(msg)
      self.robot_speak("sending message: %s " % msg)

  def robot_speak(self, text):
      if ARIEL:
          os.system("rosrun sound_play say.py '%s'&" % text)
      else:
          rospy.loginfo(text)

  def receive_msg_from(self, name):
      msg_received = False
      msg = None
      while not msg_received:
          try:
              if (name == "donatello"):
                  msg = self.clientD.get_message()
              elif (name == "leonardo"):
                  msg = self.clientL.get_message()
              else:
                  msgD = None; msgL = None
                  try:
                      msgD = self.clientD.get_message()
                  except: pass
                  try:
                      msgL = self.clientL.get_message()
                  except:pass
                  if msgD != None and msgL != None:
                      msg = msgL if random.randint(0,1) else msgD
                  elif msgL != None:
                      msg = msgL
                  elif msgD != None:
                      msg = msgD
                  else:
                      rospy.sleep(1)
                      continue #no messages received
              self.turtle_being_attended, msg = msg.split(",")
              msg_received = True
          except: pass
      return msg

  def pick_up(self):
      rospy.loginfo("picking up object")
      print "STARTING PLACING"
      self.state = self.PICKING
      if ARIEL:
          result = False
          while not result:
              result = self.awesome.pick_up()
      else:
          rospy.sleep(1) # dummy action
      if self.turtle_being_attended  != None:
          self.send_msg_to_turtle("not_serving: waiting_for_turtlebot")
      print "COMPLETED PLACING"
      self.state = self.WAITING_TO_PLACE


  def place(self):
      rospy.loginfo("placing can")
      if ARIEL:
          result = False
          while not result:
                result = self.awesome.place()
                if not result:
                    rospy.loginfo("place result failed!")
                    rospy.sleep(1) # dummy action

      else:
          rospy.sleep(1) # dummy action

def awesome_parse_arguments():
    parser = ArgumentParser("Select initial state")
    parser.add_argument("--wait", action="store_true",
        help="wait for msg then place")
    parser.add_argument("--place", action="store_true",
        help="in place position")

    args = parser.parse_args()
    init_state = 0
    if args.wait:
        init_state=  2
    if args.place:
        init_state = 3
    return init_state
if __name__=="__main__":
  rospy.init_node("pr2_communication")
  init_state = awesome_parse_arguments()
  interface(init_state)


