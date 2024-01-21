import RPi.GPIO as GPIO
import time
import sys
import Adafruit_PCA9685

trig_pin = 15
echo_pin = 14
speed_of_sound = 34370

GPIO.setmode(GPIO.BCM)
GPIO.setwarnings(False)
GPIO.setup(trig_pin, GPIO.OUT)
GPIO.setup(echo_pin, GPIO.IN)
pwm = Adafruit_PCA9685.PCA9685(address=0x40)
pwm.set_pwm_freq(60)

def get_distance(): 
	GPIO.output(trig_pin, GPIO.HIGH)
	time.sleep(0.000010)
	GPIO.output(trig_pin, GPIO.LOW)

	while not GPIO.input(echo_pin):
		pass
	t1 = time.time()

	while GPIO.input(echo_pin):
		pass
	t2 = time.time()

	return (t2 - t1) * speed_of_sound / 2

print('press to start')
input()

pwm.set_pwm(1, 0, 378)
pwm.set_pwm(3, 0, 0)

while True:
	try:
		distance = float('{:.1f}'.format(get_distance()))
		print("Distance: " + str(distance) + "cm")
		if distance <= 150.0:
			pwm.set_pwm(1, 0, 380)
			break
		time.sleep(1)
		

	except KeyboardInterrupt:
		pwm.set_pwm(1, 0, 380)
		GPIO.cleanup()
		sys.exit()
	# finally:
	# 	pwm.set_pwm(1, 0, 0)  # Set the servo back to the neutral position


