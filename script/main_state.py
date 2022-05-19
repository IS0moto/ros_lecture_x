#!/usr/bin/env python

import roslib
import rospy
import smach
import smach_ros
from subprocess import call, Popen
from std_msgs.msg import Int16
#import actionlib
#from move_base_msgs.msg import *

#define state recognition QR or sound
class Recognition(smach.State):
    def __init__(self):
        smach.State.__init__(self,outcomes=["success_Recognition"])

    def execute(self, userdata):
        rospy.loginfo("Start Recognition")
        call("rosrun ros_lecture_x_pkg recognition.py", shell=True)
        return "success_Recognition"

# define state Search target
class Search(smach.State):
    def __init__(self):
        smach.State.__init__(self, outcomes=["success_Search"])

    def execute(self, userdata):
        rospy.loginfo("Start Search")
        #Popen("rosrun competition_pkg follow.py", shell=True)
        call("rosrun ros_lecture_x_pkg search.py", shell=True)
        #rospy.sleep(30.0)
        #call("rosnode kill /search", shell=True)
        return "success_Search"

# define state Navigation to target
class Navigation(smach.State):
    def __init__(self):
        smach.State.__init__(self, outcomes=["success_Navigation","False_Navigation"])
        self.sub=rospy.Subscriber("FOO",Int16,self.callback)

    def callback(self,data):
        self.data=data.data
        #rospy.loginfo("%s",self.data)

    def execute(self, userdata):
        rospy.loginfo("Start Navigation")
        call("rosrun ros_lecture_x_pkg navigation.py", shell=True)
        if(self.data==1):
            return "success_Navigation"
        else:
            return "False_Navigation"


def main():
    rospy.init_node('sm_main')
    rospy.sleep(2.)
    raw_input("PLEASE ENTER TO START>> ")

    # Create a SMACH state machine
    sm = smach.StateMachine(outcomes=['Exit'])

    # Open the container
    with sm:
        # Add states to the container
        smach.StateMachine.add('Recognition', Recognition(), transitions={'success_Recognition':'Search'})
        smach.StateMachine.add('Search', Search(), transitions={'success_Search':'Navigation'})
        smach.StateMachine.add('Navigation', Navigation(), transitions={'success_Navigation':'Exit','False_Navigation':'Recognition'})

    # Execute SMACH plan
    sis = smach_ros.IntrospectionServer("sm_server", sm, "/ROOT")   
    sis.start()
    outcome = sm.execute()
    sis.stop()



if __name__ == '__main__':
    main()
