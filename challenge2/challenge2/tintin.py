
from sensor_msgs.msg import Image
from cv_bridge import CvBridge, CvBridgeError

import rclpy
from rclpy.node import Node
from geometry_msgs.msg import Twist
from sensor_msgs.msg import LaserScan
from sensor_msgs.msg import PointCloud
from geometry_msgs.msg import Point32
import numpy as np
import math
import pyrealsense2 as rs
import cv2,time,sys





class OrangeObjectRecognition(Node):
    def __init__(self):
        super().__init__('move')
        self.bridge = CvBridge()
        self.create_subscription( Image, 'img', self.callback,10)

        self.velocity_publisher = self.create_publisher(Twist, '/multi/cmd_nav', 10)
        self.old =0.0  
        self.old_speed=0.0                  
        self.t=[]
        self.i=0
        self.av=0.0
        self.tire =0
        
                   
    def callback(self, data):
        velo = Twist()
        velo.angular.z=self.old 
        velo.linear.x =self.old_speed  
        self.t =[]
        self.r = []
        for i in range(3):
            self.t.append(0) 
            self.r.append(0) 
        self.i=0 
        self.j=0 
        self.av=0       
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
        mask=cv2.erode(mask, kernel, iterations=1)
        mask=cv2.dilate(mask, kernel, iterations=1)
        image2=cv2.bitwise_and(cv_image, cv_image, mask= mask)
        mask_red = cv2.inRange(cv_image, lower_red, upper_red) 
        mask_noir = cv2.inRange(cv_image, lower_noir, upper_noir)               
        # Bitwise-AND mask and original image
        res = cv2.bitwise_and(cv_image, cv_image, mask= mask)
        res_red = cv2.bitwise_and(cv_image, cv_image, mask= mask_red)
        res_noir = cv2.bitwise_and(cv_image, cv_image, mask= mask_noir)
        #dilatation 
        kernel = np.ones((7, 7), np.uint8)
        img_erosion = cv2.dilate(res, kernel, iterations=1)
        img_erosion_red = cv2.dilate(res_red, kernel, iterations=1) 
        img_erosion_noir = cv2.dilate(res_noir, kernel, iterations=1)     
             
        imgray = cv2.cvtColor(img_erosion, cv2.COLOR_BGR2GRAY)
        imgray_red = cv2.cvtColor(img_erosion_red, cv2.COLOR_BGR2GRAY)
        imgray_noir = cv2.cvtColor(img_erosion_noir, cv2.COLOR_BGR2GRAY)
        
        ret, thresh = cv2.threshold(imgray,0,255,cv2.THRESH_BINARY)
        ret1, thresh1 = cv2.threshold(imgray_red,0,255,cv2.THRESH_BINARY)
        ret2, thresh2 = cv2.threshold(imgray_noir,0,255,cv2.THRESH_BINARY)
                
        gray_casc = cv2.cvtColor(cv_image, cv2.COLOR_BGR2GRAY)
        
        contours, hierarchy = cv2.findContours(thresh, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)   
        contours1, hierarchy1 = cv2.findContours(thresh1, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)   
        contours2, hierarchy2 = cv2.findContours(thresh2, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)   
        bilateral_filtered_image = cv2.bilateralFilter(cv_image, 5, 175, 175)
        cv2.drawContours(cv_image, contours, -1, (0, 255, 0), thickness=cv2.FILLED)
        cv2.drawContours(cv_image, contours1, -1, (255, 0, 0), thickness=cv2.FILLED)
        cv2.drawContours(cv_image, contours2, -1, (0, 0, 255), thickness=cv2.FILLED)
        # approximation des contours, pas viable..
        count = 0 #result

	

        bilateral_filtered_image = cv2.bilateralFilter(cv_image, 5, 175, 175)
      

        edge_detected_image = cv2.Canny(bilateral_filtered_image, 75, 200)
       
        contoursi, hierarchy = cv2.findContours(edge_detected_image, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
        
        contour_list = []
        for contour in contoursi:
            approx = cv2.approxPolyDP(contour,0.01*cv2.arcLength(contour,True),True)
            area = cv2.contourArea(contour)
            if ((len(approx) > 8) & (len(approx) < 23) & (area > 30) ):
               contour_list.append(contour)

        cv2.drawContours(cv_image, contour_list,  -1, (255,255,0), 2)
        dimensions = cv_image.shape
        rows=cv_image.shape[0]
        cols = cv_image.shape[1]
        try:
        
           
            sume=0
            taille= len(contours)

            for i in range(taille):
               sume+=contours[0][0][0][1]
            #print(taille,sume,int(sume/taille))   
            delta=int(sume/taille)

        except:
            delta= int(2*(rows-1)/3)
        #fixer ligne ?
        for x in range(1):
            for y in range(cols):
		
               if(cv_image[delta,y][0]==0 and cv_image[delta,y][1]==255 and cv_image[delta,y][2]==0):

                   self.t[1]+=1
                   self.i=1
               elif(self.i==0):
                   self.t[0]+=1               
               else:
                   self.t[2]+=1
               if(cv_image[delta,y][0]==255 and cv_image[delta,y][1]==0 and cv_image[delta,y][2]==0):

                   self.r[1]+=1
                   self.j=1
               elif(self.j==0):
                   self.r[0]+=1               
               else:
                   self.r[2]+=1
                   
                          
               
        if(self.t[1]>=10 and self.t[0]<(self.t[2]-20-self.t[1])):
            #deplace robot àgauch
            #print("tourne a gauche")
            self.old = 0.5
            velo.angular.z = 0.5
            velo.linear.x=0.0 
            print("bouteille orange ?")
        elif(self.t[1]>=10 and self.t[0]>(self.t[2]+20+self.t[1])):                     
            #print("tourne a doite")
            self.old = -0.5
            velo.angular.z = -0.5
            velo.linear.x=0.0 
            #deplace robot à droite               

        elif(self.t[1]>10):
            #print("tire")
            self.tire=1
            self.old = 0.0
            velo.angular.z = 0.0
            for y in range(cols):
            
               velo.linear.x=0.0 
               if(cv_image[-1,y][0]==0 and cv_image[-1,y][1]==255 and cv_image[-1,y][2]==0): 
               	self.av+=1
            if(self.av>10):
               velo.linear.x=0.0                              
            #else:
                   
             #  velo.linear.x=0.2    

        if( self.r[1]>10 ):
            print("bouteille rouge ?")  
            
            #calculer depth du point central
            #retransformer la couleur en distance
        else:
            self.old = 0.0
            velo.angular.z = 0.0 
            
        self.velocity_publisher.publish(velo)  
        self.old_speed = velo.linear.x 
        hsvt = cv2.cvtColor(cv_image, cv2.COLOR_BGR2HSV)                   	
        cv2.imshow('eza', cv_image)
        cv2.waitKey(3)
        
def main(args=None):
    rclpy.init(args=args)
    
    move =OrangeObjectRecognition()


    # Start the ros infinit loop with the move node.
    
    rclpy.spin(move)


    # At the end, destroy the node explicitly.
    move.destroy_node()

    # and shut the light down.
    rclpy.shutdown()

if __name__ == '__main__':
    main()

    

