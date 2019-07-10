#!/usr/bin/env python

from __future__ import print_function

import rospy

from sensor_msgs.msg import Joy

import pygame
from pygame.locals import *

import subprocess

import sys, select, termios, tty, fcntl, os


msg = """

"""


EEE = 10e-3

cmd1 = 'rosrun aizuspider_description ' \
                             'send_trajectory_with_pseq.py ' \
                             '-N AizuSpiderAA ' \
                             '-F PoseSeq1.pseq --offset=2.0'

cmd2 = 'rosrun aizuspider_description ' \
                             'send_trajectory_with_pseq.py ' \
                             '-N AizuSpiderAA ' \
                             '-F PoseSeq2.pseq --offset=2.0'

cmd3 = 'python release.py'
cmd4 = 'python grasp.py'
cmd5 = 'roslaunch aizuspider_description pointcloud_screenpoint.launch'
cmd6 = 'python click_and_pick.py'

robo_name = ['AizuSpiderAA', 'AizuSpiderBB']

def send_motion_cmd(name, motion):
    cmd = 'rosrun aizuspider_description ' \
            'send_trajectory_with_pseq.py ' \
            '-N ' + name + \
            ' -F ' + motion + \
            ' --offset=2.0'
    #print(cmd)
    runcmd = subprocess.call(cmd.split())
    print (runcmd)

def send_cmd(cmd):
    runcmd = subprocess.call(cmd.split())
    print (runcmd)

def send_arm_cmd(x, y, z):
    cmd =   'python position_solve_ik.py ' \
            ' --xxx ' + str(x) + \
            ' --yyy ' + str(y) + \
            ' --zzz ' + str(z)
    runcmd = subprocess.call(cmd.split())
    print (runcmd)



class JoyPub:
    def __init__(self):
        self.settings_ = termios.tcgetattr(sys.stdin)
        self.pub_B = rospy.Publisher('/AizuSpiderBB/joy', Joy, queue_size = 1)
        self.pub_A = rospy.Publisher('/AizuSpiderAA/joy', Joy, queue_size = 1)
        self.robo_num = 0
        #self.pub_A = rospy.Publisher('robotA', Joy, queue_size = 1)
        #self.pub_B = rospy.Publisher('robotB', Joy, queue_size = 1)
        self.stop_ = rospy.get_param("~stop", 0.5)
        self.button_flg = [0]*11
        self.joy_axis = [0]*6
        self.hand_status = 0
        self.motion = 0
        self.start_flg = 1

        pygame.init()
        pygame.joystick.init()
        try:
            self.j = pygame.joystick.Joystick(0)# create a joystick instance
            self.j.init() # init
            print('Joystick: ' + self.j.get_name())
            print('bottun : ' + str(self.j.get_numbuttons()))
            pygame.event.get()
            
        except pygame.error:
            print('No connect joystick')
            print('exit')
            pygame.quit()
            sys.exit()

        finally:
            msg = Joy()
            msg.axes = [0]*8
            msg.buttons = [0]*11
            self.pub_B.publish(msg)
            self.pub_A.publish(msg)
            termios.tcsetattr(sys.stdin, termios.TCSADRAIN, self.settings_)
 
    # Intializes everything
    def main(self):
        prev1 = None
        prev2 = None
        try:
            while(1):
                msg = Joy()
                msg.axes = [0]*8
                msg.buttons = [0]*11
                
                for e in pygame.event.get(): #event check
                    if e.type == QUIT: # is pushed quit
                        pygame.quit()
                        return
                    if e.type == KEYDOWN:
                        if e.key  == K_ESCAPE: # is pushed escape
                            pygame.quit()
                            sys.exit()
                    # check event with controler
                    if e.type == pygame.locals.JOYAXISMOTION: # 7
                        for i in range(6):
                            self.joy_axis[i] = self.j.get_axis(i)
                            #if((self.joy_axis[i] < 10e-3) and (self.joy_axis[i] > -10e-3)):
                            #    self.joy_axis[i] = 0
                            if(self.joy_axis[i] > 0.5):
                                self.joy_axis[i] = -1
                            elif(self.joy_axis[i] < -0.5):
                                self.joy_axis[i] = 1 
                            else:
                                self.joy_axis[i] = 0                              
                        print('Rx' + '{:.4}'.format(str(self.joy_axis[3])) + \
                              'Ry' + '{:.4}'.format(str(self.joy_axis[4])) + \
                              'Rz' + '{:.4}'.format(str(self.joy_axis[5])) + \
                              'Lx' + '{:.4}'.format(str(self.joy_axis[0])) + \
                              'Ly' + '{:.4}'.format(str(self.joy_axis[1])) + \
                              'Lz' + '{:.4}'.format(str(self.joy_axis[2])) )
                              
                        '''
                        msgB.axes[0] = self.joy_axis[0]
                        msgB.axes[1] = self.joy_axis[1]
                        '''
                        #msg.axes[0] = -self.joy_axis[0]
                        #msg.axes[1] = -self.joy_axis[1]
                            
                        #msg.axes[0] = -self.joy_axis[0]
                        #msg.axes[1] = -self.joy_axis[1]
                        #self.pub_A.publish(msg)


                        #msg.axes = [0]*8
                        #msg.buttons = [0]*11
                        
                        
                        '''
                        msgA.axes[0] = self.joy_axis[3]
                        msgA.axes[1] = self.joy_axis[4]
                        '''
                        msg.axes[0] = -self.joy_axis[0]
                        msg.axes[1] = -self.joy_axis[1]
                        #msg.axes[3] = -self.joy_axis[3]
                        #msg.axes[4] = -self.joy_axis[4]
                        self.pub_A.publish(msg)

                        msg.axes = [0]*8
                        msg.buttons = [0]*11
                        
                    elif e.type == pygame.locals.JOYBALLMOTION: # 8
                        print('ball motion')
                    elif e.type == pygame.locals.JOYHATMOTION: # 9
                        print('hat motion')
                    elif e.type == pygame.locals.JOYBUTTONDOWN: # 10
                        for i in range(self.j.get_numbuttons()):
                            if(e.button == i):
                                self.button_flg[i] = 1

                        if(self.button_flg[8]):
                            #self.robo_num = (self.robo_num + 1)%2
                            for i in range(1):
                                msg.buttons[i] = -self.button_flg[i]
                            self.pub_A.publish(msg)

                        elif(self.button_flg[0]):
                            #send_motion_cmd(robo_name[self.robo_num], 'PoseSeq1.pseq')
                            if(self.hand_status==1):
                                send_cmd(cmd3)
                                self.hand_status = 0
                            elif(self.hand_status==0):
                                send_cmd(cmd4)
                                self.hand_status = 1

                        elif(self.button_flg[1]):
                            #send_motion_cmd(robo_name[self.robo_num], 'PoseSeq2.pseq')
                            send_arm_cmd(str(0.424), str(-0.1583), str(1.0291))
                            runcmd = 0

                        elif(self.button_flg[2]):
                            '''
                            if(self.start_flg):
                                send_cmd(cmd5)
                                self.start_flg = 0
                            else:
                            '''   
                            #send_cmd(cmd6)
                            runcmd = 0
                            
                        elif(self.button_flg[3]):
                            if(self.motion == 0):
                                send_motion_cmd('AizuSpiderAA', 'PoseSeq1.pseq')
                                self.motion = 1
                            elif(self.motion == 1):
                                send_motion_cmd('AizuSpiderAA', 'PoseSeq2.pseq')
                                self.motion = 0
                            runcmd = 0

                        if(self.button_flg[4] and self.button_flg[5] and self.button_flg[6] and self.button_flg[7]):
                            print('exit')
                            pygame.quit()
                            sys.exit()

                        print(  'A' + str(self.button_flg[0]) + \
                                'B' + str(self.button_flg[1]) + \
                                'X' + str(self.button_flg[2]) + \
                                'Y' + str(self.button_flg[3]) + \
                                'LB' + str(self.button_flg[4]) + \
                                'RB' + str(self.button_flg[5]) + \
                                'BACK' + str(self.button_flg[6]) + \
                                'START' + str(self.button_flg[7]) + \
                                'Logicool' + str(self.button_flg[8]) + \
                                'StL' + str(self.button_flg[9]) + \
                                'StR' + str(self.button_flg[10]))    
                        self.pub_B.publish(msg)
                        self.pub_A.publish(msg)
                        
                    elif e.type == pygame.locals.JOYBUTTONUP: # 11
                        for i in range(self.j.get_numbuttons()):
                            if(e.button == i):
                                self.button_flg[i] = 0
                            
                        print(  'A' + str(self.button_flg[0]) + \
                                'B' + str(self.button_flg[1]) + \
                                'X' + str(self.button_flg[2]) + \
                                'Y' + str(self.button_flg[3]) + \
                                'LB' + str(self.button_flg[4]) + \
                                'RB' + str(self.button_flg[5]) + \
                                'BACK' + str(self.button_flg[6]) + \
                                'START' + str(self.button_flg[7]) + \
                                'Logicool' + str(self.button_flg[8]) + \
                                'StL' + str(self.button_flg[9]) + \
                                'StR' + str(self.button_flg[10]))    
        except Exception as e:
            print(e)
        finally:
            msg = Joy()
            msg.axes = [0]*8
            msg.buttons = [0]*11
            self.pub_A.publish(msg)
            self.pub_B.publish(msg)
            termios.tcsetattr(sys.stdin, termios.TCSADRAIN, self.settings_)

    def getKey(self):
        tty.setraw(sys.stdin.fileno())
        keys = []
        key = None
        while(True):
            ret = select.select([sys.stdin], [], [], 0)
            ##print(ret)
            # if len(ret[0]) < 1:
            #     if len(keys) >= 1:
            #         break
            #     msg = Joy()
            #     msg.axes = [0]*8
            #     msg.buttons = [0]*11
            #     self.pub_.publish(msg)
            #     continue
            key = sys.stdin.read(1)
            keys.append(key)
            if len(key) >= 1:
                break

        termios.tcsetattr(sys.stdin, termios.TCSADRAIN, self.settings_)
        #print(keys)
        #''.join(keys)
        return key





if __name__=="__main__":
    rospy.init_node('controller_joy')

    jp = JoyPub()

    jp.main()

