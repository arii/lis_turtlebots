#!/usr/bin/env python

import rospy
from std_msgs.msg import String

class Listener:
    def __init__(self, name):
        self.name = name
        rospy.init_node("listener_"+name, anonymous=True)
        rospy.Subscriber("chatter_"+name, String, self.callback)
        rospy.spin()

    def callback(self, data):
        rospy.loginfo(rospy.get_caller_id()+"I heard %s",data.data)
    
def listener():

    # in ROS, nodes are unique named. If two nodes with the same
    # node are launched, the previous one is kicked off. The 
    # anonymous=True flag means that rospy will choose a unique
    # name for our 'listener' node so that multiple listeners can
    # run simultaenously.
    rospy.init_node('listener', anonymous=True)

    rospy.Subscriber("chatter", String, callback)

    # spin() simply keeps python from exiting until this node is stopped
    rospy.spin()
        
if __name__ == '__main__':
    #listener()
    name = raw_input("Enter name: ")
    listen = Listener(name)
