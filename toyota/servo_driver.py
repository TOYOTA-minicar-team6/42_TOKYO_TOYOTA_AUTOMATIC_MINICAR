import senser
from define import SERVO

def adjust_servo_morter(direction):
    senser.pwm.set_pwm(SERVO, 0, direction)