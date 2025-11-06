"""
Default configuration settings for the RasPi Smart Car.

NOTE: GPIO pin numbers use BOARD numbering scheme.
"""


# === Motor GPIO Pins (BOARD) ===

FL: tuple[int, int] = (15, 16)  # Front-left motor pins
FR: tuple[int, int] = (11, 12)  # Front-right motor pins

BL: tuple[int, int] = (37, 38)  # Back-left motor pins
BR: tuple[int, int] = (35, 36)  # Back-right motor pins

MOTOR_PINS: list[tuple[int, int]] = [
                                     FL, FR,
                                     BL, BR
                                    ]
