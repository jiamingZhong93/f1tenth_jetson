from ament_index_python.packages import get_package_share_directory
from launch import LaunchDescription
from launch.actions import IncludeLaunchDescription, GroupAction
from launch.launch_description_sources import PythonLaunchDescriptionSource
from launch_ros.actions import Node
import os


def generate_launch_description():
    system_launch_share = get_package_share_directory('system_launch')

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
            actions=[
                IncludeLaunchDescription(
                    PythonLaunchDescriptionSource(realsense_launch),
                    launch_arguments={
                        'camera_name': 'd436',
                        'camera_namespace': 'camera',
                        'enable_color': 'true',
                        'enable_depth': 'true',
                        'enable_gyro': 'true',
                        'enable_accel': 'true',
                        'unite_imu_method': '2',
                        'enable_sync': 'true',
                        'align_depth.enable': 'true',
                        'pointcloud.enable': 'false',
                        'depth_module.depth_profile': '640x480x30',
                        'rgb_camera.color_profile': '640x480x30',
                    }.items(),
                ),
            ],
        ),

        GroupAction(
            scoped=True,
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