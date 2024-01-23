import RPi.GPIO as GPIO
import time
import sys
import Adafruit_PCA9685
from define import TURN, SHORT, DOWN

def stop(front, right, left):
	if front <= SHORT:
		return True
	elif right <= SHORT:
		return True
	elif left <= SHORT:
		return True
	return False

def down(front, right, left):
	if front <= DOWN:
		return True
	elif right <= DOWN:
		return True
	elif left <= DOWN:
		return True
	return False

def turn_right(front, right, left):
	if left <= TURN and TURN <= right:
		return True
	if left <= TURN and right <= TURN and 10 + left <= right:
		return True
	return False

def turn_left(front, right, left):
	if right <= TURN and TURN <= left:
		return True
	if left <= TURN and right <= TURN and 10 + right <= left:
		return True
	return False