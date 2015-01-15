#!/usr/bin/env python

import time
import rospy
from std_msgs.msg import String
from move_base_msgs.msg import MoveBaseActionResult
from move_base_msgs.msg import MoveBaseGoal
from move_base_msgs.msg import MoveBaseAction
from move_base_msgs.msg import MoveBaseActionResult
from SimpleServer import *
from geometry_msgs.msg import Twist
from ar_track_alvar.msg import AlvarMarkers
from geometry_msgs.msg import PoseWithCovarianceStamped
import actionlib
import math
#from turtlebot_2turtles_communication import *
from basic_turtlebot import *


NAME = "DONATELLO"

OFFICE1_POSITION = {"DONATELLO" : (0, 0), "LEONARDO" : (0, 0)}
OFFICE1_ORIENTATION = {"DONATELLO" : (0, 1), "LEONARDO" : (0, 1)}

OFFICE2_POSITION = {"DONATELLO" : (0, 0), "LEONARDO" : (0, 0)}
OFFICE2_ORIENTATION = {"DONATELLO" : (0, 1), "LEONARDO" : (0, 1)}

KITCHEN_POSITION = {"DONATELLO" : (1.79, -0.57), "LEONARDO" : (1.25, -1.03)}
KITCHEN_ORIENTATION = {"DONATELLO" : (0.9, 0.44), "LEONARDO" : (0.78, 0.63)}

PR2_POSITION = {"DONATELLO" : (0.83, 0.44), "LEONARDO" : (0, 0)}
PR2_ORIENTATION = {"DONATELLO" : (-0.63, 0.77), "LEONARDO" : (0, 1)}

order = None
waiting_for_order = False
waiting_for_pr2_response = True
waiting_for_drink = True
goal_reached = False


################################################################################################################

# Gets the pose of the object relative to the robot (through the AR tags)
def objectPose(AlvarMarkers):
    global obj_x, obj_y, obj_theta
    if (len(AlvarMarkers.markers) > 0):
        obj_y = AlvarMarkers.markers[0].pose.pose.position.y
        obj_x = AlvarMarkers.markers[0].pose.pose.position.x
        obj_theta = getTheta(AlvarMarkers.markers[0].pose.pose.orientation.w, AlvarMarkers.markers[0].pose.pose.orientation.z)
        #print "y = ", obj_y, ", theta = ", obj_theta / math.pi, "*pi"




def mapLocation(PoseWithCovarianceStamped):
    global robotPos # [x, y, theta]
    robotPos[0] = PoseWithCovarianceStamped.pose.pose.position.x
    robotPos[1] = PoseWithCovarianceStamped.pose.pose.position.y
    robotPos[2] = (getTheta(PoseWithCovarianceStamped.pose.pose.orientation.w, PoseWithCovarianceStamped.pose.pose.orientation.z) + 2*math.pi) % (2*math.pi)



def goalResult(MoveBaseActionResult):
    global goal_reached
    print MoveBaseActionResult.status.status
    goal_reached = True



# Goes to a point that lies on the same line as the object and the goal
# INITIAL CONDITIONS: The robot is close to the object (within ~1.50 meters of it)
# GOAL: The robot, object, and goal all lie on the same line
def getPR2Location():
    global robotPos
    (rx, ry, alpha) = robotPos
    pr2_base = [rx + obj_x*math.cos(alpha) - obj_y*math.sin(alpha), ry + obj_x*math.sin(alpha) + obj_y*math.cos(alpha)]
    turtle_to_pr2_vector = [pr2_base[0] - robotPos[0], pr2_base[1] - robotPos[1]]
    distance = math.sqrt(turtle_to_pr2_vector[0]**2 + turtle_to_pr2_vector[1]**2)
    turtle_to_pr2_vector = [t / distance for t in turtle_to_pr2_vector]
    
    k = 0.5
    loc = [pr2_base[i] - turtle_to_pr2_vector[i] for i in range(2)]

    return pr2_base

def approach():
    distance = math.sqrt(obj_x**2 + obj_y**2)
    t = time.time()
    while (distance > 0.4):
        if (abs(obj_y) > 0.25):
            face(0.1)
            t = time.time()
        print distance
        v = min(0.3, max(distance, 0.15))
        twist.linear.x = v; twist.linear.y = 0; twist.linear.z = 0
        twist.angular.x = 0; twist.angular.y = 0; twist.angular.z = 0
        pub.publish(twist)
        time.sleep(0.3)
        distance = math.sqrt(obj_x**2 + obj_y**2)
    print distance
    twist.linear.x = 0; twist.linear.y = 0; twist.linear.z = 0
    twist.angular.x = 0; twist.angular.y = 0; twist.angular.z = 0
    pub.publish(twist)
    time.sleep(0.5)
    turn(1.5 * math.pi)



# Face the object
# INITIAL CONDITIONS: Robot is close to the object
# GOAL: The robot faces the object and the robot, object, and goal all lie on the same line (the robot can just move straight
# forward and it'll hit the object and eventually the goal)
def face(error):
    global obj_y
    obj_y = 10.0
    #print "STARTED FACE" ###------------------------------------------------------------------------------------------------###
    CENTER = 0.0
    w = 0.4
    start_t = time.time()
    TIME_TO_FAIL = 60 # Check this later, it shouldn't need to be this big
    while (obj_y < CENTER - error or obj_y > CENTER + error):
        t = time.time()
        while (obj_y < CENTER - error or obj_y > CENTER + error):
            if (time.time() - start_t > TIME_TO_FAIL):
                return "box_not_found"
            if (abs(obj_y) < 0.95):
                start_t = time.time()
            if (time.time() - t > 6 and abs(obj_y) > 0.3):
                twist.linear.x = 0; twist.linear.y = 0; twist.linear.z = 0
                twist.angular.x = 0; twist.angular.y = 0; twist.angular.z = 0
                pub.publish(twist)
                time.sleep(1.5)
                t = time.time()
            twist.linear.x = 0; twist.linear.y = 0; twist.linear.z = 0
            twist.angular.x = 0; twist.angular.y = 0; twist.angular.z = math.copysign(max(min(abs(obj_y), w), 0.2), obj_y)
            pub.publish(twist)
        twist.linear.x = 0; twist.linear.y = 0; twist.linear.z = 0
        twist.angular.x = 0; twist.angular.y = 0; twist.angular.z = 0
        pub.publish(twist)
        obj_y = math.copysign(10.0, obj_y)
        time.sleep(2)
    return "box_found"


# Turns the turtlebot alpha radians
def turn(alpha):
    ERROR_TIME = 0.0 # This is needed because it'll take some time for the robot to accelerate. The ideal time will be determined experimentally (it might depend on alpha).
    w = 0.75
    t = time.time()
    while (time.time() - t < abs(alpha) / w + ERROR_TIME):
        twist.linear.x = 0; twist.linear.y = 0; twist.linear.z = 0
        twist.angular.x = 0; twist.angular.y = 0; twist.angular.z = math.copysign(w, alpha)
        pub.publish(twist)
    twist.linear.x = 0; twist.linear.y = 0; twist.linear.z = 0
    twist.angular.x = 0; twist.angular.y = 0; twist.angular.z = 0
    pub.publish(twist)


def move(distance, velocity):
    t = time.time()
    while (time.time() - t < distance / float(velocity)):
        twist.linear.x = velocity; twist.linear.y = 0; twist.linear.z = 0
        twist.angular.x = 0; twist.angular.y = 0; twist.angular.z = 0
        pub.publish(twist)
    twist.linear.x = 0; twist.linear.y = 0; twist.linear.z = 0
    twist.angular.x = 0; twist.angular.y = 0; twist.angular.z = 0
    pub.publish(twist)


# Gets the yaw angle from the quaternion describing the object's position
def getTheta(w, z):
    mag = math.sqrt(w ** 2 + z ** 2)
    w /= mag
    z /= mag
    return math.atan2(2 * w * z, w ** 2 - z ** 2) #- math.pi / 2



################################################################################################################



###################################################################################################
########################################## MACRO ACTIONS ##########################################
###################################################################################################

def goToOffice1():
    global waiting_for_order
    goToPose("map", OFFICE1_POSITION[NAME], OFFICE1_ORIENTATION[NAME])
    waiting_for_order = True
    #waitForOrder()


def goToOffice2():
    global waiting_for_order
    goToPose("map", OFFICE2_POSITION[NAME], OFFICE2_ORIENTATION[NAME])
    waiting_for_order = True
    #waitForOrder()


# This could be absorbed into the goToOffice macroactions
def waitForOrder():
    while (waiting_for_order):
        time.sleep(1)


def goToKitchen():
    global waiting_for_pr2_response, goal_reached
    goal_reached = False
    goToPose("map", KITCHEN_POSITION[NAME], KITCHEN_ORIENTATION[NAME])
    while (not goal_reached):
        time.sleep(1)
    waiting_for_pr2_response = True
    #sendOrderToPR2


# This could be absorbed into the goToKitchen macroaction
def sendOrderToPR2():
    sender = rospy.Publisher("order", String)
    rospy.init_node("waiter_"+NAME, anonymous=True)
    r = rospy.Rate(10) # 10 Hz
    while not rospy.is_shutdown():
        msg = NAME + str(rospy.get_time())
        sender.publish(msg)
        r.sleep()
    #waitForPR2Response()
    


# This could be absorbed into the sendOrderToPR2 macroaction
def waitForPR2Response():
    global waiting_for_pr2_response
    t = time.time()
    try_or_except = "try"
    while (waiting_for_pr2_response):
        if (time.time() - t) > 10:
            t = time.time()
            print try_or_except
        try:
            msg = listener.get_message()
            print msg 
            if (msg == "pr2 ready to place can"):
                print "PR2 ready"
                waiting_for_pr2_response = False
            else:
                time.sleep(1)
            try_or_except = "try_" + msg
        except:
            try_or_except = "except"
            time.sleep(1)
    

def goToPR2():
    global waiting_for_drink
    pr2_loc = getPR2Location()
    print "Turtle's position = ", robotPos
    print "PR2's position = ", pr2_loc
    goToPose("map", pr2_loc, PR2_ORIENTATION[NAME])
    waiting_for_drink = True
    #waitForDrink


# This could be absorbed into the goToPR2 macroaction
def waitForDrink():
    global waiting_for_drink
    #msg = listener.get_message()
    #if (msg != None):
    #    print "I'm ready to receive drink"
    #else:
    #    print "SOMETHING'S WRONG!! Didn't receive message from PR2"
    t = time.time()
    try_or_except = "try"
    while (waiting_for_drink):
        if (time.time() - t) > 10:
            t = time.time()
            print try_or_except
        try:
            msg = listener.get_message()
            print msg
            if (msg == "pr2 placed object"):
                print "PR2 is done"
                waiting_for_drink = False
            else:
                time.sleep(1)
            try_or_except = "try_" + msg
        except:
            try_or_except = "except"
            time.sleep(1)




# Uses the navigation stack to move the robot to the specified pose
def goToPose(frame, position, orientation): #frame, [x, y], [z, w]
    goal.target_pose.header.frame_id = frame
    goal.target_pose.header.stamp.secs = rospy.get_time()

    goal.target_pose.pose.position.x = position[0]; goal.target_pose.pose.position.y = position[1]
    goal.target_pose.pose.orientation.z = orientation[0]; goal.target_pose.pose.orientation.w = orientation[1]
    #print "SENDING GOAL..." ###---------------------------------------------------------------------------------------------###
    nav.send_goal(goal)
    #print "DONE SENDING GOAL" ###-------------------------------------------------------------------------------------------###
    nav.wait_for_result(rospy.Duration.from_sec(5.0))


def wait_until_msg_is(correct_msg):
    rospy.loginfo("waiting to receive following msg from turtle: %s"\
    % correct_msg)
    msg = receive_msg_from_pr2()
    print "msg = ", msg
    while msg != correct_msg:
        msg = receive_msg_from_pr2()
        print "msg = ", msg
              
def send_msg_to_pr2(msg):
    rospy.loginfo( "sending message: %s " % msg)
    sender.broadcast(msg)
    rospy.loginfo( "message sent: %s " % msg)
  
def receive_msg_from_pr2():
    msg_received = False
    while not msg_received:
        try:
            msg = listener.get_message()
            msg_received = True
            rospy.loginfo("message received is: %s " % msg)
        except:
            rospy.sleep(2)
    return msg


############################################################

class interface:
  GOING_TO_KITCHEN, WAITING_FOR_PR2, APPROACHING_PR2, WAITING_FOR_DRINK= range(4)
  def __init__(self, name, init_state=None, debug=False):
      self.name = name
      if (name == "donatello"):
      	  self.server = SimpleServer(12346)
      else:
          self.server = SimpleServer(12347)
      self.client = SimpleClient(host="pr2mm1.csail.mit.edu",port=12345) #10.68.0.171 #pr2mm1.csail.mit.edu
      
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
              goToKitchen()
              self.state = self.WAITING_FOR_PR2
          
          if self.state == self.WAITING_FOR_PR2:
              self.wait_until_msg_is("pr2 ready to place can")
              self.send_msg_to_pr2("can i come")
              self.wait_until_msg_is("come " + self.name)
              self.state = self.APPROACHING_PR2
          
          if self.state == self.APPROACHING_PR2:
              #raw_input("Hit enter to approach the PR2...")
              #self.approach()
              approach()
              self.send_msg_to_pr2("turtle in place position")
              self.state = self.WAITING_FOR_DRINK

          if self.state == self.WAITING_FOR_DRINK:
              self.wait_until_msg_is("pr2 placed object")
              time.sleep(1)
              move(0.5, 0.25)
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




############################################################





obj_x = 10.0
obj_y = 10.0
obj_theta = 0.0

robotPos = [0, 0, 0]

leave = False
goal = MoveBaseGoal
twist = Twist()

if __name__ == "__main__":
    rospy.init_node("waiter")
    
    pub = rospy.Publisher('~cmd_vel', Twist)
    nav = actionlib.SimpleActionClient("move_base", MoveBaseAction)

    #print "WAITING FOR SERVER..." ###---------------------------------------------------------------------------------------###
    nav.wait_for_server()
    #print "DONE WAITING FOR SERVER" ###-------------------------------------------------------------------------------------###

    goal = MoveBaseGoal()
    twist = Twist()

    rospy.Subscriber('/ar_pose_marker', AlvarMarkers, objectPose)
    rospy.Subscriber('/amcl_pose', PoseWithCovarianceStamped, mapLocation)
    rospy.Subscriber('/move_base/result', MoveBaseActionResult, goalResult)
    
    #listener = SimpleClient()
    #sender = SimpleServer()

    #while (True):
    #    try:
    #        listener.get_message()
    #        break
    #    except:
    #        time.sleep(1)
    i = 0
    print "Starting..."
    
    #name = raw_input("Enter turtlebot's name: ")
    interface(NAME.lower(), 0)

"""
    while (True):
        goToKitchen()

        # This only happens if it's not the first time we go through the loop
        # Once we get away from the PR2, we want to tell it we left so that it can turn and grab another drink
        
        #if (leave):
            #send_msg_to_pr2("turtle left pr2")
            #time.sleep(5)
            #obj_x = 10.0
            #obj_y = 10.0
        

        # Wait until we see an AR tag to start listening to the PR2
        print "Waiting to see PR2's AR tag"        
        while (obj_x == 10.0):
            time.sleep(1)

        # Wait until the PR2 tells us that it is ready to place the drink
        print "Waiting for PR2's READY message"
        wait_until_msg_is("pr2 ready to place can")
        
        # Approach the PR2 so that it can place the drink on the turtlebot
        approach()

        # Once we're in the placement position, tell the PR2 that it can place the drink on the turtlebot
        send_msg_to_pr2("turtle in place position")

        # Wait for the PR2 to place the drink on the turtlebot        
        print "Waiting for drink"
        time.sleep(10)
        print "Waiting for PR2's DONE message"
        wait_until_msg_is("pr2 placed object")
        
        t = time.time()
        while ((time.time() - t) < 3):
            twist.linear.x = 0.25; twist.linear.y = 0; twist.linear.z = 0
            twist.angular.x = 0; twist.angular.y = 0; twist.angular.z = 0
            pub.publish(twist)
        twist.linear.x = 0; twist.linear.y = 0; twist.linear.z = 0
        twist.angular.x = 0; twist.angular.y = 0; twist.angular.z = 0
        pub.publish(twist)
        send_msg_to_pr2("turtle left pr2")

        #leave = True
        print "DONE!", i
        i += 1
        waiting_for_pr2_response = True
        waiting_for_drink = True
        obj_x = 10.0
        obj_y = 10.0

"""



