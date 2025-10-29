from ..Server.servo import SensorArrayServos
import time

def test_Servo():
    """
    Test SensorArrayServos class:
    Rotate servos to 90 degrees.
    """

    print('Rotating both servos 90 degrees...')

    servos = SensorArrayServos()

    try:
        s = time.time()

        while time.time() - s != 10:
            servos.set_angle(0, 90)
            servos.set_angle(1, 90)
            time.sleep(0.05)

        servos.set_angle(0, 0)
        servos.set_angle(1, 0)

    except KeyboardInterrupt:
        servos.cleanup()
        print('\nEnd of program.')
