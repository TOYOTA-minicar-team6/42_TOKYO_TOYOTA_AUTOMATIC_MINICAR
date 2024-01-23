def set_speed(pwm, esc, speed):
	pwm.set_pwm(esc, 0, speed)