import Adafruit_PCA9685
import time
pwm = Adafruit_PCA9685.PCA9685(address=0x40)
pwm.set_pwm_freq(60)
pwm.set_pwm(3, 0, 350)
time.sleep(0.5)
pwm.set_pwm(3, 0, 450)