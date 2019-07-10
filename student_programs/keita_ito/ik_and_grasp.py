import rospy
import tf
import sys

from aizuspider_description.srv import (
    Grasp,
    SolveIK,
    )

from geometry_msgs.msg import (
    Pose
    )

from pyquaternion import Quaternion

import math

name = 'AizuSpiderAA'

#tfBuffer = tf2_ros.Buffer()
rospy.init_node('ik_and_grasp', anonymous=True)
rospy.wait_for_service('%s/solve_ik'%(name))
rospy.wait_for_service('%s/grasp'%(name))

listener = tf.TransformListener()
while True:
    try:
        w2obj_tf = listener.lookupTransform('AizuSpiderAA/CHASSIS', 'my_cluster_decomposeroutput' + sys.argv[1], rospy.Time(0))
        w2cam_tf = listener.lookupTransform('AizuSpiderAA/CHASSIS', 'AizuSpiderAA/ARM_CAMERA', rospy.Time(0))
        break
    except:
        pass
#print w2cam_tf
for i in range(3):
    w2obj_tf[1][i] = w2cam_tf[1][i]

try:
    toggle_srv = rospy.ServiceProxy('%s/solve_ik'%(name), SolveIK)
    cds = Pose()
    cds.position.x = w2obj_tf[0][0] 
    cds.position.y = w2obj_tf[0][1]
    if len(sys.argv) == 3:
        if sys.argv[2] == "clock":
            cds.position.x = w2obj_tf[0][0] + 0.02
            cds.position.z = w2obj_tf[0][2] + 0.05
            q = Quaternion(axis=[1, 1, 1], angle=0)
        else:
            cds.position.z = w2obj_tf[0][2]
            q = Quaternion(axis=[1, 0, 0], angle=1.57)
    else:
        cds.position.y -= 0.2
        cds.position.z = w2obj_tf[0][2]
        q = Quaternion(axis=[1, 1, 1], angle=0)
        
    cds.orientation.w = q.elements[0]
    cds.orientation.x = q.elements[1]
    cds.orientation.y = q.elements[2]
    cds.orientation.z = q.elements[3]

    res = toggle_srv(pose=cds, position_ik=False, move=2000, wait=True)
    print res
    dir(res)
except rospy.ServiceException, e:
    print "IK Service call failed: %s"%e
    exit(1)
    
try:
    toggle_srv = rospy.ServiceProxy('%s/grasp'%(name), Grasp)
    ##req = Grasp()
    ##req.position = 60.0
    ##req.time   = 1000
    ##req.wait = False
    res = toggle_srv(position=[math.pi/2.5, math.pi/2.5, math.pi/2.5], time=1000, wait=False)

except rospy.ServiceException, e:
    print "Grasp Service call failed: %s"%e
    exit(1)
