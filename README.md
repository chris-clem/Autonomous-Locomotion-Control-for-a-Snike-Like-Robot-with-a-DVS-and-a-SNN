
# Autonomous Locomotion Control for a Snake-like Robot with a Dynamic Vision Sensor and a Spiking Neural Network

The repository for the Bachelor's Thesis in Informatics 'Autonomous Locomotion Control for a Snake-like Robot with a Dynamic Vision Sensor and a Spiking Neural Network' by Christoph Clement under the supervision of Zhenshan Bing, M.Sc. at the TU Munich.

-- **controller**: Contains the python module for the SNN controlled Locomotion of the snake and plotting scripts for the training Figures.
-- **data**: Contains h5f, csv and json files of the training and testing sessions
-- **plots**: Contains plotting scripts for the testing Figures and other Figures from the thesis and the actual testing and training Figures.
-- **V-REP_scenarios**: Contains the different V-REP scenarios.

## Abstract
How is the brain able to process vast amounts of information so energy efficient? Compared to modern Artificial Neural Networks (ANNs), the energy consumption of the brain is ten times lower - 20W in comparison to 200W. On top of that, we are still far away from imitating the brain's capabilities with ANNs.

A solution to this question might come from the third generation of ANNs - Spiking Neural Networks (SNNs) that mimic the underlying mechanism of the brain better than current ANNs. They incorporate spatial and temporal information into their calculations leading them to be more computationally and energy efficient. Especially in combination with Dynamic Vision Sensors (DVSs), they are a great fit for autonomous robots where energy efficiency and fast real-time computations are key success factors.

In this work, a SNN controller using the Reward-modulated Spike Timing Dependent Plasticity learning rule for the autonomous locomotion control of a snake-like robot is implemented. The controller is trained in a maze environment and demonstrates the ability to cope with new situations in form of different wall heights and maze angles during testing. In a real world application, such a robot could be deployed in areas with uneven terrain like in a collapsed factory building.

## Getting Started

### Prerequisites

 - Ubuntu 16.04 LTS
 - Python 2.7
 - ROS Kinetic 1.12.13
 - V-REP 3.4.0
 - NEST 2.14.0

### Installing

1. Install Ubuntu 16.04 LTS
2. Install ROS Kinetic
- Follow this guide: https://wiki.ros.org/kinetic/Installation/Ubuntu
- Make sure to use the Desktop-Full Install in step 1.4
  ```
  sudo apt-get install ros-kinetic-desktop-full
  ```  
3. Install V-REP 3.4.0
- Download
  ```
  cd ~/Downloads
  wget http://coppeliarobotics.com/files/V-REP_PRO_EDU_V3_4_0_Linux.tar.gz
  cd ~
  tar zvxf ~/Downloads/V-REP_PRO_EDU_V3_4_0_Linux.tar.gz
  ```
- Set the VREP_ROOT variable in ~/.bashrc
  ```
  echo 'export VREP_ROOT="$HOME/V-REP_PRO_EDU_V3_4_0_Linux"' >> ~/.bashrc
  source ~/.bashrc
  ```
4. Install some required Ubuntu packages
  ```
  sudo apt install git cmake python-tempita python-catkin-tools python-lxml default-jre
  ```
5. Install saxon
- Download
  ```
	cd ~/Downloads
	wget http://downloads.sourceforge.net/project/saxon/Saxon-HE/9.7/SaxonHE9-7-0-8J.zip
	cd ~
	mkdir -p saxon/bin
	cd saxon
	unzip ~/Downloads/SaxonHE9-7-0-8J.zip
	echo -e '#!/bin/sh\njava -jar "`dirname "$0"`/../saxon9he.jar" "$@"' > bin/saxon
	chmod a+x bin/saxon
  ```
- Update PATH env var with the location of saxon executable
  ```
	echo 'export PATH="$PATH:$HOME/saxon/bin"' >> ~/.bashrc
	source ~/.bashrc
  ```
6. Install v_repStubsGen (https://github.com/CoppeliaRobotics/v_repStubsGen)
  ```
	mkdir ~/python-packages
	cd ~/python-packages
	git clone --recursive https://github.com/CoppeliaRobotics/v_repStubsGen
	echo 'export PYTHONPATH="$PYTHONPATH:$HOME/python-packages"' >> ~/.bashrc
	source ~/.bashrc
  ```
7. Setup catkin workspace
  ```
	echo 'export PYTHONPATH="$PYTHONPATH:/usr/lib/python2.7/dist-packages"' >> ~/.bashrc
	source ~/.bashrc
	rm -rf ~/catkin_ws
	mkdir -p ~/catkin_ws/src
	cd ~/catkin_ws/src
	catkin_init_workspace
	cd ..
	catkin build
	source devel/setup.bash
  ```
- Copy ~/V-REP_PRO_EDU_V3_4_0_Linux/programming/ros_packages/v_repExtRosInterface to ~/catkin_ws/src
  ``` 	
	catkin build
  ```
- Copy /home/christoph/catkin_ws/devel/lib/libv_repExtRosInterface.so to ~/V-REP_PRO_EDU_V3_4_0_Linux

8. Install NEST 2.14.0 from http://www.nest-simulator.org/

## Start a training/ testing simulation

1. Start a ROS node via the terminal
	```
	roscore
	```
2. V-REP
- Start V-REP via another terminal from the V-REP foler
	```
	.\vrep.sh
	```
- Open V-REP scenario and start the V-REP simulation
3. SNN
- Set parameters in `./controller/parameters.py`. Create a subfolder for each session otherwise the data will be overwritten.
- Start training/ testing simulation by running `./controller/training.py`/ `./controller/controller.py`.
