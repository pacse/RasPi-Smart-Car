"""
Default configuration settings for the RasPi Smart Car server.
"""
import logging


class DEFAULT:
    HOST = "0.0.0.0" # TODO: set
    PORT = 5000      # TODO: set

    LOG_LEVEL = logging.INFO

    MOTOR_PINS = [
                  (11, 12),  # Front-left motor pins
                  (15, 16),  # Front-right motor pins
                  (35, 36),  # Back-left motor pins
                  (37, 38)   # Back-right motor pins
                 ]

    SERVO_PINS = [
                  32,  # TODO: set
                  33   # TODO: set
                 ]


# Configure basic logging
logging.basicConfig(level=DEFAULT.LOG_LEVEL,
                    format='[%(levelname)s | %(name)s]: %(message)s')
