"""epuck_go_forward controller."""

# You may need to import some classes of the controller module. Ex:
#  from controller import Robot, Motor, DistanceSensor
#from controller import Robot
from controller import Supervisor
from controller import Robot
import cv2
import numpy as np

# create the Robot instance.

#print("hello")
# 1. Initialize Supervisor
sp = Supervisor()
#timestep = int(robot.getBasicTimeStep())

# 2. Get the root 'children' field where objects are added
root_node = sp.getRoot()
children_field = root_node.getField('children')

# 3. Spawn multiple objects in a loop
scale = 20
for i in range(60):
    # Define object as a VRML string (e.g., a simple Box or a PROTO)
    # Use 'DEF' to give each object a unique name for later reference
    d = scale*np.random.rand(2)-scale/2
    obj_string = f'DEF WB_{i} WaterBottle {{ translation {d[0]} {d[1]} 0.0 }}'
    # Import the node into the scene
    children_field.importMFNodeFromString(-1, obj_string)
    d = scale*np.random.rand(2)-scale/2
    obj_string = f'DEF KN_{i} Knife {{ translation {d[0]} {d[1]} 0.0 }}'
    # Import the node into the scene
    children_field.importMFNodeFromString(-1, obj_string)
    d = scale*np.random.rand(2)-scale/2
    obj_string = f'DEF SP_{i} Spoon {{ translation {d[0]} {d[1]} 0.0 }}'
    # Import the node into the scene
    children_field.importMFNodeFromString(-1, obj_string)



#robot = Robot()

light_def = sp.getFromDef("light")
lum_field = light_def.getField('luminosity')
lum_field.setSFFloat(0.1)

fog_def = sp.getFromDef("fog")
vis_fog = fog_def.getField('visibilityRange')
vis_fog.setSFFloat(100.0)

#n = robot.getNumberOfDevices()
#for i in range(n):
#    device = robot.getDeviceByIndex(i)
#    print(device.getName())
# get the time step of the current world.
timestep = int(sp.getBasicTimeStep())
print(timestep)
# You should insert a getDevice-like function in order to get the
# instance of a device of the robot. Something like:
#  motor = robot.getDevice('motorname')
#  ds = robot.getDevice('dsname')
#  ds.enable(timestep)
# get the motor devices
#TIME_STEP = 64

MAX_SPEED = 6.28


# get a handler to the motors and set target position to infinity (speed control)
#leftMotor = robot.getDeviceByIndex(0)
#rightMotor = robot.getDeviceByIndex(2)
#leftMotor.setPosition(float('inf'))
#rightMotor.setPosition(float('inf'))

w1 = sp.getDevice('wheel1')
w2 = sp.getDevice('wheel2')
w3 = sp.getDevice('wheel3')
w4 = sp.getDevice('wheel4')
w1.setPosition(float('inf'))
w2.setPosition(float('inf'))
w3.setPosition(float('inf'))
w4.setPosition(float('inf'))

# set up the motor speeds at 10% of the MAX_SPEED.
w1.setVelocity(0.4 * MAX_SPEED) # RF
w2.setVelocity(-0.4 * MAX_SPEED) # LF
w3.setVelocity( 0.4 * MAX_SPEED) # RR
w4.setVelocity(-0.4 * MAX_SPEED) # LR

camera = sp.getDevice('camera')
camera.enable(timestep)
# Main loop:
# - perform simulation steps until Webots is stopping the controller
data_folder = "/home/ml/project/webots/datasets/run1/"
cnt = 0
while sp.step(timestep) != -1:
    raw_image=camera.getImage()
    image = np.frombuffer(raw_image,np.uint8).reshape((camera.getHeight(),camera.getWidth(),4))
    frame = cv2.cvtColor(image,cv2.COLOR_BGRA2BGR)
    cv2.imshow("disp",frame)
    if cnt%10 == 0:
        cv2.imwrite(f"{data_folder}{cnt}.jpg",frame)
    cv2.waitKey(1)
    if cnt%500==0:
        lmval = np.random.rand(1)
        lum_field.setSFFloat(float(lmval))
        lmval_fog = np.random.rand(1)*10+1
        vis_fog.setSFFloat(float(lmval_fog))
    # Read the sensors:
    # Enter here functions to read sensor data, like:
    #  val = ds.getValue()
    #
    # Process sensor data here.
    #
    # Enter here functions to send actuator commands, like:
    #  motor.setPosition(10.0)
    cnt = cnt + 1
    pass

# Enter here exit cleanup code.
