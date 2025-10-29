"""
Classes for hardware components:
- Servos for Sensor Array
"""
from RPi import GPIO
GPIO.setmode(GPIO.BOARD)

from .servo import SensorArrayServos
