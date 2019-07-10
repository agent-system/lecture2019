#!/usr/bin/env python

import rospy
import cv2
import time

from sensor_msgs.msg import Image
from cv_bridge import CvBridge, CvBridgeError

from aizuspider_description.srv import (
    Grasp,
    SolveIK,
    )

from geometry_msgs.msg import (
    Pose,
    PointStamped,
    )

from pyquaternion import Quaternion
import math

image_topic_name = "/hsv_color_filter/image"
name = 'AizuSpiderAA'

# camera params
f = 137.5
rows = 480
cols = 640
baseL = 0.2

# initial pose
init_x = 0.5
init_y = -0.0
init_z = 0.8
q = Quaternion(axis=[1, 0, 0], angle=0)
cds = Pose()
cds.position.x =  init_x
cds.position.y =  init_y
cds.position.z =  init_z
cds.orientation.w = q.elements[0]
cds.orientation.x = q.elements[1]
cds.orientation.y = q.elements[2]
cds.orientation.z = q.elements[3]

def calcObjectUV():
    data = rospy.wait_for_message(image_topic_name, Image)
    try:
        cv_image = bridge.imgmsg_to_cv2(data, "bgr8")
    except CvBridgeError as e:
        print e

    cv_image = cv2.cvtColor(cv_image, cv2.COLOR_BGR2GRAY)
    # find contours
    ret, thresh = cv2.threshold(cv_image, 127, 255, 0)
    _, contours, hierarchy = cv2.findContours(thresh, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_NONE)

    rows, cols = cv_image.shape

     # pick largest contour
    if len(contours) == 0: return None
    contour = max(contours, key=cv2.contourArea)

    moments = cv2.moments(contour)
    if moments['m00'] == 0: return None

    # a = (moments['m20'] - moments['m02']) / moments['m11']
    # tan_theta = -a/2 + math.sqrt(a*a/4 + 1)
    # theta = math.atan(tan_theta)
    # print math.degrees(theta)

    _, _, width, height = cv2.boundingRect(contour)


    return [moments['m10'] / moments['m00'],
              moments['m01'] / moments['m00']], [width, height]


def do_grasp(isclose=True):
    try:
        if isclose == True:
            res = grasp_srv(position=[math.pi/3, math.pi/3, math.pi/3], time=1000, wait=True)
        else:
            res = grasp_srv(position=[-math.pi/6, -math.pi/6, -math.pi/6], time=1000, wait=True)
    except rospy.ServiceException as e:
        print "Service call failed: %s"%(e)
        rospy.signal_shutdown('service error')

def solve_ik(cds):
    try:
        # cds = Pose()
        # cds.position.x =  0.424
        # cds.position.y = -0.1583
        # cds.position.z = 1.0291
        # q = Quaternion(axis=[0, 1, 0], angle=0.35)
        # cds.orientation.w = q.elements[0]
        # cds.orientation.x = q.elements[1]
        # cds.orientation.y = q.elements[2]
        # cds.orientation.z = q.elements[3]
        res = solve_ik_srv(pose=cds, position_ik=False, move=2000, wait=True)
        print res.success
        dir(res)
        return res.success
    except rospy.ServiceException as e:
        print "Service call failed: %s"%(e)
        rospy.signal_shutdown('service error')
    return False


# main
rospy.init_node('c', anonymous=True)

bridge = CvBridge()

rospy.wait_for_service('%s/grasp'%(name))
rospy.wait_for_service('%s/solve_ik'%(name))

grasp_srv = rospy.ServiceProxy('%s/grasp'%(name), Grasp)
solve_ik_srv = rospy.ServiceProxy('%s/solve_ik'%(name), SolveIK)

do_grasp(False)
solve_ik(cds)
time.sleep(2)

# first shot
cds.position.y = -baseL/2
solve_ik(cds)
obj_uv1, _ = calcObjectUV()

# second shot
cds.position.y = baseL/2
solve_ik(cds)
obj_uv2, _ = calcObjectUV()

# calculate target pos
camera_x =  baseL * f / (obj_uv2[0] - obj_uv1[0])
cds.position.x = init_x
cds.position.y = -camera_x /f * (obj_uv1[0] - cols/2) - baseL/2
cds.position.z = -camera_x /f * (obj_uv1[1] - rows/2) + init_z

solve_ik(cds)

# calc rotation
_, ratio = calcObjectUV()
if ratio[0] < ratio[1]:
    q = Quaternion(axis=[1, 0, 0], angle=0)
else:
    q = Quaternion(axis=[1, 0, 0], angle=math.pi/2)
cds.orientation.w = q.elements[0]
cds.orientation.x = q.elements[1]
cds.orientation.y = q.elements[2]
cds.orientation.z = q.elements[3]

solve_ik(cds)

# reach target
cds.position.x = camera_x + init_x
solve_ik(cds)
do_grasp()

# reset pose
cds.position.x =  init_x
cds.position.y =  init_y
cds.position.z =  init_z
solve_ik(cds)

