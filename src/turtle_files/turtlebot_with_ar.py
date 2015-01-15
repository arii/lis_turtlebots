#!/usr/bin/env python

from ar_track_alvar.msg import AlvarMarkers
from basic_turtlebot import *

class TurtlebotWithAR(Turtlebot):
    def __init__(self, debug = False, default_velocity = 0.3, default_angular_velocity = 0.75):
        Turtlebot.__init__(self, debug, default_velocity, default_angular_velocity)
        self.obj_x = 10.0; self.obj_y = 10.0; self.obj_theta = 0.0
        if (not self.debug):
            rospy.Subscriber('/ar_pose_marker', AlvarMarkers, self.objectPose)
        

    # Gets the pose of the object relative to the robot (through the AR tags)
    def objectPose(self, AlvarMarkers):
        if (len(AlvarMarkers.markers) > 0):
            self.obj_y = AlvarMarkers.markers[0].pose.pose.position.y
            self.obj_x = AlvarMarkers.markers[0].pose.pose.position.x
            orientation = Orientation(AlvarMarkers.markers[0].pose.pose.orientation.z, AlvarMarkers.markers[0].pose.pose.orientation.w)
            self.obj_theta = orientation.getTheta()

    # Face the object (obj_y ~= 0)
    def face(self, error = 0.1):
        self.obj_y = 10.0
        w = 0.4
        start_t = time.time()
        TIME_TO_FAIL = 60 # Check this later, it shouldn't need to be this big
        while (abs(self.obj_y) > abs(error)):
            t = time.time()
            while (abs(self.obj_y) > abs(error)):
                if (time.time() - start_t > TIME_TO_FAIL):
                    return "box_not_found"
                if (abs(self.obj_y) < 0.95):
                    start_t = time.time()
                if (time.time() - t > 6 and abs(self.obj_y) > 0.3):
                    self.setVelocity(0, 0)
                    time.sleep(1.5)
                    t = time.time()
                self.setVelocity(0, math.copysign(max(min(abs(self.obj_y), w), 0.2), self.obj_y))
            self.setVelocity(0, 0)
            self.obj_y = math.copysign(10.0, self.obj_y)
            time.sleep(2)
        return "obj_found"

    # Move until turtlebot is "desired_distance" meters away from the AR tag
    def approach(self, desired_distance = 0.45):
        distance = math.sqrt(self.obj_x**2 + self.obj_y**2)
        t = time.time()
        while (distance > desired_distance):
            if (abs(self.obj_y) > 0.25):
                self.face(0.1)
                t = time.time()
            print distance
            v = min(0.3, max(distance, 0.15))
            self.setVelocity(v, 0)
            time.sleep(0.3)
            distance = math.sqrt(self.obj_x**2 + self.obj_y**2)
        print distance
        self.setVelocity(0, 0)





