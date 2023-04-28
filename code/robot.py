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
    ina = ina219.ina219()

    try:
        # Testing INA219
        print('Voltage:', ina.get_voltage())
        print('Current:', ina.get_current())
        print('Power:', ina.get_power())

        # Testing Servo
        #sv.test_routine()
        sv.move_to_angle(45)
        time.sleep(1)
        sv.move_to_angle(0)
        time.sleep(1)
        sv.move_to_angle(90)

        # Testing Motors
        motor_driver.change_both_duty_cycles(100)
        time.sleep(2)
        motor_driver.set_both_direction_clockwise(False)
        time.sleep(2)
        motor_driver.set_standby_both()
        motor_driver.set_left_direction_clockwise(True)
        motor_driver.change_both_duty_cycles(100)
        time.sleep(2)
        motor_driver.set_right_direction_clockwise(True)
        motor_driver.change_both_duty_cycles(0)
        for i in range(0,100,5):
            motor_driver.change_both_duty_cycles(i)
            time.sleep(0.3)
        motor_driver.set_standby_both()


        # Cleaning up in the end
        GPIO.cleanup()

    except KeyboardInterrupt:
        motor_driver.stop_both()
        GPIO.cleanup()
        print('Stopped!')