import rospy

from aizuspider_description.srv import (
    Grasp,
    SolveIK,
    )

import math

name = 'AizuSpiderAA'

rospy.init_node('test_grasp', anonymous=True)

rospy.wait_for_service('%s/grasp'%(name))
try:
    toggle_srv = rospy.ServiceProxy('%s/grasp'%(name), Grasp)
    ##req = Grasp()
    ##req.position = 60.0
    ##req.time   = 1000
    ##req.wait = False
    res = toggle_srv(position=[math.pi/3, math.pi/3, math.pi/3], time=1000, wait=False)

except rospy.ServiceException, e:
    print "Service call failed: %s"%e
    exit(1)
