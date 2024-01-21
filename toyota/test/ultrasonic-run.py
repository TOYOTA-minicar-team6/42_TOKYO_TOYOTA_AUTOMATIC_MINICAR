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

def set_motor_speed(distance):
    if distance < 10:
        pwm.set_pwm(1, 0, 0)  # モーター停止
    else:
        speed = 350 + (400 - 350) * (10 - distance) / 10
        speed = max(350, min(speed, 400))
        pwm.set_pwm(1, 0, int(speed))

while True:
    try:
        distance = get_distance()
        set_motor_speed(distance)
        print("Distance: {:.1f} cm, Speed: {}".format(distance, int(speed)))
        time.sleep(1)

    except KeyboardInterrupt:
        GPIO.cleanup()
        pwm.set_pwm(1, 0, 0)
        sys.exit()

