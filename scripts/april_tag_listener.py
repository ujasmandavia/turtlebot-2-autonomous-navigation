#!/usr/bin/env python  

#import roslib
#roslib.load_manifest('learning_tf')
import rospy
import math
import tf
from final_project.msg import AprilTag
import geometry_msgs.msg

# Given the 
def check_for_tag(tag_frame):
    try:
        (trans,rot) = listener.lookupTransform('/map', tag_frame, rospy.Time(0))
    except (tf.LookupException, tf.ConnectivityException, tf.ExtrapolationException):
        return None
    (x, y, z) = trans
    return (x, y)


if __name__ == '__main__':
    rospy.init_node('april_tag_listener')

    listener = tf.TransformListener()

    pub = rospy.Publisher('/april_tags_locations', AprilTag, queue_size=10)
    move_pub = rospy.Publisher('move_base_simple/goal', geometry_msgs.msg.PoseStamped, queue_size=10)

    t = 0

    rate = rospy.Rate(10.0)

    tag_store = {} # Create a hashtable to store locations of tags
    tag_names = ["tag_0", "tag_1", "tag_2", "tag_3", "tag_4", "tag_5"] # Move to config file
    
    
    while not rospy.is_shutdown():
        for tag_name in tag_names:
            coordinates = check_for_tag(tag_name)
            if coordinates is not None:
                # (x, y) = coordinates
                tag_store[tag_name] = coordinates

        for tag_name in tag_store:
            #publish
            tag_loc = AprilTag()
            tag_loc.header.frame_id = "/map"
            tag_loc.id = tag_name
            (x, y) = tag_store[tag_name]
            tag_loc.point.x = x
            tag_loc.point.y = y
            pub.publish(tag_loc)
        
        print tag_store

        rate.sleep()
