from Server.motors import Car
from Server.motors.config import MOTOR_PINS
from time import sleep

car = Car(MOTOR_PINS)
car.set_motor_speeds(50, 50, 50, 50)
sleep(2)
car.stop_all_motors()

for motor in car.motors:
    motor.set_speed(50)
    sleep(5)
    motor.stop()

car.cleanup()
