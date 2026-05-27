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
$ ros2 launch my_robot_controller start_mapping.launch.py

P2: Run the navigation stack with:
$ ros2 launch my_robot_controller run_navigation.launch.py

P3: For Autoware navigation, first ensure ~/autoware_map/sample-map-planning exists, then start the Autoware Docker:
xhost +local:docker

docker run -it --rm --privileged --net=host --env=DISPLAY
--env=QT_X11_NO_MITSHM=1 -v /tmp/.X11-unix:/tmp/.X11-unix -v
/home/autolab/ros2_ws:/ros2_ws -v
/home/autolab/autoware_map:/autoware_map --workdir /ros2_ws
mohsen_aw:full bash

Then build, source and launch:
colcon build --symlink-install
source /ros2_ws/setup.bash
ros2 launch my_robot_controller car_nav.launch.py

Before building for P3, the turtlebot packages must be ignored. Run the following on your host machine:

touch ~/ros2_ws/src/turtlebot3/COLCON_IGNORE
touch ~/ros2_ws/src/turtlebot3_simulations/COLCON_IGNORE

To revert back to P1/P2, remove these files:

rm ~/ros2_ws/src/turtlebot3/COLCON_IGNORE
rm ~/ros2_ws/src/turtlebot3_simulations/COLCON_IGNORE


P4: AV Validation

Designed and simulated an interactive traffic scenario using Autoware Scenario Simulator V2.
The scenario involves an Ego vehicle navigating a four-way intersection with two NPC vehicles
crossing perpendicular to its path.

The scenario YAML file is located in the `scenario/` folder.
