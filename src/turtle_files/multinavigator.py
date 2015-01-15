#!/usr/bin/env python

from threading import Thread
from geometry_msgs.msg import PoseWithCovarianceStamped
from SimpleServer import SimpleServer, SimpleClient
from navigator import *
from point import *
from orientation import *
import time

class MultiNavigator(Navigator):
    request_ports = {"donatello" : 12348, "leonardo" : 12349}
    response_ports = {"donatello" : 12350, "leonardo" : 12351}
    waypoints_host = "10.68.0.171" #"10.68.0.165" #"localhost" #"10.68.0.171"
    DISTANCE_TOLERANCE = 0.55 # When the robot is within this distance of a waypoint, we publish a new goal (to make the path smoother)
    
    def __init__(self, name, debug = True, default_velocity = 0.3, default_angular_velocity = 0.75):
        Navigator.__init__(self, debug, default_velocity, default_angular_velocity)
        self.name = name
        self.position = Point(0, 0)
        self.angle = 0
        self.last_reserved_location = None
        self.multiagent = False
        
        if (self.multiagent):
            # Create request server and response clients to communicate with waypoints_server
            self.waypoint_request = SimpleServer(port = self.request_ports[name], threading = False)
            self.waypoint_response = SimpleClient(host = self.waypoints_host, port = self.response_ports[name])
        
        # Subscribe to /amcl_pose topic to use to cancel the waypoints goals when the robot is close enough to avoid
        # spending time getting the orientation and position perfectly (we only care about passing close to the waypoint)
        if (not debug):
            rospy.Subscriber('/amcl_pose', PoseWithCovarianceStamped, self.robotPose)
        
    # Navigate to a goal location passing through a list of waypoints, always waiting until the next waypoint to be free
    def wayposeNavigation(self, wayposes):
        for (point, orientation) in wayposes[:-1]:
            self.reserveWaypoint(point)
            self.publishGoal(point, orientation)
            #raw_input("Go to " + str(point) + "...")
            self.waitUntilCloseToGoal(point)
            self.releaseWaypoint(self.last_reserved_location)
            self.last_reserved_location = point
        self.goToPose(wayposes[-1][0], wayposes[-1][1])
        
    # Send message to the waypoints server to reserve next waypoint. Called right before publishing that waypoint as the next navigation goal.
    def reserveWaypoint(self, point):j
        if (not self.multiagent):
            return
        print "Reserving waypoint " + str(point)
        self.waypoint_request.broadcast("reserve," + str(point.x) + "," + str(point.y))
        #print "Waypoint server received reservation request"
        # The waypoints_server is only going to send an accept response. If the waypoint requested is already reserved, the server will wait until it's released to send a response.
        self.waypoint_response.get_message()
        print "Granted waypoint " + str(point)
        
    # Send message to the waypoints server to release previous waypoint. Called after the next waypoint is reached.
    def releaseWaypoint(self, point):
        if (not self.multiagent):
            return
        if (point != None):
            print "Releasing waypoint " + str(point)
            self.waypoint_request.broadcast("release," + str(point.x) + "," + str(point.y))
            print "Waypoint server received release request"
    
    # Wait until the robot's location is within self.DISTANCE_TOLERANCE of point. Used to cancel a waypoint
    # once the robot is close to it so that it doesn't lose time trying to get the specified orientation.
    def waitUntilCloseToGoal(self, point):
        if (self.debug):
            raw_input("Hit enter when the robot is close enough to " + str(point) + "...")
            return
            
        while (self.position.distance(point) > self.DISTANCE_TOLERANCE):
            time.sleep(0.3) #sleep for a little
    
    # Listen to the robot's pose in the "map" frame
    def robotPose(self, PoseWithCovarianceStamped):
        position = PoseWithCovarianceStamped.pose.pose.position
        (x, y) = (position.x, position.y)
        orientation = Orientation(PoseWithCovarianceStamped.pose.pose.orientation.z, PoseWithCovarianceStamped.pose.pose.orientation.w)
        self.position = Point(x, y)
        self.angle = orientation.getTheta()


if __name__=="__main__":
    name = raw_input("Enter name: ")
    multinavigator = MultiNavigator(name)
    while (True):
        command = raw_input("Enter command (reserve, release, end): ")
        if (command == "reserve"):
            (x, y) = [float(coord) for coord in raw_input("Enter point as x,y: ").split(",")]
            multinavigator.reserveWaypoint(Point(x, y))
        elif (command == "release"):
            (x, y) = [float(coord) for coord in raw_input("Enter point as x,y: ").split(",")]
            multinavigator.releaseWaypoint(Point(x, y))
    
        elif (command == "end"):
            break
    

