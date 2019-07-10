#!/usr/bin/env python

from __future__ import print_function

import rospy
import tf
import math
import argparse
import sys

from sensor_msgs.msg import Joy
from geometry_msgs.msg import Twist
from geometry_msgs.msg import PoseStamped

msg = """

"""

class MovePub:
    def __init__(self, name=''):
        self.joy_pub_ = rospy.Publisher('%sjoy'%(name), Joy,   queue_size = 10)
        self.cmd_pub_ = rospy.Publisher('%scmd_vel'%(name), Twist, queue_size = 10)

        self.stop_ = rospy.get_param("~stop", 0.5)
        self.trans_x = 0.0
        self.trans_y = 0.0
        self.trans_z = 0.0
        self.rot_x = 0.0
        self.rot_y = 0.0
        self.rot_z = 0.0
        self.rot_w = 1.0
        self.tm = None

        self.rate = rospy.Rate(100)

    def stop_pub(self):
        msg = Joy()
        msg.axes = [0]*8
        msg.buttons = [0]*11
        self.joy_pub_.publish(msg)

        cmd = Twist()
        self.cmd_pub_.publish(cmd)

    def move_pub(self, trans, rot):
        msg = Joy()
        msg.axes = [0]*8
        msg.buttons = [0]*11
        # print('move: %f %f'%(trans, rot))
        if trans > 0.0:
            msg.axes[1] = -1
        elif trans < 0.0:
            msg.axes[1] =  1
        if rot > 0.0:
            msg.axes[0] = -1
        elif rot < 0.0:
            msg.axes[0] =  1

        self.joy_pub_.publish(msg)

        cmd = Twist()
        if trans != 0.0:
            cmd.linear.x  = 4.0 * trans / math.fabs(trans)
        if rot != 0.0:
            cmd.angular.z = 1.5 * rot / math.fabs(rot)
        self.cmd_pub_.publish(cmd)

    def move(self, x_trans = 0.0 , z_rot = 0.0):
        origin_pos = (self.trans_x, self.trans_y, self.trans_z)
        origin_rot = (self.rot_w, self.rot_x, self.rot_y, self.rot_z)
        #print(origin_pos)

        for i in range(20): ## waiting enable publishing (why needed??)
            self.rate.sleep()
        self.move_pub(x_trans, z_rot)

        cntr = 0
        while True:
            self.rate.sleep()

            pos = (self.trans_x, self.trans_y, self.trans_z)
            rot = (self.rot_w, self.rot_x, self.rot_y, self.rot_z)
            #print(pos)
            diff_pos = [pos[0] - origin_pos[0], pos[1] - origin_pos[1], pos[2] - origin_pos[2]]
            diff_len = math.sqrt(diff_pos[0] * diff_pos[0] + diff_pos[1] * diff_pos[1] + diff_pos[2] * diff_pos[2])

            diff_rot = math.atan2(rot[3], rot[0]) - math.atan2(origin_rot[3], origin_rot[0])
            if diff_rot > math.pi:
                diff_rot = diff_rot - math.pi
            if diff_rot < - math.pi:
                diff_rot = diff_rot + math.pi
            diff_rot = math.sqrt(diff_rot * diff_rot)

            ### debug print
            if cntr %10 == 0:
                print('trans:%5.2f rot:%5.2f'%(diff_len, diff_rot))

            cntr = cntr + 1
            if x_trans == 0.0 or diff_len > math.fabs(x_trans):
                if z_rot == 0.0 or diff_rot > math.fabs(z_rot):
                    print('trans:%5.2f rot:%5.2f'%(diff_len, diff_rot))
                    break

        self.stop_pub()

    def callback(self, msg):
        self.tm = msg.header.stamp
        ##fm = msg.header.frame_id
        self.trans_x = msg.pose.position.x
        self.trans_y = msg.pose.position.y
        self.trans_z = msg.pose.position.z

        self.rot_x = msg.pose.orientation.x
        self.rot_y = msg.pose.orientation.y
        self.rot_z = msg.pose.orientation.z
        self.rot_w = msg.pose.orientation.w

    def wait_first_callback(self):
        while not self.tm:
            self.rate.sleep()

if __name__=="__main__":
    ### parser section
    args = sys.argv
    name = 'AizuSpiderAA/'

    if len(args) > 1:
        trans = float(args[1])
    else:
        trans = 0.0

    if len(args) > 2:
        rot = float(args[2])
    else:
        rot = 0.0

    ### ROS section
    rospy.init_node('move_sample')

    mv = MovePub(name)

    rospy.Subscriber('%sground_truth_pose'%(name), PoseStamped, mv.callback)
    mv.wait_first_callback()

    mv.move(trans, rot)

    ##rospy.spin()
