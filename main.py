from Code.Server.motors import Motor, config
from Code.Server.motors.car import Car

car = Car(config.MOTOR_PINS)
car.set_motor_speeds(50, 50, 50, 50)


