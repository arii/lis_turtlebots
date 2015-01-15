#!/usr/bin/env python

from threading import Thread
from geometry_msgs.msg import PoseWithCovarianceStamped
from SimpleServer import SimpleServer, SimpleClient
from navigator import *
from orientation import *

class MultiNavigator(Navigator):
    ports = {"donatello" : 12348, "leonardo" : 12349}
    hosts = {"donatello" : "10.68.0.171", "leonardo" : "10.68.0.175"}
    DISTANCE_TOLERANCE = 1.0
    def __init__(self, name, other_turtlebots, default_velocity = 0.3, default_angular_velocity = 0.75):
        Navigator.__init__(self, default_velocity, default_angular_velocity)
        self.name = name
        self.position = Point(0, 0)
        self.angle = 0
        
        # Subscribe to /amcl_pose topic and broadcast it to the other turtlebots (via SimpleServer)
        self.pose_publisher = SimpleServer(port = self.ports[name], threading = True)
        rospy.Subscriber('/amcl_pose', PoseWithCovarianceStamped, self.publishPose)
        
        # Create listeners for other turtlebot's pose
        self.pose_listener = {}
        for turtlebot in other_turtlebots:
            self.pose_listener[turtlebot] = SimpleClient(host = self.hosts[name], port = self.ports[name])
        self.t = Thread(target = self.listenToPose)
        self.t.start()

    def publishPose(self, PoseWithCovarianceStamped):
        position = PoseWithCovarianceStamped.pose.pose.position
        (x, y) = (position.x, position.y)
        orientation = Orientation(0, 0, PoseWithCovarianceStamped.pose.pose.orientation.w, PoseWithCovarianceStamped.pose.pose.orientation.z)
        self.position = Point(x, y)
        self.angle = orientation.getTheta()
        self.pose_publisher.update_broadcast(str(x) + "," + str(y) + "," + str(self.angle))

    def listenToPose(self):
        while (True):
            # Only applies when the turtlebot is navigating to a goal
            if (self.going_to_goal):
                close_to_other_turtlebots = False
                for turtlebot in pose_listener:
                    (x, y, theta) = self.pose_listener[turtlebot].get_message().split(",")
                    if (self.position.distance(Point(x, y)) < self.DISTANCE_TOLERANCE):
                        close_to_other_turtlebots = True
        
                if (close_to_other_turtlebots):
                    # Tell the turtlebot to stop, so that it can detect the other turtlebot and reroute around it
                    self.stop() # Defaults to stopping for 2 seconds
                    
                    # Give the turtlebot time to move (travel to the goal). Without this, the turtlebot wouldn't move at all.
                    time.sleep(10)



if __name__=="__main__":
    rospy.init_node('navigator')

    navigator = MultiNavigator("donatello", [])

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


