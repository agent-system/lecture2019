#!/usr/bin/env python

import rospy
import cv2
import subprocess
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

name = 'AizuSpiderAA'

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

rospy.wait_for_service('%s/grasp'%(name))
rospy.wait_for_service('%s/solve_ik'%(name))

grasp_srv = rospy.ServiceProxy('%s/grasp'%(name), Grasp)
solve_ik_srv = rospy.ServiceProxy('%s/solve_ik'%(name), SolveIK)

# target pose
cds = Pose()
cds.position.x =  0.9
cds.position.y =  0
cds.position.z =  0.8

solve_ik(cds)
do_grasp(False)

cds.position.x =  0.5
cds.position.y =  0
cds.position.z =  0.8
solve_ik(cds)
