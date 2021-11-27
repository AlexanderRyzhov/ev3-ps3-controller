from math import pi

class Tank():

    def __init__(self, left_motor, right_motor, wheel_diameter, axle_track):
        self.left_motor = left_motor
        self.right_motor = right_motor
        self.wheel_diameter = wheel_diameter
        self.axle_track = axle_track
        self.self_controlled = False

    def run_straight(self, distance):
        speed = 250
        rotation_angle = distance * 360 // (self.wheel_diameter * pi)
        self.left_motor.run_angle(speed, rotation_angle, wait = False)
        self.right_motor.run_angle(speed, rotation_angle, wait = False)
        while (not (self.left_motor.control.done() and self.right_motor.control.done())):
            yield self.self_controlled 
        #yield True

    def run_turn(self, angel):
        speed = 250
        rotation_angle = angel * self.axle_track // self.wheel_diameter 
        self.left_motor.run_angle(speed, rotation_angle, wait = False)
        self.right_motor.run_angle(speed, -rotation_angle, wait = False)
        while (not (self.left_motor.control.done() and self.right_motor.control.done())):
            yield self.self_controlled 
        #yield True

    def run_square(self):        
        def async_movement():
            print("#1")
            yield from self.run_straight(300)
            yield from self.run_turn(90)
            print("#2")
            yield from self.run_straight(300)
            yield from self.run_turn(90)
            print("#3")
            yield from self.run_straight(300)
            yield from self.run_turn(90)
            print("#4")
            yield from self.run_straight(300)
            yield from self.run_turn(90)
            self.self_controlled = False
            yield

        self.self_controlled = True        
        result = async_movement()
        return result
    
    def tank_move(self, speed, turn):
        self.left_motor.dc(speed - turn)
        self.right_motor.dc(speed + turn)

    def stop_self_controll(self):
        self.left_motor.stop()
        self.right_motor.stop()
        self.self_controlled = False