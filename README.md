# my_project

ROS2 package for F1TENTH development on Jetson.

## Build

```bash
cd ~/F1Tenth/f1tenth_ws
colcon build --symlink-install
source install/setup.bash
```

## Run
```bash
ros2 launch system_launch full_stack.launch.py
```

The RealSense D436 is optional and enabled by default. If you want to disable it, run:

```bash
ros2 launch system_launch full_stack.launch.py enable_realsense:=false
```

