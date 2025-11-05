"""
Run tests from test suite
"""

from Code.tests import test_Controller, test_Motor, test_Car

def run_all_tests():
    """
    Run all tests.
    """
    test_Motor()
    test_Car()
    test_Controller()
    print("All tests pass?")
