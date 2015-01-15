#!/usr/bin/env python

import rospy
from std_msgs.msg import String
from move_base_msgs.msg import MoveBaseActionResult
from move_base_msgs.msg import MoveBaseGoal
from move_base_msgs.msg import MoveBaseAction
from move_base_msgs.msg import MoveBaseActionResult
from geometry_msgs.msg import Twist
from ar_track_alvar.msg import AlvarMarkers
from geometry_msgs.msg import PoseWithCovarianceStamped
import actionlib
import math
import time
import random
import numpy
#from turtlebot_2turtles_communication import *
from SimpleServer import *
from multinavigator import *


class TimingsListener(object):
    timings = {"donatello" : {("room1", "room2") : [], ("room1", "room3") : [], ("room1", "kitchen") : [], ("room2", "room1") : [], ("room2", "room3") : [], ("room2", "kitchen") : [], ("room3", "room1") : [], ("room3", "room2") : [], ("room3", "kitchen") : [], ("kitchen", "room1") : [], ("kitchen", "room2") : [], ("kitchen", "room3") : [], ("kitchen", "after_pr2") : [], ("after_pr2", "room1") : [], ("after_pr2", "room2") : [], ("after_pr2", "room3") : []}, "leonardo" : {("room1", "room2") : [], ("room1", "room3") : [], ("room1", "kitchen") : [], ("room2", "room1") : [], ("room2", "room3") : [], ("room2", "kitchen") : [], ("room3", "room1") : [], ("room3", "room2") : [], ("room3", "kitchen") : [], ("kitchen", "room1") : [], ("kitchen", "room2") : [], ("kitchen", "room3") : [], ("kitchen", "after_pr2") : [], ("after_pr2", "room1") : [], ("after_pr2", "room2") : [], ("after_pr2", "room3") : []}}
    timings_ports = {"donatello" : 12352, "leonardo" : 12353}
    timings_hosts = {"donatello" : "10.68.0.171", "leonardo" : "10.68.0.175"}
    
    def __init__(self):
        self.debug = True
    
        self.listener = {}
        
        self.stop = False
        
        for name in self.timings_ports.keys():
            if (self.debug):
                self.listener[name] = SimpleClient(host = "localhost", port = self.timings_ports[name])
            else:
                self.listener[name] = SimpleClient(host = self.timings_hosts[name], port = self.timings_ports[name])
            t = Thread(target = self.listen, args = [name])
            t.start()
            
        self.loop()
            
    
    def listen(self, name):
        while (not self.stop):
            (loc0, loc1, delta_t) = self.listener[name].get_message().split(",")
            self.timings[name][(loc0, loc1)].append(float(delta_t))
    
    
    def loop(self):
        while (not self.stop):
            command = raw_input("Type 'end' to stop, 'all' to display all the stats, 'summary' for the avg and std, or 'loc0,loc1' to show the stats for 'loc0,loc1'...")
            if (command == "end"):
                self.stop = True
            elif (command == "all"):
                combined_timings = {}
                for key in self.timings["donatello"].keys():
                    combined_timings[key] = self.timings["donatello"][key] + self.timings["leonardo"][key]
                average = {key : numpy.average(combined_timings[key]) for key in combined_timings.keys()}
                std = {key : numpy.std(combined_timings[key]) for key in combined_timings.keys()}
                for key in combined_timings.keys():
                    print str(key) + " -> average = " + str(average[key]) + ", std = " + str(std[key]) + ", timings = " + str(combined_timings[key])
            elif (command == "summary"):
                combined_timings = {}
                for key in self.timings["donatello"].keys():
                    combined_timings[key] = self.timings["donatello"][key] + self.timings["leonardo"][key]
                average = {key : numpy.average(combined_timings[key]) for key in combined_timings.keys()}
                std = {key : numpy.std(combined_timings[key]) for key in combined_timings.keys()}
                for key in combined_timings.keys():
                    print str(key) + " -> average = " + str(average[key]) + ", std = " + str(std[key])
            else:
                combined_timings = {}
                for key in self.timings["donatello"].keys():
                    combined_timings[key] = self.timings["donatello"][key] + self.timings["leonardo"][key]
                average = {key : numpy.average(combined_timings[key]) for key in combined_timings.keys()}
                std = {key : numpy.std(combined_timings[key]) for key in combined_timings.keys()}
                try:
                    key = tuple(command.split(","))
                    print str(key) + " -> average = " + str(average[key]) + ", std = " + str(std[key]) + ", timings = " + str(combined_timings[key])
                except:
                    print "ILLEGAL COMMAND!!"
    
    
    
    
    
if __name__=="__main__":
    timings_listener = TimingsListener()
    
    
    
    
    
