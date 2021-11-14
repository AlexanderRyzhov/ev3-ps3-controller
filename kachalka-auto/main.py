#!/usr/bin/env pybricks-micropython

from pybricks import ev3brick as brick
from pybricks.hubs import EV3Brick
from pybricks.ev3devices import (Motor, TouchSensor, ColorSensor,
                                 InfraredSensor, UltrasonicSensor, GyroSensor)
from pybricks.parameters import (Port, Stop, Direction, Button, Color,
                                 SoundFile, ImageFile, Align)
from pybricks.tools import print, wait, StopWatch, DataLog
from pybricks.robotics import DriveBase

import struct

# Declare motors 
left_motor = Motor(Port.A)
right_motor = Motor(Port.B)

gyro_sensor = GyroSensor(Port.S1)

# Initialize the EV3 brick.
ev3 = EV3Brick()

data = DataLog('time', 'speed', 'delta_speed_average', 'delta_speed_prev')

watch = StopWatch()

speed_prev = None
delta_speed = []
delta_speed_prev = None

while True:
    speed = gyro_sensor.speed()
    if speed_prev:
        ds = speed - speed_prev
        delta_speed.append(ds)

        if len(delta_speed)>15:
            delta_speed.pop(0)

        delta_speed_average = sum(delta_speed)/len(delta_speed) 

        if delta_speed_prev:
            if (delta_speed_prev > 0) and (delta_speed_average <= 0):
                left_motor.track_target(-90)
                right_motor.track_target(-90) 
            if (delta_speed_prev < 0) and (delta_speed_average >= 0):
                left_motor.track_target(90)
                right_motor.track_target(90) 

            # logging
            time = watch.time()
            data.log(time, speed, delta_speed_average, delta_speed_prev)

        delta_speed_prev = delta_speed_average

    speed_prev = speed