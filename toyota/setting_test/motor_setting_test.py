import Adafruit_PCA9685
import time
pwm = Adafruit_PCA9685.PCA9685(address=0x40)
pwm.set_pwm_freq(60)
#急加速急停止
pwm.set_pwm(1, 0, 375)
time.sleep(0.2)
pwm.set_pwm(1, 0, 380)
