import time

import RPi.GPIO as GPIO
from actuators import l298n_mini


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

    try:
        motor_driver.change_right_duty_cycle(100)
        time.sleep(2)
        motor_driver.set_right_direction_clockwise(False)
        time.sleep(2)
        motor_driver.set_standby_right()

    except KeyboardInterrupt:
        motor_driver.stop_both()
        GPIO.cleanup()
        print('Stopped!')