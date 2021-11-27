#!/usr/bin/env pybricks-micropython
from pybricks.hubs import EV3Brick
from pybricks.ev3devices import (Motor, TouchSensor, ColorSensor,
                                 InfraredSensor, UltrasonicSensor, GyroSensor)
from pybricks.parameters import Port, Stop, Direction, Button, Color
from pybricks.tools import wait, StopWatch, DataLog
from pybricks.robotics import DriveBase
from pybricks.media.ev3dev import SoundFile, ImageFile

from tank import Tank
from ps3 import ps3_controller


# This program requires LEGO EV3 MicroPython v2.0 or higher.
# Click "Open user guide" on the EV3 extension tab for more information.


# Create your objects here.
ev3 = EV3Brick()

def init_robot():

    left_motor = Motor(Port.A, Direction.COUNTERCLOCKWISE)
    right_motor = Motor(Port.D, Direction.COUNTERCLOCKWISE)
    WHEEL_DIAMETER = 43
    AXLE_TRACK = 130
    #robot = DriveBase(left_motor, right_motor, WHEEL_DIAMETER, AXLE_TRACK) 
    robot = Tank(left_motor, right_motor, WHEEL_DIAMETER, AXLE_TRACK)
    return robot
    
# Write your program here.
ev3.speaker.beep()

robot = init_robot()
controller = ps3_controller()

while True:

    # controller input processing    
    action = None
    mode, params = next(controller) or (None, None)
    
    if mode == "manual":        
        action = "manual"
        forward, left = params
        print("MANUAL: forward =", forward, ", left =", left)
    elif mode == "auto":
        action = params

    # robot movements processing
    if robot.self_controlled:
        next(movement)
        if action == "cross":
            print('cross was pressed, stop moving...')
            robot.stop_self_controll()
        if action == "manual":
            print('go to manual mode, stop self_controlled moving...')
            robot.stop_self_controll()
            robot.tank_move(forward, left)
    else:
        if action == "square":
            print('square was pressed, start moving...')
            movement = robot.run_square()
        if action == "manual":
            robot.tank_move(forward, left)
        