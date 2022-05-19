#!/usr/bin/env python
# -*- coding: utf-8 -*-

import rospy
from std_msgs.msg import String


def talker():
    pub = rospy.Publisher('chatter_search', String, queue_size=10)
    rospy.init_node('search', anonymous=False)
    r = rospy.Rate(10) # 10hz
    for i in range(10):
        str = "hello world %s"%rospy.get_time()
        #rospy.loginfo(str)
        pub.publish(str)
        r.sleep()

if __name__ == '__main__':
    try:
        talker()
    except rospy.ROSInterruptException: pass