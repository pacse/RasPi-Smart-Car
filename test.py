"""
Run tests from test suite
"""

#from Code.tests.motors import test_Controller, test_Motor, test_Car
from Code.config import MOTOR_PINS
from time import sleep

def run_all_tests():
    """
    Run all tests.
    """
    #test_Motor()
    #test_Car()
    #test_Controller()
    #print("All tests pass?")

from Code.motors import Car

car = Car(MOTOR_PINS)

car.forward(50)
sleep(10)
car.stop_all_motors()
car.cleanup()
