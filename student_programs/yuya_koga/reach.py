#!/usr/bin/env python

import rospy
import sys
import struct
import tf
import time

from aizuspider_description.srv import (
    Grasp,
    SolveIK,
    )
from geometry_msgs.msg import (
    Pose
    )
from sensor_msgs.msg import (
    PointCloud2
    )
from opencv_apps.msg import(
    RotatedRectArrayStamped,
    Point2D
    )

from pyquaternion import Quaternion
import math

name = 'AizuSpiderAA'
contour_detected = False
contour_center = Point2D
object_position = [0, 0, 0]
hand_rotate = 0.0
hand_offset_x = 0.0
hand_offset_y = 0.0
tf_listener = None

is_finished = False

rospy.init_node('catch_object', anonymous=True)

rospy.wait_for_service('%s/solve_ik'%(name))

def contours_callback(data):
    if is_finished:
        sys.exit(1)

    print("[contours_callback] start.")
    rects = data.rects
    max_num = -1
    tmp_max = 0
    for i in range(len(rects)):
        tmp_size = rects[i].size.width * rects[i].size.height
        if tmp_max < tmp_size:
            max_num = i
            tmp_max = tmp_size
    if max_num == -1:
        print("[contours_callback] No contour found.")
        return
    else:
        print("[contours_callback] center is ({}, {}).".format(rects[max_num].center.x, rects[max_num].center.y))
        global contour_detected
        global contour_center
        contour_center = rects[max_num].center
        contour_detected = True

def point_cloud_callback(data):
    if is_finished:
        sys.exit(1)
    if not contour_detected:
        return

    global contour_center
    global object_position

    print("[point_cloud_callback] start.")
    offset = int(contour_center.y) * data.row_step + int(contour_center.x) * data.point_step

    for i in range(3):
        data_array = [data.data[offset + 4 * i], data.data[offset + 4 * i + 1], data.data[offset + 4 * i + 2], data.data[offset + 4 * i + 3]]
        object_position[i] = struct.unpack('<f', bytearray(data_array))[0]
    print("[point_cloud_callback] x:{0}, y:{1}, z:{2}".format(object_position[0], object_position[1], object_position[2]))
    #ik(getHandI())
    trans = getHandTF()
    if trans == -1:
        return
    global is_finished
    is_finished = True
    ik(trans)
    sys.exit(1)

def getHandTF():
    br = tf.TransformBroadcaster()
    br.sendTransform((object_position[0], object_position[1], object_position[2]),
                     (0.0, 0.0, 0.0, 1.0),
                     rospy.Time.now(),
                     "/target_object", "/AizuSpiderAA/ARM_CAMERA")
    try:
        (trans,rot) = tf_listener.lookupTransform('/AizuSpiderAA/CHASSIS', '/target_object', rospy.Time(0))
    except (tf.LookupException, tf.ConnectivityException, tf.ExtrapolationException):
        print("[getHandTF] no transform to /target_object")
        return -1

    print("[getHandTF] object trans x:{0}, y:{1}, z:{2}".format(trans[0], trans[1], trans[2]))
    return trans

def ik(trans):
    print "[ik] start"
    try:
        toggle_srv = rospy.ServiceProxy('%s/solve_ik'%(name), SolveIK)
        cds = Pose()

        cds.position.x = float(trans[0] - hand_offset_x)
        cds.position.y = float(trans[1] - hand_offset_y)
        cds.position.z = float(trans[2])
        q = Quaternion(axis=[1, 0, 0], angle=hand_rotate)
        cds.orientation.w = q.elements[0]
        cds.orientation.x = q.elements[1]
        cds.orientation.y = q.elements[2]
        cds.orientation.z = q.elements[3]

        res = toggle_srv(pose=cds, position_ik=False, move=2000, wait=True)
        print res
        dir(res)
    except rospy.ServiceException, e:
        print "Service call failed: %s"%e
        return

if __name__ == '__main__':
    rospy.init_node('catch_object', anonymous=True)

    rospy.Subscriber("/camera/arm/general_contours/rectangles", RotatedRectArrayStamped, contours_callback)
    rospy.Subscriber("/AizuSpiderAA/ARM_CAMERA/points", PointCloud2, point_cloud_callback)

    global hand_rotate
    args = sys.argv
    if len(args) > 1:
        hand_rotate = float(args[1])

    global hand_offset_x
    args = sys.argv
    if len(args) > 2:
        hand_offset_x = float(args[2])

    global hand_offset_y
    args = sys.argv
    if len(args) > 3:
        hand_offset_y = float(args[3])

    global tf_listener
    tf_listener = tf.TransformListener()

    rospy.spin()
