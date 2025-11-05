"""
Package for RasPi Smart Car project.
"""

from RPi import GPIO # type: ignore (not coding on Raspberry Pi)
GPIO.setmode(GPIO.BOARD)

from .motors import Motor, Car, Controller
