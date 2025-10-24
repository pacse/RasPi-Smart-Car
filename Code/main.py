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

car = Car(motor_pins)

car.set_motor_speeds(FL=50, FR=50, BL=50, BR=50)

sleep(2)

car.stop_all_motors()
car.cleanup()
