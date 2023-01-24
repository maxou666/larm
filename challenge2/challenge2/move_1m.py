import rclpy
from rclpy.node import Node
from geometry_msgs.msg import Twist
class MoveNode(Node):

    i=0
    def __init__(self):
        super().__init__('move')
        self.velocity_publisher = self.create_publisher(Twist, '/multi/cmd_nav', 10)
        self.timer = self.create_timer(0.1, self.activate) # 0.1 seconds to target a frequency of 10 hertz
       
    	
    def activate(self):
        if(self.i<50):
        	velo = Twist()
        	velo.linear.x = 0.2 # target a 0.2 meter per second velocity
        	self.velocity_publisher.publish(velo)
        	self.i=self.i+1
        	self.get_logger().info( f" j'avance")
            

def main(args=None):
    rclpy.init(args=args)
    move = MoveNode()


    # Start the ros infinit loop with the move node.
    
    rclpy.spin(move)


    # At the end, destroy the node explicitly.
    move.destroy_node()

    # and shut the light down.
    rclpy.shutdown()

if __name__ == '__main__':
    main()
