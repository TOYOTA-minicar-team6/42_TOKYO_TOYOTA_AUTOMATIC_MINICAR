def adjust_servo_morter(pwm, servo, direction):
    pwm.set_pwm(servo, 0, direction)