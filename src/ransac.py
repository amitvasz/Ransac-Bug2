#!/usr/bin/env python
import roslib
import rospy
from geometry_msgs.msg import Twist
from sensor_msgs.msg import LaserScan
from nav_msgs.msg import Odometry
import math
import numpy as np
import geometry_msgs.msg
import turtlesim.srv
roslib.load_manifest('lab2')
import tf
import turtlesim.msg
from visualization_msgs.msg import Marker
flagWall = 0
sinx = np.array((360,1)) 
cosx = np.array((360,1))

def init():
    global sinx
    global cosx
    degrees = np.radians(np.linspace(-90, 90 , 360))
    sinx = np.sin(degrees)
    cosx = np.cos(degrees)

def ransacimp():
    x = []
    y = []
    ln = len(x)
    indexes = range(ln)
    points = []
    somethreshold = ln * 0.1
    k = 20
    inl = []
    outl = []
    xx1 = -1
    yy1 = -1
    xx2 = -1
    yy2 = -1
    threshold = 0.4
    print "ENTRY in the ransacimp function "
    for r in range(10):
	    for i in indexes:
		tempinl = []
		tempoutl = []
		index1 = random.randint(0,ln)
		index2 = random.randint(0,ln)
		x1 = x[index1]
		y1 = y[index1]
		x2 = x[index2]
		y2 = y[index2]
		for j in range(ln):
		    x0 = x[j]
		    y0 = y[j]
		    dist = abs((y2 - y1) * x0 - (x2 - x1)*y0 + x2 * y1 - y2 * x1) / sqrt((y2 - y1) * (y2 - y1) + (x2 - x1) * (x2 - x1))
		    if dist < threshold:
		        # add inliners
		        tempinl.append(i)
		    else:
		        # add outliers
		        tempoutl.append(i)
		if len(inl) < len(tempinl):
		    inl = tempinl
		    outl = tempoutl
		    in1 = index1
		    in2 = index2
	    #Add new line two something for latter use
	    points.append(index1, index2)
	    indexes = outl
	    if len(indexes) < somethreshold:
		break
        


def talker():
    rate = rospy.Rate(10)
    shape = Marker.ARROW
    pub = rospy.Publisher("visualization_marker", Marker, queue_size=10)
    # initialization of 
    init()
    while not rospy.is_shutdown():
        try:
            ransacimp()
	    marker = Marker()
            marker.header.frame_id = "/my_frame"
            marker.header.stamp = rospy.Time.now()
            marker.ns = "ransac"
            marker.id = 0
            marker.type = shape
            marker.action = Marker.ADD
            marker.pose.position.x = 0
            marker.pose.position.y = 0
            marker.pose.position.z = 0
            marker.pose.orientation.x = 0.0
            marker.pose.orientation.y = 0.0
            marker.pose.orientation.z = 0.0
            marker.pose.orientation.w = 1.0

	    marker.scale.x = 1.0
	    marker.scale.y = 1.0
	    marker.scale.z = 1.0

	    marker.color.r = 0.0
	    marker.color.g = 1.0
	    marker.color.b = 0.0
	    marker.color.a = 1.0

	    marker.lifetime = rospy.Duration()
	    pub.publish(marker)
            rate.sleep()
        except (tf.LookupException, tf.ConnectivityException, tf.ExtrapolationException):
            continue		
            



if __name__ == '__main__':
    try:
        rospy.init_node('ransac', anonymous=True)
        #turtlename = rospy.get_param('~/robot_1/odom')
        talker()
    except rospy.ROSInterruptException:
        pass

