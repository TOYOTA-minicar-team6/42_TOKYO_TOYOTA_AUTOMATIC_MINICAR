import RPi.GPIO as GPIO
import time
import sys
import Adafruit_PCA9685

def stop(front):
	if front <= 50.0:
		return True
	return False

def turn_right(front, right, left):
	if left <= 50.0:
		return True
	return False

def turn_left(front, right, left):
	if right <= 50.0:
		return True
	return False