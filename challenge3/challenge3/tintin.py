import rclpy
from rclpy.node import Node
from geometry_msgs.msg import Twist
from sensor_msgs.msg import LaserScan
from sensor_msgs.msg import PointCloud
from geometry_msgs.msg import Point32
from sensor_msgs.msg import Image
from cv_bridge import CvBridge, CvBridgeError
import numpy as np
import math
import pyrealsense2 as rs
import cv2,time,sys
from std_msgs.msg import String
from tf2_msgs.msg import TFMessage
from visualization_msgs.msg import Marker
import tf2_ros
from geometry_msgs.msg import PoseStamped
from rclpy.duration import Duration


class MoveNode(Node):
    i = 0

    def __init__(self):
        super().__init__('move')
        self.velocity_publisher = self.create_publisher(Twist, '/multi/cmd_nav', 10)
        self.bouteille_publisher = self.create_publisher(String, 'bottle_detection', 10)
        self.marker = self.create_publisher(Marker, 'marker', 10)
        self.create_subscription(PointCloud, 'point', self.scan_callback, 10)
        #self.create_subscription(TFMessage, 'tf', self.coordo, 10)
        
        self.tf_buffer = tf2_ros.Buffer()
        self.tf_listener = tf2_ros.TransformListener(self.tf_buffer, self)
  
        
        self.bridge = CvBridge()
        self.create_subscription(Image, 'img', self.video, 10)
        self.rep = 0.0	

        self.premiere = [0, 1]

        self.old = 0.0
        self.old_speed = 0.0
        self.t = []
        self.i = 0
        self.av = 0.0
        self.tire = 0
        self.jevoisbouteile=0
        self.dejavu=0
        for j in range(4):
            self.premiere.append(0)
            
    
        
     
    def scan_callback(self, data):
    
        '''now = self.get_clock().now()
        dur = Duration()
        dur.sec = 40
        dur.nsec = 0

        trans = self.tf_buffer.lookup_transform('odom', 'base_link', now, dur )

        self.get_logger().info("\n")
        self.get_logger().info("Translation:")
        self.get_logger().info( "x:" + str( trans.transform.translation.x ) )
        self.get_logger().info( "y:" + str( trans.transform.translation.y ) )
        self.get_logger().info( "z:" + str( trans.transform.translation.z ) )'''
        tab_val = []
        for k in range(10):
            tab_val.append(0)

        n = len(self.premiere) - 1
        velo = Twist()
        velo.angular.z = self.rep
        
          # target a 0.2 meter per second velocity

        for j in data.points:
            if (j.x > -0.05 and j.x < 0.17 and j.y < 0.2 and j.y > -0.2):
                tab_val[0] += 1
            if (j.x > -0.15 and j.x < 0.17 and j.y < 0.0 and j.y > -0.30):
                tab_val[1] += 1
            if (j.x > -0.15 and j.x < 0.17 and j.y < 0.30 and j.y > -0.0):
                tab_val[2] += 1

            if (j.x > 0.15 and j.x < 0.4 and j.y < 0.2 and j.y > -0.2):
                tab_val[3] += 1
            if (j.x > 0.15 and j.x < 0.4 and j.y < 0.0 and j.y > -0.30):
                tab_val[4] += 1
            if (j.x > 0.15 and j.x < 0.4 and j.y < 0.30 and j.y > -0.0):
                tab_val[5] += 1

            if (j.x > 0.4 and j.x < 0.8 and j.y < 0.2 and j.y > -0.2):
                tab_val[6] += 1
            if (j.x > 0.4 and j.x < 0.8 and j.y < 0.0 and j.y > -0.30):
                tab_val[7] += 1
            if (j.x > 0.4 and j.x < 0.8 and j.y < 0.30 and j.y > -0.0):
                tab_val[8] += 1

        if (tab_val[0] > 30):

            velo.linear.x = 0.0  # target a 0 meter per second velocity
            if (tab_val[2] < tab_val[1] and velo.angular.z >= 0.0):
                velo.angular.z = 1.0
                self.rep = 1.0

            elif (tab_val[2] >= tab_val[1] and velo.angular.z <= 0.0):
                velo.angular.z = -1.0
                self.rep = -1.0


        elif (tab_val[3] > 30):


            if (tab_val[5] < tab_val[4] and velo.angular.z >= 0.0):
                velo.angular.z = 0.6
                self.rep = 0.6

            elif (tab_val[5] >= tab_val[4] and velo.angular.z <= 0.0):
                velo.angular.z = -0.6
                self.rep = -0.6

        elif (tab_val[6] > 30):

            velo.linear.x = 0.3  # target a 0 meter per second velocity
            if (tab_val[8] < tab_val[7] and velo.angular.z != 1.0 and velo.angular.z != -1.0):
                velo.angular.z = 0.3
                self.rep = 0.3

            elif (tab_val[8] >= tab_val[7] and velo.angular.z != 1.0 and velo.angular.z != -1.0):
                velo.angular.z = -0.3
                self.rep = -0.3


        else:

            velo.angular.z = 0.0

        self.rep = velo.angular.z
        if (self.jevoisbouteile ==0):
            self.velocity_publisher.publish(velo)

    def video(self, data):
    
        velo = Twist()
        velo.angular.z = 0.0
        velo.linear.x = 0.0  # target a 0.2 meter per second velocity
        msg= String()
        self.t = []
        self.r = []
        for i in range(3):
            self.t.append(0)
            self.r.append(0)
        self.i = 0
        self.j = 0
        self.av = 0
        try:
            cv_image = self.bridge.imgmsg_to_cv2(data, "bgr8")
        except CvBridgeError as e:
            print(e)

        hsv = cv2.cvtColor(cv_image, cv2.COLOR_BGR2HSV)

        # define range of orange color in HSV
        lower_orange = (8, 220, 210)
        upper_orange = (15, 255, 255)
        lower_red = (0, 10, 120)
        upper_red = (40, 50, 160)
        upper_orange = (15, 255, 255)
        lower_noir = (90, 100, 80)
        upper_noir = (140, 140, 140)
        lower_blanc = (220, 220, 220)
        upper_blanc = (255, 255, 255)
        # Threshold the HSV image to get only orange colors

        mask = cv2.inRange(hsv, lower_orange, upper_orange)
        kernel = np.ones((3, 3), np.uint8)
        mask = cv2.erode(mask, kernel, iterations=1)
        mask = cv2.dilate(mask, kernel, iterations=1)
        image2 = cv2.bitwise_and(cv_image, cv_image, mask=mask)
        mask_red = cv2.inRange(cv_image, lower_red, upper_red)
     

        mask_noir = cv2.inRange(cv_image, lower_noir, upper_noir)
        # Bitwise-AND mask and original image
        res = cv2.bitwise_and(cv_image, cv_image, mask=mask)
        res_red = cv2.bitwise_and(cv_image, cv_image, mask=mask_red)
        res_noir = cv2.bitwise_and(cv_image, cv_image, mask=mask_noir)
        # dilatation
        kernel = np.ones((7, 7), np.uint8)
        img_erosion = cv2.dilate(res, kernel, iterations=1)
        img_erosion_red = cv2.dilate(res_red, kernel, iterations=1)
        img_erosion_noir = cv2.dilate(res_noir, kernel, iterations=1)

        imgray = cv2.cvtColor(img_erosion, cv2.COLOR_BGR2GRAY)
        imgray_red = cv2.cvtColor(img_erosion_red, cv2.COLOR_BGR2GRAY)
        imgray_noir = cv2.cvtColor(img_erosion_noir, cv2.COLOR_BGR2GRAY)

        ret, thresh = cv2.threshold(imgray, 0, 255, cv2.THRESH_BINARY)
        ret1, thresh1 = cv2.threshold(imgray_red, 0, 255, cv2.THRESH_BINARY)
        ret2, thresh2 = cv2.threshold(imgray_noir, 0, 255, cv2.THRESH_BINARY)

        gray_casc = cv2.cvtColor(cv_image, cv2.COLOR_BGR2GRAY)

        contours, hierarchy = cv2.findContours(thresh, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
        contours1, hierarchy1 = cv2.findContours(thresh1, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
        contours2, hierarchy2 = cv2.findContours(thresh2, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
        bilateral_filtered_image = cv2.bilateralFilter(cv_image, 5, 175, 175)
        cv2.drawContours(cv_image, contours, -1, (0, 255, 0), thickness=cv2.FILLED)
       
        # approximation des contours, pas viable..
        count = 0  # result

        bilateral_filtered_image = cv2.bilateralFilter(cv_image, 5, 175, 175)

        edge_detected_image = cv2.Canny(bilateral_filtered_image, 75, 200)

        contoursi, hierarchy = cv2.findContours(edge_detected_image, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)

        contour_list = []
        for contour in contours2:
            approx = cv2.approxPolyDP(contour, 0.01 * cv2.arcLength(contour, True), True)
            area = cv2.contourArea(contour)
            if ((len(approx) > 8) & (len(approx) < 23) & (area > 30)):
                contour_list.append(contour)


        dimensions = cv_image.shape
        rows = cv_image.shape[0]
        cols = cv_image.shape[1]
        try:

            sume = 0
            taille = len(contours)

            for i in range(taille):
                sume += contours[0][0][0][1]
            # print(taille,sume,int(sume/taille))
            delta = int(sume / taille)

        except:
            delta = int(2 * (rows - 1) / 3)
        # fixer ligne ?
        for x in range(1):
            for y in range(cols):

                if (cv_image[delta, y][0] == 0 and cv_image[delta, y][1] == 255 and cv_image[delta, y][2] == 0):

                    self.t[1] += 1
                    self.i = 1
                elif (self.i == 0):
                    self.t[0] += 1
                else:
                    self.t[2] += 1
                if (cv_image[delta, y][0] == 255 and cv_image[delta, y][1] == 0 and cv_image[delta, y][2] == 0):

                    self.r[1] += 1
                    self.j = 1
                elif (self.j == 0):
                    self.r[0] += 1
                else:
                    self.r[2] += 1
        if (self.t[1]>=10):
            self.jevoisbouteile=1
        else:
            self.jevoisbouteile=0
        if (self.t[1] >= 10 and self.t[0] < (self.t[2] - 20 - self.t[1])):
            # deplace robot ??gauch
            # print("tourne a gauche")
            print("bouteille orange ?")
            velo.angular.z=0.3

            msg.data="bouteille orange ?"
        elif (self.t[1] >= 10 and self.t[0] > (self.t[2] + 20 + self.t[1])):
            # print("tourne a doite")
            print("bouteille orange ?")
            msg.data = "bouteilleorange"
            velo.angular.z=-0.3

            # deplace robot ?? droite

        elif (self.t[1] > 10):
            # print("tire")
            print("bouteille orange ?")
            msg.data="bouteilleorange"
            self.tire = 1
            for y in range(cols):

                if ((cv_image[-1, y][0] == 0 and cv_image[-1, y][1] == 255 and cv_image[-1, y][2] == 0) or (cv_image[-2, y][0] == 0 and cv_image[-2, y][1] == 255 and cv_image[-2, y][2] == 0) or (cv_image[-3, y][0] == 0 and cv_image[-3, y][1] == 255 and cv_image[-3, y][2] == 0)):
                    self.av += 1
            if (self.av > 10):
                print("bouteille orange ?")
                velo.linear.x=0.0
                print("LA bouteille est ?? une distance de 30cm")
                velo.angular.z=0.3
                self.dejavu=99
               
                	
                
            else:
                msg.data = "bouteilleorange "
                

        if (self.r[1] > 10):
            print("bouteille rouge ?")
            msg.data = "bouteillerouge"

            # calculer depth du point central
            # retransformer la couleur en distance
        else:
            self.old = 0.0
        #self.bouteille_publisher.publish(msg)
        if (self.jevoisbouteile ==1):
            self.velocity_publisher.publish(velo)

        hsvt = cv2.cvtColor(cv_image, cv2.COLOR_BGR2HSV)
        cv2.imshow('eza', cv_image)
        cv2.waitKey(3)

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