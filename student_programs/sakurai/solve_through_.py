import rospy

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

rospy.init_node('test_ik', anonymous=True)

rospy.wait_for_service('%s/solve_ik'%(name))
try:
    toggle_srv = rospy.ServiceProxy('%s/solve_ik'%(name), SolveIK)
    cds = Pose()
    cds.position.x =  0.84
    cds.position.y = -0.183
    cds.position.z = 0.17

    q = Quaternion(axis=[0, 1, 0], angle=0.35)
    cds.orientation.w = q.elements[0]
    cds.orientation.x = q.elements[1]
    cds.orientation.y = q.elements[2]
    cds.orientation.z = q.elements[3]

    res = toggle_srv(pose=cds, position_ik=False, move=2000, wait=True)
    print res
    dir(res)
except rospy.ServiceException, e:
    print "Service call failed: %s"%e
    exit(1)
