#!/usr/bin/env python  

import rospy
import geometry_msgs.msg
from move_base_example import GoToPose
from final_project.msg import AprilTag

tag_store = {}
num_tags = 3 #MAGIC NUMBER
following_waypoints = False

def tag_location_callback(tag):
    if tag.id not in tag_store:
        print "I see", tag.id
    tag_store[tag.id] = tag.point
    if len(tag_store) == num_tags and not following_waypoints:
        # tags = []
        # for tag in tag_store:
        #     tags.append(tag_store[tag])
        follow_waypoints()

def follow_waypoints():
    print "Following Waypoints"
    navigator = GoToPose()
    for tag_id in tag_store:
        print "Navigating to", tag_id, "\n\n\n"
        tag = tag_store[tag_id]
        
        try:
            # Customize the following values so they are appropriate for your location
            position = {'x': tag.x, 'y' : tag.y}
            quaternion = {'r1' : 0.000, 'r2' : 0.000, 'r3' : 0.000, 'r4' : 1.000}

            rospy.loginfo("Go to (%s, %s) pose", position['x'], position['y'])
            success = navigator.goto(position, quaternion)
        
            if success:
                rospy.loginfo("Hooray, reached the desired pose")
            else:
                rospy.loginfo("The base failed to reach the desired pose")

            # Sleep to give the last log messages time to be sent
            rospy.sleep(1)

        except rospy.ROSInterruptException:
            rospy.loginfo("Ctrl-C caught. Quitting")

if __name__ == '__main__':
    rospy.init_node('april_follow_waypoints')

    rospy.Subscriber("/april_tags_locations", AprilTag, tag_location_callback)

    rospy.spin()
