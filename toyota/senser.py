import RPi.GPIO as GPIO
import time
import sys
import Adafruit_PCA9685

front_trig_pin = 15
front_echo_pin = 14
right_trig_pin = 23
right_echo_pin = 24
left_trig_pin = 27
left_echo_pin = 17
speed_of_sound = 34370

GPIO.setmode(GPIO.BCM)
GPIO.setwarnings(False)
GPIO.setup(front_trig_pin, GPIO.OUT)
GPIO.setup(front_echo_pin, GPIO.IN)
GPIO.setup(right_trig_pin, GPIO.OUT)
GPIO.setup(right_echo_pin, GPIO.IN)
GPIO.setup(left_trig_pin, GPIO.OUT)
GPIO.setup(left_echo_pin, GPIO.IN)
pwm = Adafruit_PCA9685.PCA9685(address=0x40)
pwm.set_pwm_freq(60)

def front_get_distance(): 
	GPIO.output(front_trig_pin, GPIO.HIGH)
	time.sleep(0.000010)
	GPIO.output(front_trig_pin, GPIO.LOW)

	while not GPIO.input(front_echo_pin):
	 	pass
	t1 = time.time()

	while GPIO.input(front_echo_pin):
		pass
	t2 = time.time()

	return (t2 - t1) * speed_of_sound / 2

def right_get_distance(): 
	GPIO.output(right_trig_pin, GPIO.HIGH)
	time.sleep(0.000010)
	GPIO.output(right_trig_pin, GPIO.LOW)

	while not GPIO.input(right_echo_pin):
		pass

	t1 = time.time()

	while GPIO.input(right_echo_pin):
		pass
	t2 = time.time()

	return (t2 - t1) * speed_of_sound / 2

def left_get_distance(): 
	GPIO.output(left_trig_pin, GPIO.HIGH)
	time.sleep(0.000010)
	GPIO.output(left_trig_pin, GPIO.LOW)

	while not GPIO.input(left_echo_pin):
		pass

	t1 = time.time()

	while GPIO.input(left_echo_pin):
		pass
	t2 = time.time()

	return (t2 - t1) * speed_of_sound / 2
