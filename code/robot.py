import time

import RPi.GPIO as GPIO
from actuators import l298n_mini, servo
from sensors import ina219


# IMPORTANT VARIABLES TO CONFIGURE -------------------

GPIO_MODE = GPIO.BCM
GPIO.setmode(GPIO_MODE)


if __name__ == '__main__':

    motor_driver = l298n_mini.l298n(
        in1_pin=26,
        in2_pin=19,
        in3_pin=13,
        in4_pin=6,
        gpio_mode=GPIO_MODE)
    
    sv = servo.servo(23)

    try:
        #motor_driver.change_both_duty_cycles(100)
        #time.sleep(2)
        #motor_driver.set_both_direction_clockwise(False)
        #motor_driver.set_both_direction_clockwise(False)
        #time.sleep(2)
        #motor_driver.set_standby_both()

        ina219.read()

        sv.move_to_angle(0)
        time.sleep(2)
        sv.move_to_angle(45)
        time.sleep(2)
        sv.move_to_angle(90)
        time.sleep(2)
        sv.move_to_angle(0)

        # Cleaning up in the end
        GPIO.cleanup()

    except KeyboardInterrupt:
        motor_driver.stop_both()
        GPIO.cleanup()
        print('Stopped!')