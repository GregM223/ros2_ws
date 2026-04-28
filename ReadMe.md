	requirements:
Docker with ros2_turtlebot3 image available
ubuntu 22.04 or other compatible OS
the given workspace cloned to your pc
	
	Setup
clone this repository with:
git clone #repo_url#
cd #repo_folder#
	
Start the docker container, this can differ depending on how you have set docker up, but the command used for this project was:
docker run -it --rm --privileged --net=host --env=DISPLAY --env=QT_X11_NO_MITSHM=1 -v /tmp/.X11-unix:/tmp/.X11-unix -v /path/to/ros2_ws:/home/student/ros2_ws ros2_turtlebot3:V1.7

Build the workspace with:
cd ~/ros2_ws
colcon build --symlink-install
source install/setup.bash

P1: Run the mapping stack with:
ros2 launch my_robot_controller start_mapping.launch.py

P2: Run the navigation stack with:
ros2 launch my_robot_controller run_navigation.launch.py
