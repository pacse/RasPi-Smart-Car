from Server.components import Buzzer, Infrared, Photoresistor, Servo
from time import sleep

import smbus
print('Imported smbus')

print('Buzzer init . . .')
buzzer = Buzzer()

buzzer.on()
sleep(2)
buzzer.off()
sleep(2)

print('Servo init . . .')
pwm_servo = Servo()

pwm_servo.set_servo_pwm(0,90)
pwm_servo.set_servo_pwm(1,90)

pwm_servo.cleanup()
buzzer.cleanup()
