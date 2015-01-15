#!/usr/bin/env python

import rospy
from std_msgs.msg import String

class Talker:
    def __init__(self, name):
        self.name = name
        self.pub = rospy.Publisher('chatter_'+name, String)
        rospy.init_node('talker_'+name, anonymous=True)
        self.r = rospy.Rate(10) # 10hz
        self.talker()
    
    def talker(self):
        #pub = rospy.Publisher('chatter', String)
        #rospy.init_node('talker', anonymous=True)
        #r = rospy.Rate(10) # 10hz
        while not rospy.is_shutdown():
            str = self.name + " says: hello world %s"%rospy.get_time()
            rospy.loginfo(str)
            self.pub.publish(str)
            self.r.sleep()

if __name__ == '__main__':
    name = raw_input("Enter name: ")
    try:
        #talker()
        talk = Talker(name)
    except rospy.ROSInterruptException: pass
