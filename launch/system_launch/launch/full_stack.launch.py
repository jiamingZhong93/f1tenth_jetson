from ament_index_python.packages import get_package_share_directory
from launch import LaunchDescription
from launch.actions import DeclareLaunchArgument, IncludeLaunchDescription, GroupAction
from launch.conditions import IfCondition
from launch.launch_description_sources import PythonLaunchDescriptionSource
from launch.substitutions import LaunchConfiguration
from launch_ros.actions import Node
import os


def generate_launch_description():
    system_launch_share = get_package_share_directory('system_launch')
    enable_realsense = LaunchConfiguration('enable_realsense')

    lakibeam_launch = os.path.join(
        get_package_share_directory('lakibeam1'),
        'launch',
        'lakibeam1_scan.launch.py'
    )

    f1tenth_launch = os.path.join(
        get_package_share_directory('f1tenth_stack'),
        'launch',
        'no_lidar_bringup_launch.py'
    )

    realsense_launch = os.path.join(
        get_package_share_directory('realsense2_camera'),
        'launch',
        'rs_launch.py'
    )

    rviz_config = os.path.normpath(os.path.join(
        system_launch_share,
        '..', '..', '..', '..',
        'src', 'launch', 'rviz', 'basic.rviz'
    ))

    return LaunchDescription([
        DeclareLaunchArgument(
            'enable_realsense',
            default_value='true',
            description='Start the optional Intel RealSense D436 camera and image republisher.',
        ),

        GroupAction(
            scoped=True,
            actions=[
                IncludeLaunchDescription(
                    PythonLaunchDescriptionSource(lakibeam_launch)
                ),
            ],
        ),

        GroupAction(
            scoped=True,
            actions=[
                IncludeLaunchDescription(
                    PythonLaunchDescriptionSource(f1tenth_launch)
                ),
            ],
        ),

        GroupAction(
            scoped=True,
            condition=IfCondition(enable_realsense),
            actions=[
                IncludeLaunchDescription(
                    PythonLaunchDescriptionSource(realsense_launch),
                    launch_arguments={
                        'camera_name': 'd436',
                        'camera_namespace': 'camera',
                        'enable_color': 'true',
                        'enable_depth': 'false',
                        'enable_gyro': 'false',
                        'enable_accel': 'false',
                        'unite_imu_method': '2',
                        'enable_sync': 'false',
                        'align_depth.enable': 'false',
                        'pointcloud.enable': 'false',
                        'depth_module.depth_profile': '640x480x30',
                        'rgb_camera.color_profile': '640x480x30',
                    }.items(),
                ),
            ],
        ),

        GroupAction(
            scoped=True,
            condition=IfCondition(enable_realsense),
            actions=[
                Node(
                    package='image_transport',
                    executable='republish',
                    name='d436_color_compressed_republisher',
                    arguments=['raw', 'compressed'],
                    remappings=[
                        ('in', '/camera/d436/color/image_raw'),
                        ('out/compressed', '/rviz/d436/color/image_raw/compressed'),
                    ],
                    output='screen',
                ),
            ],
        ),

        # Node(
        #     package='rviz2',
        #     executable='rviz2',
        #     name='rviz2',
        #     arguments=['-d', rviz_config],
        #     output='screen',
        # ),
    ])