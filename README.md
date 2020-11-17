# raspi_ros

A package that provides ROS-based interfaces to the digital outputs/inputs of a Raspberry P

# Quick How-to

First of all, navigate to the `src` directory in your ROS workspace. Then execute the following commands:
```
git clone https://github.com/ReconCycle/raspi_ros
wstool init
wstool merge raspi_ros/dependencies.rosinstall
wstool up
rosdep install --from-paths . --ignore-src --rosdistro kinetic
catkin build
source devel/setup.bash
```


