"""
Test motor module
"""
from ..Server.motors import Car, Motor, Controller
from .. import logging, DEFAULT
from time import sleep

DURATION = 1     # how long to run motors
RAMP_DELAY = 0.1 # delay between speed changes during ramp test

logger = logging.getLogger(__name__)


# === Helpers ===
def motor_action(motor: Motor, action_name: str, action_func, *args) -> None:
    """
    Helper to take motor actions.

    :param motor: Motor instance.
    :param action_name: Name of the action.
    :param action_func: Function to call.
    :param args: Arguments for the function.
    """

    logger.info(f'{action_name}: {", ".join(map(str, args))}% | {DURATION}s . . .')
    action_func(*args)
    sleep(DURATION)
    motor.stop()

def car_action(car: Car, action_name: str, action_func, *args) -> None:
    """
    Helper to take car actions.

    :param car: Car instance.
    :param action_name: Name of the action.
    :param action_func: Function to call.
    :param args: Arguments for the function.
    """

    logger.info(f'{action_name}: {", ".join(map(str, args))}% | {DURATION}s . . .')
    action_func(*args)
    sleep(DURATION)
    car.stop_all_motors()

def controller_action(
                      controller: Controller,
                      action_name: str,
                      duration: float,
                      action_func, *args
                     ) -> None:
    """
    Helper to take controller actions.

    :param controller: Controller instance.
    :param action_name: Name of the action.
    :param action_func: Function to call.
    :param args: Arguments for the function.
    """
    duration = duration or DURATION

    logger.info(f'{action_name}: {", ".join(map(str, args))} | {duration}s . . .')
    action_func(*args)
    sleep(duration)


# === Tests ===
def test_Motor():
    """
    Test Motor class
    """
    logger.info('Testing Motor class . . .')


    logger.debug('Creating Motor instance . . .')
    motor = Motor(DEFAULT.MOTOR_PINS[0])


    motor_action(motor, 'forward', motor.forward, 50)
    motor_action(motor, 'backward', motor.backward, 75)


    logger.info('Ramping: -100% to 100% . . .')

    for speed in range(-100, 101):
        motor.set_speed(speed)
        sleep(RAMP_DELAY)

    motor.stop()


    logger.info('Invalid speed inputs . . .')

    for speed in [110, -300, 'A', None]:
        try:
            motor.set_speed(speed)
            logger.error(f'Exception not raised for speed={speed!r}')

        except (ValueError, TypeError) as e:
            logger.info(f'Caught expected exception with speed {speed!r}: {e}')


    logger.info('Motor class tests completed.')
    motor.cleanup()


def test_Car():
    """
    Test Car class
    """
    logger.info('Testing Car class . . .')

    logger.debug('Creating Car instance . . .')
    car = Car(DEFAULT.MOTOR_PINS)


    car_action(car, 'set_all_speeds', car.set_all_speeds, 60)

    car_action(car, 'set_motor_speeds', car.set_motor_speeds, 50, 60, -70, -80)

    car_action(car, 'forward', car.forward, 70)
    car_action(car, 'backward', car.backward, 50)

    car_action(car, 'turn_left', car.turn_left, 60)
    car_action(car, 'turn_right', car.turn_right, 60)

    car_action(car, 'pivot_left', car.pivot_left, 80)
    car_action(car, 'pivot_right', car.pivot_right, 80)

    logger.info('Ramping all: -100% to 100% . . .')
    for speed in range(-100, 101):
        car.set_all_speeds(speed)
        sleep(RAMP_DELAY)

    car.stop_all_motors()

    logger.info('Invalid speed inputs . . .')
    for speeds in [
        (120, 0, 0, 0),
        (0, -150, 0, 0),
        (0, 0, 'A', 0),
        (0, 0, 0, None),
        (50, 60)  # too few speeds
    ]:
        try:
            car.set_motor_speeds(*speeds)
            logger.error(f'Exception not raised for speeds={speeds!r}')

        except (ValueError, TypeError, RuntimeError) as e:
            logger.info(f'Caught expected exception with speeds {speeds!r}: {e}')

    logger.info('Car class tests completed.')
    car.cleanup()


def test_Controller():
    """
    Test Controller class
    """
    logger.info('Testing Controller class . . .')

    logger.debug('Creating Car Instance . . .')
    car = Car(DEFAULT.MOTOR_PINS)

    logger.debug('Creating Controller instance . . .')
    controller = Controller(car)


    logger.info('Simulating controller inputs . . .')

    inputs = [
        (1, 0),        # forward
        (-1, 0),       # backward
        (0, 1),        # turn right
        (0, -1),       # turn left
        (0.5, 0.5),    # forward-right
        (0.5, -0.5),   # forward-left
        (-0.5, 0.5),   # backward-right
        (-0.5, -0.5),  # backward-left
        (0, 0)         # stop
    ]

    for y_axis, x_axis in inputs:
        controller_action(controller,
                          'from_joystick', RAMP_DELAY,
                          controller.from_joystick,
                          y_axis, x_axis
                         )

    car.stop_all_motors()


    controller_action(controller,
                      'strafe_left', DURATION,
                      controller.strafe_left, 70
                    )
    car.stop_all_motors()

    controller_action(controller,
                      'strafe_left', DURATION,
                      controller.strafe_left, 70
                    )
    car.stop_all_motors()

    logger.info('Controller class tests completed.')
    controller.cleanup()
    car.cleanup()


if __name__ == '__main__':
    test_Motor()
    test_Car()
    test_Controller()
    print('\nAll tests pass?')
