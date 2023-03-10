import rospy
from geometry_msgs.msg import PoseStamped
from move_base_msgs.msg import MoveBaseAction, MoveBaseGoal
from actionlib import SimpleActionClient
import numpy as np


class RobotController:
    def __init__(self):
        rospy.init_node("robot_controller")
        self.client = SimpleActionClient("move_base", MoveBaseAction)
        self.client.wait_for_server()

    def go_to_goal(self, x, y, theta):
        goal = MoveBaseGoal()
        goal.target_pose.header.frame_id = "map"
        goal.target_pose.header.stamp = rospy.Time.now()
        goal.target_pose.pose.position.x = x
        goal.target_pose.pose.position.y = y
        goal.target_pose.pose.orientation.z = np.sin(theta / 2)
        goal.target_pose.pose.orientation.w = np.cos(theta / 2)
        self.client.send_goal(goal)
        self.client.wait_for_result()


if __name__ == "__main__":
    try:
        controller = RobotController()
        controller.go_to_goal(1.0, 0, np.pi / 2)  # example goal
    except rospy.ROSInterruptException:
        pass
