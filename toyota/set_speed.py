import senser
from define import ESC

def set_speed(speed):
	senser.pwm.set_pwm(ESC, 0, speed)