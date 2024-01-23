import RPi.GPIO as GPIO
import time
import sys
import Adafruit_PCA9685
import senser
import check_turn as check
import set_speed as speed
import servo_driver as servo
from define import STOP, SLOW, RUN, STRAIGHT, RIGHT, LEFT

print('press to start')
input()

speed.set_speed(RUN)
servo.adjust_servo_morter(STRAIGHT)

while True:
	try:
		front_distance = float('{:.1f}'.format(senser.front_get_distance()))
		print("front_Distance: " + str(front_distance) + "cm")
		right_distance = float('{:.1f}'.format(senser.right_get_distance()))
		print("right_Distance: " + str(right_distance) + "cm")
		left_distance = float('{:.1f}'.format(senser.left_get_distance()))
		print("left_Distance: " + str(left_distance) + "cm")
		if check.stop(front_distance) == True:
			speed.set_speed(STOP)
			servo.adjust_servo_morter(STRAIGHT)
			print('stop')
			break
		elif check.turn_right(front_distance, right_distance, left_distance) == True:
			speed.set_speed(RUN)
			servo.adjust_servo_morter(RIGHT)
			print('right')
		elif check.turn_left(front_distance, right_distance, left_distance) == True:
			speed.set_speed(RUN)
			servo.adjust_servo_morter(LEFT)
			print('left')
		else:
			speed.set_speed(RUN)
			servo.adjust_servo_morter(STRAIGHT)
			print('straight')
		time.sleep(0.3)
		

	except KeyboardInterrupt:
		senser.pwm.set_pwm(1, 0, 380)
		GPIO.cleanup()
		sys.exit()
	finally:
		senser.pwm.set_pwm(3, 0, 0)  # Set the servo back to the neutral position
