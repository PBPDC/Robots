import rclpy
from rclpy.node import Node
from rclpy.qos import qos_profile_sensor_data
from sensor_msgs.msg import Imu, LaserScan, BatteryState
import time
import datetime
import numpy as np


class SensorSubscriber(Node):

    def __init__(self):
        super().__init__('sensor_subscriber')

        #self.get_params()
        #self.scan_ranges = []
        #self.init_scan_state = False
        hello = input('What do you want to see? 1:IMU 2:Laser 3:Battery 4:Time 5:ALL ')
        if hello == '1':
            self.imu_sub = self.create_subscription(Imu, 'imu', self.imu_callback, qos_profile=qos_profile_sensor_data)
        if hello == '2':
            self.laser_sub = self.create_subscription(LaserScan, 'scan', self.scan_callback, qos_profile=qos_profile_sensor_data)
        if hello == '3':
            self.battery_sub = self.create_subscription(BatteryState, 'battery_state', self.batter_callback, qos_profile=qos_profile_sensor_data)
        if hello == '4':
            self.timer = self.create_timer(1.0, self.timer_callback)
        if hello == '5':
            self.timer = self.create_timer(1.0, self.timer_callback)
            self.imu_sub = self.create_subscription(Imu, 'imu', self.imu_callback, qos_profile=qos_profile_sensor_data)
            self.laser_sub = self.create_subscription(LaserScan, 'scan', self.scan_callback, qos_profile=qos_profile_sensor_data)
            self.battery_sub = self.create_subscription(BatteryState, 'battery_state', self.battery_callback, qos_profile=qos_profile_sensor_data)

        self.imu_count = 0

    def imu_callback(self, msg):
        # Print IMU data
        self.get_logger().info('IMU data (linear_acceleration): x_component:{} y_component:{} z_component:{}'.format(msg.linear_acceleration.x, msg.linear_acceleration.y, msg.linear_acceleration.z), throttle_duration_sec=2)        
        self.get_logger().info('IMU data (orientation): x_component:{} y_component:{} z_component:{}'.format(msg.orientation.x, msg.orientation.y, msg.orientation.z), throttle_duration_sec=3)
        self.get_logger().info('IMU data (angular velocity): x_component:{} y_component:{} z_component:{}'.format(msg.angular_velocity.x, msg.angular_velocity.y, msg.angular_velocity.z), throttle_duration_sec=3)

    def scan_callback(self, msg):
        # Print Laser Scan data
        filtered_ranges = [r for r in msg.ranges if r>0]
        self.get_logger().info('Laser Scan data: min:{} max:{}'.format(min(filtered_ranges), max(msg.ranges)), throttle_duration_sec=3)

    def battery_callback(self, msg):
        # Print Battery State data
        self.get_logger().info('Battery State data: {} V'.format(msg.voltage), throttle_duration_sec=3)

    def timer_callback(self):
        # Print current time
        self.get_logger().info('Current time: {}'.format(datetime.datetime.now()), throttle_duration_sec=3)

def main(args=None):
    rclpy.init(args=args)
    sensor_subscriber = SensorSubscriber()
    rclpy.spin(sensor_subscriber)
    sensor_subscriber.destroy_node()
    rclpy.shutdown()

if __name__ == '__main__':
    main()
