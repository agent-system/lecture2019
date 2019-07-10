#!/usr/bin/env python

import rospy
import tf
import os

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

rospy.init_node('clicked_point', anonymous=True)

listener = tf.TransformListener()

rospy.wait_for_service('%s/grasp'%(name))
rospy.wait_for_service('%s/solve_ik'%(name))

grasp_srv = rospy.ServiceProxy('%s/grasp'%(name), Grasp)
solve_ik_srv = rospy.ServiceProxy('%s/solve_ik'%(name), SolveIK)

def do_grasp():
    try:
        res = grasp_srv(position=[math.pi/3, math.pi/3, math.pi/3], time=1000, wait=False)
    except rospy.ServiceException as e:
        print "Service call failed: %s"%(e)
        rospy.signal_shutdown('service error')

def do_release():
    try:
        res = grasp_srv(position=[0, 0, 0], time=1000, wait=False)
    except rospy.ServiceException as e:
        print "Service call failed: %s"%(e)
        rospy.signal_shutdown('service error')

def move_to_trash():
    os.system('./move.py --trans -1.0 --name AizuSpiderAA')
    os.system('./move.py --rot 0.785 --name AizuSpiderAA')
    os.system('./move.py --trans 1.5 --name AizuSpiderAA')
    os.system('./move.py --rot -0.785 --name AizuSpiderAA')
    os.system('./move.py --trans 6.0 --name AizuSpiderAA')
    os.system('./move.py --rot 0.785 --name AizuSpiderAA')
    os.system('./move.py --trans 1.0 --name AizuSpiderAA')

def move_to_desk():
    os.system('./move.py --trans -1.0 --name AizuSpiderAA')
    os.system('./move.py --rot -0.785 --name AizuSpiderAA')
    os.system('./move.py --trans -6.0 --name AizuSpiderAA')
    os.system('./move.py --rot 0.785 --name AizuSpiderAA')
    os.system('./move.py --trans -1.5 --name AizuSpiderAA')
    os.system('./move.py --rot -0.785 --name AizuSpiderAA')
    os.system('./move.py --trans 1.0 --name AizuSpiderAA')
    
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
        print res
        dir(res)
        return res.success
    except rospy.ServiceException as e:
        print "Service call failed: %s"%(e)
        rospy.signal_shutdown('service error')
    return False

def callback(ptmsg):
    rospy.loginfo("callback %s", ptmsg)
    #ptmsg.header.frame_id
    #ptmsg.header.stamp
    listener.waitForTransform('/%s/CHASSIS'%(name), ptmsg.header.frame_id, ptmsg.header.stamp, rospy.Duration(5.0))
    try:
        (trans,rot) = listener.lookupTransform('/%s/CHASSIS'%(name), ptmsg.header.frame_id, ptmsg.header.stamp)
    except (tf.LookupException, tf.ConnectivityException, tf.ExtrapolationException) as e:
        print "Tf error %s"%(e)
        rospy.signal_shutdown('tf error')

    print 'tr:', trans
    print 'rt:', rot
    q = Quaternion([ rot[3], rot[0], rot[1], rot[2] ])
    print 'org:', [ ptmsg.point.x, ptmsg.point.y, ptmsg.point.z ]
    ptrans = q.rotate([ ptmsg.point.x, ptmsg.point.y, ptmsg.point.z ])
    print 'tgt:', ptrans

    cds = Pose()
    cds.position.x = trans[0] + ptrans[0]
    cds.position.y = trans[1] + ptrans[1]
    cds.position.z = trans[2] + ptrans[2]
    ##q = Quaternion(axis=[0, 1, 0], angle=0.35)
    cds.orientation.w = 1
    cds.orientation.x = 0
    cds.orientation.y = 0
    cds.orientation.z = 0

    if solve_ik(cds):
        do_grasp()
        move_to_trash()
        do_release()
        move_to_desk()
                
    else:
        print "IK failed"

    ### pick up ...

    rospy.signal_shutdown('finished')

rospy.Subscriber("/pointcloud_screenpoint_nodelet/output_point", PointStamped, callback)

rospy.spin()
