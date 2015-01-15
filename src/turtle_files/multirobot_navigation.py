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

robotPos = [0, 0, 0]

if __name__ == "__main__":
    rospy.init_node("multirobot_navigation")
    
    pub = rospy.Publisher('~cmd_vel', Twist)

    twist = Twist()

    #rospy.Subscriber('/ar_pose_marker', AlvarMarkers, objectPose)
    rospy.Subscriber('/amcl_pose', PoseWithCovarianceStamped, mapLocation)

    rospy.Subscriber('/move_base/result', MoveBaseActionResult, goalResult)
    
    #listener = SimpleClient()
    #sender = SimpleServer()


