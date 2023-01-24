#!python3
import rclpy
from rclpy.node import Node
from geometry_msgs.msg import Twist
from sensor_msgs.msg import LaserScan
from sensor_msgs.msg import PointCloud
from sensor_msgs.msg import Image
from geometry_msgs.msg import Point32
import math

class MoveNode(Node):

    i=0
    def __init__(self):
        super().__init__('move')
        self.velocity_publisher = self.create_publisher(Twist, '/multi/cmd_nav', 10)
        self.create_subscription( PointCloud, 'point', self.scan_callback,10)
        self.old =0.0

        self.premiere=[0,1]
        for j in range(4):
        	self.premiere.append(0)

       
    	
    def scan_callback(self,data):
            tab_val=[]
            for k in range(10):
            	tab_val.append(0)                    	
          
            self.get_logger().info(f"{len(self.premiere)}")
            n=len(self.premiere)-1	
            velo = Twist()
            velo.angular.z=self.old
            velo.linear.x = 0.3 # target a 0.2 meter per second velocity

            
            for j in data.points:
            	if( j.x>-0.05 and j.x < 0.17 and j.y < 0.2 and j.y > -0.2):
            		tab_val[0]+=1
            	if( j.x>-0.15 and j.x < 0.17 and j.y < 0.0 and j.y > -0.30):
            		tab_val[1]+=1
            	if( j.x>-0.15 and j.x < 0.17 and j.y < 0.30 and j.y > -0.0):
            		tab_val[2]+=1
		    		
            	if( j.x>0.15 and j.x < 0.4 and j.y < 0.2 and j.y > -0.2):
            		tab_val[3]+=1
            	if( j.x>0.15 and j.x < 0.4 and j.y < 0.0 and j.y > -0.30):
            		tab_val[4]+=1
            	if( j.x>0.15 and j.x < 0.4 and j.y < 0.30 and j.y > -0.0):
            		tab_val[5]+=1
		    	
            	if( j.x>0.4 and j.x < 0.8 and j.y < 0.2 and j.y > -0.2):
            		tab_val[6]+=1
            	if( j.x>0.4 and j.x < 0.8 and j.y < 0.0 and j.y > -0.30):
            		tab_val[7]+=1
            	if( j.x>0.4 and j.x < 0.8 and j.y < 0.30 and j.y > -0.0):
            		tab_val[8]+=1
                
            if(tab_val[0]>30):
            	
            	
            	velo.linear.x = 0.0 # target a 0 meter per second velocity
            	self.get_logger().info( f"{velo.angular.z} import")
            	if (tab_val[2]<tab_val[1] and velo.angular.z>=0.0):
            		velo.angular.z = 1.0
            		self.old=1.0
            		
            	elif (tab_val[2]>=tab_val[1] and velo.angular.z<=0.0):
            		velo.angular.z = -1.0
            		self.old=-1.0
            		
            		
            elif(tab_val[3]>30):
            	

            	velo.linear.x = 0.2 # target a 0 meter per second velocity
            	self.get_logger().info( f"{velo.angular.z} import")
            	if (tab_val[5]<tab_val[4] and velo.angular.z>=0.0):
            		velo.angular.z = 0.6
            		self.old=0.6
            		
            	elif (tab_val[5]>=tab_val[4] and velo.angular.z<=0.0):
            		velo.angular.z = -0.6
            		self.old=-0.6
            		
            elif(tab_val[6]>30):
            	

            	velo.linear.x = 0.3 # target a 0 meter per second velocity
            	self.get_logger().info( f"{velo.angular.z} import")
            	if (tab_val[8]<tab_val[7] and velo.angular.z!=1.0 and velo.angular.z!=-1.0):
            		velo.angular.z = 0.3
            		self.old=0.3
            		
            	elif (tab_val[8]>=tab_val[7] and velo.angular.z!=1.0 and velo.angular.z!=-1.0):
            		velo.angular.z = -0.3
            		self.old=-0.3
            		
            		
            else:

            	velo.angular.z=0.0    

            	self.get_logger().info( f"{velo.angular.z} j'avance")
            self.old=velo.angular.z           	        		
            self.velocity_publisher.publish(velo)
            self.get_logger().info( f"{velo.angular.z}")

             	
            	              		

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
