import Adafruit_PCA9685
import time

pwm = Adafruit_PCA9685.PCA9685(address=0x40)
pwm.set_pwm_freq(60)

print('Enter a value between 350 - 450:')

try:
    while True:
        user_input = int(input())
        if 350 <= user_input <= 450:
            pwm.set_pwm(3, 0, user_input)
        else:
            print("Input out of range (350 - 450)")

except KeyboardInterrupt:
    print("\nProgram terminated by user.")

finally:
    pwm.set_pwm(3, 0, 0)  # Set the servo back to the neutral position


