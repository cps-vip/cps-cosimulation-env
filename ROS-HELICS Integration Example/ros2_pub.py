import rclpy
from rclpy.node import Node
from std_msgs.msg import String

class Publisher(Node):

    def __init__(self):
        super().__init__('ros_publisher')
        # datacomm is the topic name
        self.publisher_ = self.create_publisher(String, 'datacomm', 10)
        timer_period = 0.5  # seconds
        self.timer = self.create_timer(timer_period, self.timer_callback)
        self.i = 0

    def timer_callback(self):
        msg = String()
        msg.data = 'HELLO HELICS'
        self.publisher_.publish(msg)
        self.get_logger().info('Publishing: "%s"' % msg.data)

def main(args=None):
    rclpy.init(args=args)

    ros_publisher = Publisher()

    rclpy.spin(ros_publisher)

    ros_publisher.destroy_node()
    rclpy.shutdown()

if __name__ == '__main__':
    main()