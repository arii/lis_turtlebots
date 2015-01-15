#!/usr/bin/env python

#import roslib
import rospy
from geometry_msgs.msg import Twist
from move_base_msgs.msg import MoveBaseGoal
from move_base_msgs.msg import MoveBaseAction
from move_base_msgs.msg import MoveBaseActionResult
#import sys, select, termios, tty
import time
import math
import actionlib
#import tf
from basic_turtlebot import *
from turtlebot_with_ar import *
from point import *

class Navigator(TurtlebotWithAR):
    def __init__(self, debug = True, default_velocity = 0.3, default_angular_velocity = 0.75):
        TurtlebotWithAR.__init__(self, debug, default_velocity, default_angular_velocity)
        if (not debug):
            self.nav = actionlib.SimpleActionClient("move_base", MoveBaseAction)
            self.nav.wait_for_server()
            self.goal = MoveBaseGoal()
            rospy.Subscriber('/move_base/result', MoveBaseActionResult, self.goalResult)
        self.going_to_goal = False
        

    # Go to the specified pose and wait until the turtlebot reaches it
    def goToPose(self, position, orientation, frame = "map"):
        if (self.debug):
            raw_input("Hit enter to go to pose (" + str(position) + "," + str(orientation) + ")...")
            return
        
        self.publishGoal(position, orientation, frame)
        return self.waitToReachGoal()
    
    # Go to the specified pose without waiting for the turtlebot to reach it. Useful for waypoint navigation
    def publishGoal(self, position, orientation, frame = "map"):
        if (self.debug):
            rospy.loginfo("Hit enter to publish the goal of (" + str(position) + "," + str(orientation) + ")...")
            return
    
        self.going_to_goal = True
        self.goal.target_pose.header.frame_id = frame
        self.goal.target_pose.header.stamp.secs = rospy.get_time()

        self.goal.target_pose.pose.position.x = position.x; self.goal.target_pose.pose.position.y = position.y
        self.goal.target_pose.pose.orientation.z = orientation.z; self.goal.target_pose.pose.orientation.w = orientation.w
        self.nav.send_goal(self.goal)
        self.nav.wait_for_result(rospy.Duration.from_sec(5.0)) # Does this line do anything?

    # Wait until the goal is reached
    def waitToReachGoal(self):
        while (self.going_to_goal):
            rospy.sleep(1)
        return True

    # Listens to the "/move_base/result" topic to determine when the goal is reached
    def goalResult(self, MoveBaseActionResult):
        self.going_to_goal = False
        #if (MoveBaseActionResult.status.status == 3):
        #    self.going_to_goal = False


if __name__=="__main__":
    rospy.init_node('navigator')

    navigator = Navigator()

    while (True):
        command = raw_input("Enter command: ")
        if (command == "move"):
            distance = float(raw_input("Enter distance: "))
            velocity = raw_input("Enter velocity: ")
            if (velocity == ""):
                navigator.move(distance)
            else:
                navigator.move(distance, float(velocity))
        elif (command == "turn"):
            angle = float(raw_input("Enter angle: "))
            angular_velocity = raw_input("Enter angular velocity: ")
            if (angular_velocity == ""):
                navigator.turn(angle)
            else:
                navigator.turn(angle, float(angular_velocity))
        elif (command == "stop"):
            stop_time = raw_input("Enter stop time: ")
            if (stop_time == ""):
                navigator.stop()
            else:
                navigator.stop(float(stop_time))
        elif (command == "approach"):
            navigator.approach()
        elif (command == "navigate"):
            (x, y) = [float(coordinate) for coordinate in raw_input("Enter goal position (as x,y): ").split(",")]
            (z, w) = [float(coordinate) for coordinate in raw_input("Enter goal orientation (as z,w): ").split(",")]
            navigator.goToPose(Point(x, y), (z, w))
        elif (command == "show_variables"):
            print "Default velocity =", navigator.default_velocity
            print "Default angular velocity =", navigator.default_angular_velocity
            print "going_to_goal =", navigator.going_to_goal
        elif (command == "end"):
            break


