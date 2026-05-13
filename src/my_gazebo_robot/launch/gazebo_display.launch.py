import os
from ament_index_python.packages import get_package_share_directory
from launch import LaunchDescription
from launch.actions import ExecuteProcess, TimerAction
from launch_ros.actions import Node

def generate_launch_description():
    pkg_dir = get_package_share_directory('my_gazebo_robot')
    urdf_file = os.path.join(pkg_dir, 'urdf', 'my_robot.urdf')

    with open(urdf_file, 'r') as f:
        robot_desc = f.read()

    # 启动 Gazebo （注意加了 -r 自动开始仿真）
    gazebo = ExecuteProcess(
        cmd=['gz', 'sim', '-r', 'empty.sdf'],
        output='screen',
        additional_env={'LIBGL_ALWAYS_SOFTWARE': '1'}
    )

    # 生成机器人（高度设为 0.2，避免车轮卡地面）
    spawn_entity = Node(
        package='ros_gz_sim',
        executable='create',
        arguments=['-name', 'my_robot',
                   '-topic', 'robot_description',
                   '-x', '0', '-y', '0', '-z', '0.2'],
        output='screen'
    )

    robot_state_pub = Node(
        package='robot_state_publisher',
        executable='robot_state_publisher',
        parameters=[{'robot_description': robot_desc}]
    )

    rviz = Node(
        package='rviz2',
        executable='rviz2',
        arguments=['-d', os.path.join(pkg_dir, 'config', 'gazebo_display.rviz')]
    )

    bridge = Node(
        package='ros_gz_bridge',
        executable='parameter_bridge',
        arguments=[
            '/cmd_vel@geometry_msgs/msg/Twist@gz.msgs.Twist',
            '/odom@nav_msgs/msg/Odometry@gz.msgs.Odometry',
            '/scan@sensor_msgs/msg/LaserScan@gz.msgs.LaserScan'
        ],
        output='screen'
    )

    return LaunchDescription([
        gazebo,
        TimerAction(period=5.0, actions=[spawn_entity]),
        robot_state_pub,
        rviz,
        bridge
    ])
