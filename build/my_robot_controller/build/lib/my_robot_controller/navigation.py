#!/usr/bin/env python3

import rclpy
from rclpy.node import Node
from nav_msgs.msg import Odometry
from geometry_msgs.msg import PoseStamped, PoseWithCovarianceStamped
import tf_transformations
import math
import time

class TurtleNavigationNode(Node):
    def __init__(self):
        super().__init__("navigation")
        self.get_logger().info("Navigation Node started")
        self.goal_poses = [
            {'x': 8.5, 'y': 3.1, 'yaw': -30},
            {'x': 10, 'y': -1.2, 'yaw': 60},
            {'x': 9.2, 'y': -7, 'yaw': 0},
            {'x': 2.35, 'y': -7.75, 'yaw': 90}
        ]
        self.current_goal_index = 0
        
        # Publishers
        self.initial_pose_publisher = self.create_publisher(
            PoseWithCovarianceStamped, "/initialpose", 10)
        self.goal_pose_publisher = self.create_publisher(
            PoseStamped, "/goal_pose", 10)
        
        # Subscriber
        self.odom_listener = self.create_subscription(
            Odometry, "/odom", self.odom_callback, 10)
        
        # Publish initial pose and first goal
        # Note: In a production node, using a timer is better than sleep in __init__
        time.sleep(5) 
        self.publish_initial_pose()
        time.sleep(5)
        self.publish_goal()

    def publish_initial_pose(self):
        initial_pose = PoseWithCovarianceStamped()
        initial_pose.header.frame_id = 'map'
        initial_pose.header.stamp = self.get_clock().now().to_msg()
        initial_pose.pose.pose.position.x = -2.0
        initial_pose.pose.pose.position.y = -0.5
        quaternion = tf_transformations.quaternion_from_euler(0, 0, 0)
        initial_pose.pose.pose.orientation.x = quaternion[0]
        initial_pose.pose.pose.orientation.y = quaternion[1]
        initial_pose.pose.pose.orientation.z = quaternion[2]
        initial_pose.pose.pose.orientation.w = quaternion[3]
        self.initial_pose_publisher.publish(initial_pose)
        self.get_logger().info("Initial pose published")

    def odom_callback(self, msg: Odometry):
        current_pose = msg.pose.pose
        goal_pose = self.goal_poses[self.current_goal_index]
        distance_to_goal = math.sqrt(
            (current_pose.position.x - goal_pose['x']) ** 2 +
            (current_pose.position.y - goal_pose['y']) ** 2
        )
        if distance_to_goal < 0.3:
            self.publish_next_goal()

    def publish_next_goal(self):
        if self.current_goal_index < len(self.goal_poses) - 1:
            self.current_goal_index += 1
            self.publish_goal()
        else:
            self.get_logger().info("All goals reached!")
            # Using a small delay before shutdown to ensure logs are seen
            time.sleep(1)
            rclpy.shutdown()

    def publish_goal(self):
        goal = self.goal_poses[self.current_goal_index]
        pose_msg = PoseStamped()
        pose_msg.header.frame_id = 'map'
        pose_msg.header.stamp = self.get_clock().now().to_msg()
        pose_msg.pose.position.x = goal['x']
        pose_msg.pose.position.y = goal['y']
        quaternion = tf_transformations.quaternion_from_euler(0, 0, math.radians(goal['yaw']))
        pose_msg.pose.orientation.x = quaternion[0]
        pose_msg.pose.orientation.y = quaternion[1]
        pose_msg.pose.orientation.z = quaternion[2]
        pose_msg.pose.orientation.w = quaternion[3]
        self.goal_pose_publisher.publish(pose_msg)
        self.get_logger().info(f"Published goal {self.current_goal_index + 1}")

def main(args=None):
    rclpy.init(args=args)
    node = TurtleNavigationNode()
    try:
        rclpy.spin(node)
    except (KeyboardInterrupt, rclpy.executors.ExternalShutdownException):
        pass
    finally:
        if rclpy.ok():
            node.destroy_node()
            rclpy.shutdown()

if __name__ == "__main__":
    main()