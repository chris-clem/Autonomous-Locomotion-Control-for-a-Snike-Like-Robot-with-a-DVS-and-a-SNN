#!/bin/bash
gnome-terminal --tab -e "bash -c \"roscore; exec bash\"" --tab -e "bash -c \"cd ~/V-REP_PRO_EDU_V3_4_0_Linux;./vrep.sh $1 -s; exec bash\""
