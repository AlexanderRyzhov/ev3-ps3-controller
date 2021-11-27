import struct

def ps3_controller():

    # Initialize variables. 
    # Assuming sticks are in the middle when starting.
    right_stick_x = 124
    right_stick_y = 124

    right_stick_zeroes = True
    right_stick_zeroes_sent = False

    # A helper function for converting stick values (0 - 255)
    # to more usable numbers (-100 - 100)
    def scale(val, src, dst):
        """
        Scale the given value from the scale of src to the scale of dst.
    
        val: float or int
        src: tuple
        dst: tuple
    
        example: print(scale(99, (0.0, 99.0), (-1.0, +1.0)))
        """
        return (float(val - src[0]) / (src[1] - src[0])) * (dst[1] - dst[0]) + dst[0]

    def deadzones(x, y):        
        
        if abs(x)<10:
            x = 0
        if abs(y)<10:
            y = 0

        if x==0 and y == 0:
            zeroes = True            
        else:
            zeroes = False
        return (x,y, zeroes)


    # Find the PS3 Gamepad:
    # /dev/input/event3 is the usual file handler for the gamepad.
    # look at contents of /proc/bus/input/devices if it doesn't work.
    infile_path = "/dev/input/event3"

    # open file in binary mode
    in_file = open(infile_path, "rb")

    # Read from the file
    # long int, long int, unsigned short, unsigned short, unsigned int
    FORMAT = 'llHHI'    
    EVENT_SIZE = struct.calcsize(FORMAT)
    event = in_file.read(EVENT_SIZE)
    counter = 0

    while event:        
        button = None
        (tv_sec, tv_usec, ev_type, code, value) = struct.unpack(FORMAT, event)

        if ev_type == 3 and code == 3:
            button = "right_stick"  
            right_stick_x = value
        if ev_type == 3 and code == 4:
            button = "right_stick"  
            right_stick_y = value

        if (ev_type == 1 and code == 308 and value == 1):
            button = "square"        
        if (ev_type == 1 and code == 304 and value == 1):
            button = "cross"

        # Scale stick positions to -100,100

        forward = scale(right_stick_y, (0,255), (100,-100))        
        left = scale(right_stick_x, (0,255), (100,-100))

        # calc deadzones and zero-zero position flags        
        forward, left, right_stick_zeroes = deadzones(forward, left)
        
        if not right_stick_zeroes:
            right_stick_zeroes_sent = False

        if (button == "right_stick" and not (right_stick_zeroes and right_stick_zeroes_sent)):                
            out = ("manual", (forward, left))
            if right_stick_zeroes:
                right_stick_zeroes_sent = True
            yield out
        elif (not button is None):
            out = ("auto", button)
            yield out
        else:
            yield

        #left_motor.dc(forward - left)
        #right_motor.dc(forward + left)

        # Finally, read another event

        event = in_file.read(EVENT_SIZE)
        counter += 1
        
    in_file.close()