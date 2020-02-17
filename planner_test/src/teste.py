#!/usr/bin/env python
# license removed for brevity
import rospy
from geometry_msgs.msg import PoseStamped
from nav_msgs.msg import Path
from move_base_msgs.msg import MoveBaseAction, MoveBaseGoal
import math
import sys
import argparse
import actionlib

def talker():

    parser=argparse.ArgumentParser()

    parser.add_argument('--planner')
    parser.add_argument('--test_n')
    parser.add_argument('--x_pos')
    parser.add_argument('--y_pos')
    parser.add_argument('--x_or')
    parser.add_argument('--y_or')
    parser.add_argument('--z_or')
    parser.add_argument('--w_or')

    arg=parser.parse_args()

    planner = arg.planner
    x_pos = float(arg.x_pos) if arg.x_pos else 0.0
    y_pos = float(arg.y_pos) if arg.y_pos else 0.0
    x_or = float(arg.x_or) if arg.x_or else 0.0
    y_or = float(arg.y_or) if arg.y_or else 0.0
    z_or = float(arg.z_or) if arg.z_or else 0.0
    w_or = float(arg.w_or) if arg.w_or else 0.0
    test_n = arg.test_n


    # goal_publisher = rospy.Publisher('move_base_simple/goal', PoseStamped, queue_size=1)
    rospy.init_node('pytester')
    rate = rospy.Rate(10) # 10hz
    # while not rospy.is_shutdown():

    goal_client = actionlib.SimpleActionClient('move_base',MoveBaseAction)
    goal_client.wait_for_server()
    
    #Build and send goal
    goal = MoveBaseGoal()

    # goal.target_pose.header.seq = 1
    goal.target_pose.header.frame_id = "map"

    goal.target_pose.pose.position.x = x_pos
    goal.target_pose.pose.position.y = y_pos
    goal.target_pose.pose.position.z = 0.0

    goal.target_pose.pose.orientation.x = x_or
    goal.target_pose.pose.orientation.y = y_or
    goal.target_pose.pose.orientation.z = z_or
    goal.target_pose.pose.orientation.w = w_or

    goal.target_pose.header.stamp = rospy.Time.now()
    goal_client.send_goal(goal)

    #Wait for path and calculate length
    path = rospy.wait_for_message("move_base/"+planner+"/plan", Path)


    tempo = path.header.stamp - goal.target_pose.header.stamp
    length = 0.0
    for i in range(1, len(path.poses)):
        length += math.sqrt(math.pow(path.poses[i].pose.position.x - path.poses[i-1].pose.position.x, 2) + math.pow(path.poses[i].pose.position.y - path.poses[i-1].pose.position.y, 2))


    #Write results on file
    saida = open(planner + "_" + test_n, "a")
    saida.write("Tempo: " + str(tempo.secs) + "s  " + str(tempo.nsecs) + "ns\n")
    saida.write("Comprimento: " + str(length) + "m\n")
    saida.close()

if __name__ == '__main__':
    try:
        talker()
    except rospy.ROSInterruptException:
        pass