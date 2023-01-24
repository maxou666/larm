
import pyrealsense2 as rs
import numpy as np
import math
import cv2,time,sys

pipeline = rs.pipeline()
config = rs.config()
colorizer = rs.colorizer()

# fps plus bas (30)
config.enable_stream(rs.stream.depth, 640, 480, rs.format.z16, 30)
config.enable_stream(rs.stream.color, 640, 480, rs.format.bgr8, 30)

pipeline.start(config)

align_to = rs.stream.depth
align = rs.align(align_to)



color_info=(0, 0, 255)
rayon=10

count=1
refTime= time.process_time()
freq= 60


try:
    
        # This call waits until a new coherent set of frames is available on a device
        frames = pipeline.wait_for_frames()
        
        #Aligning color frame to depth frame
        aligned_frames =  align.process(frames)
        depth_frame = aligned_frames.get_depth_frame()
        aligned_color_frame = aligned_frames.get_color_frame()



        # Two ways to colorized the depth map
        # first : using colorizer of pyrealsense                
        colorized_depth = colorizer.colorize(depth_frame)
        depth_colormap = np.asanyarray(colorized_depth.get_data())
        
        # second : using opencv by applying colormap on depth image (image must be converted to 8-bit per pixel first)
        #depth_image = np.asanyarray(depth_frame.get_data())
        #depth_colormap = cv2.applyColorMap(cv2.convertScaleAbs(depth_image, alpha=0.03), cv2.COLORMAP_JET)

        # Get the intrinsic parameters
        color_intrin = aligned_color_frame.profile.as_video_stream_profile().intrinsics

        color_image = np.asanyarray(aligned_color_frame.get_data())

        depth_colormap_dim = depth_colormap.shape
        color_colormap_dim = color_image.shape

        #Use pixel value of  depth-aligned color image to get 3D axes
        x, y = int(color_colormap_dim[1]/2), int(color_colormap_dim[0]/2)
        depth = depth_frame.get_distance(x, y)
        dx ,dy, dz = rs.rs2_deproject_pixel_to_point(color_intrin, [x,y], depth)
        distance = math.sqrt(((dx)**2) + ((dy)**2) + ((dz)**2))
        print(distance)
        

except Exception as e:
    print(e)
    pass

finally:
    pipeline.stop()


