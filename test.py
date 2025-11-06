"""
Run tests from test suite
"""

#from Code.tests import test_Controller, test_Motor, test_Car

def run_all_tests():
    """
    Run all tests.
    """
    #test_Motor()
    #test_Car()
    #test_Controller()
    #print("All tests pass?")

from Code.motors import Motor

L = Motor((15, 16), 10)
R = Motor((11, 12))

L.set_speed(100)
R.set_speed(100)
import time
time.sleep(5)
L.set_speed(0)
R.set_speed(0)
L.cleanup()
R.cleanup()
