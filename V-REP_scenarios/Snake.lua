-- Childscript of the snake that implements the slithering gait equation.

function calculate_travelled_distance(travelled_distance, position_old, position)
  -- Calculate the traveled distance of the snake.
  delta_x = position[1] - position_old[1]
  delta_y = position[2] - position_old[2]
  delta_z = position[3] - position_old[3]

  delta_distance = (delta_x^2 + delta_y^2 + delta_z^2)^0.5
  travelled_distance = travelled_distance + delta_distance
  return travelled_distance
end

function setTurningRadius_cb(msg)
  -- Turning Radius subscriber callback
  radius = msg.data

  -- Update the body shape offset C with the radius
  C = 0
  if (radius >= 1 or radius <= -1) then
    C = l/(N*radius)
  end
end

function resetRobot_cb(msg)
  -- Reset robot subscriber callback

  -- Publish travelled_distance and steps
  simExtRosInterface_publish(travelledDistancePub, {data=travelled_distance})
  simExtRosInterface_publish(stepsPub, {data=step})

  -- Get all objects in the model
  allModelObjects=simGetObjectsInTree(robotHandle)

  simSetThreadAutomaticSwitch(false)

  -- Reset all objects in the model to their initial position
  for i=1,#allModelObjects,1 do
    simResetDynamicObject(allModelObjects[i])
  end

  for i=1,N,1 do
    simSetJointPosition(joints_v[i], 0)
    simSetJointTargetPosition(joints_v[i], 0)
  end

  -- Set travel direction
  if (msg.data == true) then
    ori = {0.0, 0.0, math.pi}
  else
    ori = {0.0, 0.0, 0.0}
  end

  simSetObjectPosition(robotHandle, -1, init_pos)
  simSetObjectOrientation(robotHandle, -1, ori)

  simSetThreadAutomaticSwitch(true)

  -- reset t, step, position, travelled_distance
  t = 0
  step = 0
  position_old = simGetObjectPosition(robotHandle,-1)
  position = simGetObjectPosition(robotHandle,-1)
  travelled_distance = 0

  -- Debug comments for the console from which V-REP is started
  if (comments == true) then
    print("----------Reset Snake-----------")
    for i=1,#init_pos,1 do
      print("init_pos["..(i).."]:", init_pos[i])
    end
    for i=1,#ori,1 do
      print("ori["..(i).."]:", ori[i])
    end
    print("msg.data:\t", msg.data)
    print("travelled_distance:\t", travelled_distance)
    print("--------------------------------")
  end
end

if (sim_call_type==sim_childscriptcall_initialization) then
  -- Get object handles
  robotHandle=simGetObjectAssociatedWithScript(sim_handle_self)

  joints_v={-1,-1,-1,-1,-1,-1,-1,-1}
  for i=1,8,1 do
      joints_v[i]=simGetObjectHandle('Snake_vJoint_'..(i))
  end

  distanceHandle1=simGetDistanceHandle('Distance_Snake_Wall_1')
  distanceHandle2=simGetDistanceHandle('Distance_Snake_Wall_2')

  -- Get init position and orientation
  init_pos = simGetObjectPosition(robotHandle, -1)
  init_ori = simGetObjectOrientation(robotHandle, -1)

  -- Check if the required ROS plugin is there:
  moduleName=0
  moduleVersion=0
  index=0
  pluginNotFound=true

  while moduleName do
    moduleName,moduleVersion=simGetModuleName(index)
    if (moduleName=='RosInterface') then
      pluginNotFound=false
    end
    index=index+1
  end

  -- Prepare DVS handle
  cameraHandle=simGetObjectHandle('DVS_128')

  showConsole=simGetScriptSimulationParameter(sim_handle_self,'showConsole')
  if (showConsole) then
      auxConsole=simAuxiliaryConsoleOpen("DVS128 output",500,4)
  end

  showCameraView=simGetScriptSimulationParameter(sim_handle_self,'showCameraView')
  if (showCameraView) then
      floatingView=simFloatingViewAdd(0.2,0.8,0.4,0.4,0)
      simAdjustView(floatingView,cameraHandle,64)
  end

  if (not pluginNotFound) then
    -- Set up the ROS Publisher and Subscriber
    dvsPub=simExtRosInterface_advertise('/dvsData', 'std_msgs/Int8MultiArray')
    transformPub=simExtRosInterface_advertise('/transformData', 'geometry_msgs/Transform')
    turnRadiusSub=simExtRosInterface_subscribe('/turningRadius','std_msgs/Float32','setTurningRadius_cb')
    resetRobotSub=simExtRosInterface_subscribe('/resetRobot','std_msgs/Bool','resetRobot_cb')
    paramsPub=simExtRosInterface_advertise('/parameters', 'std_msgs/String')
    distancePub=simExtRosInterface_advertise('/distances', 'std_msgs/Float32MultiArray')
    travelledDistancePub=simExtRosInterface_advertise('/travelledDistance','std_msgs/Float32')
    stepsPub=simExtRosInterface_advertise('/steps','std_msgs/Float32')
  end

  -- Initialize parameters
  step = 0
  t = 0
  comments = simGetScriptSimulationParameter(sim_handle_self, "comments")
  mod = simGetScriptSimulationParameter(sim_handle_self, "mod")
  radius =  simGetScriptSimulationParameter(sim_handle_self, "r")

  -- For travelled distance calculation
  position_old = simGetObjectPosition(robotHandle,-1)
  position = simGetObjectPosition(robotHandle,-1)
  travelled_distance = 0

  -- Number of segments of the snake minus the head
  N = 8

  -- Length of a segment of the snake
  local l0 = simGetScriptSimulationParameter(sim_handle_self, "l0")

  -- Linear reduction parameters (set y = 0 and z = 1 for disabling)
  y = simGetScriptSimulationParameter(sim_handle_self, "y")
  z = 1 - y

  -- Set of control Parameters
  -- w: temporal frequency: traveling speed of the wave
  w = math.pi*simGetScriptSimulationParameter(sim_handle_self, "w")
  -- A: Amplitude
  A = math.pi*simGetScriptSimulationParameter(sim_handle_self, "A")/180
  -- Omega: spatial frequency: cycle number of the wave
  Omega = math.pi*simGetScriptSimulationParameter(sim_handle_self, "Omega")/180
  -- For damping
  p = -1

  -- Theta k: joint angle --> theta[i]
  local theta = {0,-1,-1,-1,-1,-1,-1,-1,-1}
  -- Theta snake: global angle of the snake robot --> head_dir
  local head_dir = 0

  -- Snake locomotion
  for i=1, N, 1 do
    -- Linear reduction equation P = ((n/N)*z+y) e [0,1], for all n e [0,N]
    P = ((i-1)/N)*y + z
    -- Gait equation
    theta[i+1] = theta[i] + P*A*math.sin(Omega * (i-1))

    head_dir = head_dir + theta[i+1]
  end

  head_dir = head_dir/(N+1)

  -- Calculate effective segment length
  l = 0;
  for i=1,N+1,1 do
    l = l + math.cos(theta[i] - head_dir)
  end
  l = l0 * l;

  if (radius ~= 0) then
    C = l/(N*radius)
  else
    C = 0
  end

  -- Debug comments
  if (comments == true) then
    print("------Snake initialization------")
    for i=1,#init_pos,1 do
        print("init_pos["..(i).."]:", init_pos[i])
    end
    for i=1,#init_ori,1 do
        print("init_ori["..(i).."]:", init_ori[i])
    end
    print("w:\t", w)
    print("A:\t", A)
    print("Omega:\t", Omega)
    print("P*A:\t", P*A)
    print("head_dir:", head_dir)
    print("l:\t", l)
    print("--------------------------------")
  end
end

if (sim_call_type==sim_childscriptcall_cleanup) then
  if not pluginNotFound then
    simExtRosInterface_shutdownPublisher(dvsPub)
    simExtRosInterface_shutdownPublisher(transformPub)
    simExtRosInterface_shutdownSubscriber(turnRadiusSub)
    simExtRosInterface_shutdownSubscriber(resetRobotSub)
  end

  if auxConsole then
    simAuxiliaryConsoleClose(auxConsole)
  end
end

if (sim_call_type==sim_childscriptcall_actuation) then
  step=step+1
  t=t+simGetSimulationTimeStep()

  -- Snake locomotion
  local theta = 0

  local head_dir = theta

  for i=2,N,1 do
    P = ((i-1)/N)*y + z

    phi = C + P*A*math.sin(Omega*(i-1) - w*t)

    simSetJointTargetPosition(joints_v[i], -phi*(1-math.exp(p*t)))

    phi = simGetJointPosition(joints_v[i])

    theta = theta + phi

    head_dir = head_dir + theta
  end

  head_dir = head_dir/(N+1)

  simSetJointTargetPosition(joints_v[1], -head_dir*(1-math.exp(p*t)))

  position_old = position
  position = simGetObjectPosition(robotHandle,-1)
  travelled_distance = calculate_travelled_distance(travelled_distance, position_old, position)

  quaternion=simGetObjectQuaternion(robotHandle,-1)
  simExtRosInterface_publish(transformPub, {translation={x=position[1],y=position[2],z=position[3]},rotation={x=quaternion[1],y=quaternion[2],z=quaternion[3],w=quaternion[4]}})

  -- Print parameters every mod steps
  if(comments==true and math.fmod(step,mod)==0) then
    print("--------Snake step: "..(step).."----------")
    print("radius:\t", radius)
    print("w:\t", w)
    print("distance:", travelled_distance)
    print("--------------------------------")
  end
end

if (sim_call_type==sim_childscriptcall_sensing) then
  -- Read and publish distances
  result,smallestDistance1=simHandleDistance(distanceHandle1)
  result,smallestDistance2=simHandleDistance(distanceHandle2)

  smallestDistances={smallestDistance1, smallestDistance2}

  simExtRosInterface_publish(distancePub,{data=smallestDistances})

  -- Read and formate DVS data at each simulation step
  if notFirstHere and not pluginNotFound then
    r,t0,t1=simReadVisionSensor(cameraHandle)

    if (t1) then
      ts=math.floor(simGetSimulationTime()*1000)
      newData={}
      for i=0,(#t1/3)-1,1 do
        newData[1+i*2]=math.floor(t1[3*i+2])
        newData[2+i*2]=math.floor(t1[3*i+3])

        if (showConsole) then
          if (t1[3*i+1]>0) then
            onOff=", on"
          else
            onOff=", off"
          end
          simAuxiliaryConsolePrint(auxConsole,"time="..ts.." ms, x="..math.floor(t1[3*i+2])..", y="..math.floor(t1[3*i+3])..onOff.."\n")
        end
      end
    end
    simExtRosInterface_publish(dvsPub,{data=newData})
  end
  notFirstHere=true
end
