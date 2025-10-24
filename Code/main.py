"""
Test script for movement
"""

from Server.components.motors import Car, Motor
from time import sleep

motor_pins = [
              (11, 12),  # Front-left motor pins
              (15, 16),  # Front-right motor pins
              (35, 36),  # Back-left motor pins
              (37, 38)   # Back-right motor pins
             ]

FL = Motor(motor_pins[0])
FR = Motor(motor_pins[1])
BL = Motor(motor_pins[2])
BR = Motor(motor_pins[3])

FL.set_speed(50)
FR.set_speed(50)
BL.set_speed(50)
BR.set_speed(50)

sleep(2)

FL.cleanup()
FR.cleanup()
BL.cleanup()
BR.cleanup()
