from launch import LaunchDescription
from launch_ros.actions import Node
import os
from ament_index_python.packages import get_package_share_directory
from launch import LaunchDescription
from launch.actions import IncludeLaunchDescription
from launch.launch_description_sources import PythonLaunchDescriptionSource


def generate_launch_description():
    tbot_sim_path = get_package_share_directory('slam_toolbox')
    launch_file_dir = os.path.join(tbot_sim_path, 'launch','includes')
    tbot_start_path = get_package_share_directory('tbot_start')
    tbot_start_launch_dir = os.path.join(tbot_start_path, 'launch')
    return LaunchDescription([
    
        IncludeLaunchDescription(
            PythonLaunchDescriptionSource([tbot_start_launch_dir, '/full.launch.py']),

            ),
        
        IncludeLaunchDescription(
            PythonLaunchDescriptionSource([launch_file_dir, '/online_sync_launch.py']),

            ),
        
        
        Node(

            package = 'challenge2',
            executable='scan_echo',
            name='teleop',
            prefix='gnome-terminal -x',
        ),
        Node(

            package = 'challenge2',
            executable='tintin',
            name='teleop',
            prefix='gnome-terminal -x',
        ),
        
        Node(

            package = 'teleop_twist_keyboard',
            executable='teleop_twist_keyboard',
            name='teleop',
            prefix='gnome-terminal -x',
        ),
        Node(package='rviz2', executable='rviz2', name="rviz2", output='screen', arguments=['-d '+str('/home/bot/ros2_ws/tuto_sim/launch/oscar.rviz')]),
 
        
    ])
