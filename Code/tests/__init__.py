"""
Test suite for motor control
"""
# === Logging ===

import logging

LOG_LEVEL = logging.INFO

logging.basicConfig(level=LOG_LEVEL,
                    format='[%(levelname)s | %(name)s]: %(message)s')

from .motors import test_Controller, test_Motor, test_Car, test_Controller
