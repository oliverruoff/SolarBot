# Motor driver control for driver l298n
# author: Oliver Ruoff


import RPi.GPIO as GPIO


class l298n:

    def __init__(
        self,
        in1_pin,
        in2_pin,
        in3_pin,
        in4_pin,
        gpio_mode=GPIO.BCM
    ):

        self.in1_pin = in1_pin
        self.in2_pin = in2_pin
        self.in3_pin = in3_pin
        self.in4_pin = in4_pin
        self.left_duty_cycle = 0
        self.right_duty_cycle = 0
        self.left_direction_clockwise = True
        self.right_direction_clockwise = True

        # initializing pins
        GPIO.setmode(gpio_mode)
        GPIO.setup(in1_pin, GPIO.OUT)
        GPIO.setup(in2_pin, GPIO.OUT)
        GPIO.setup(in3_pin, GPIO.OUT)
        GPIO.setup(in4_pin, GPIO.OUT)

        # right motor
        self.p_a = GPIO.PWM(in1_pin, 1000)  # setting pin1 to pwm
        GPIO.output(self.in2_pin, GPIO.LOW) # and pin2 to 0 -> forward
        self.p_a.start(0)

        # left motor
        self.p_b = GPIO.PWM(in3_pin, 1000)  # setting pin3 to pwm
        GPIO.output(self.in4_pin, GPIO.LOW) # and pin4 to 0 -> forward
        self.p_b.start(0)

        self.p_a.ChangeDutyCycle(self.right_duty_cycle)
        self.p_b.ChangeDutyCycle(self.left_duty_cycle)

    def change_right_duty_cycle(self, duty_cycle):
        if duty_cycle > 100:
            duty_cycle = 100
        elif duty_cycle < 0:
            duty_cycle = 0
        self.right_duty_cycle = duty_cycle
        self.p_a.ChangeDutyCycle(duty_cycle)

    def change_left_duty_cycle(self, duty_cycle):
        if duty_cycle > 100:
            duty_cycle = 100
        elif duty_cycle < 0:
            duty_cycle = 0
        self.left_duty_cycle = duty_cycle
        self.p_b.ChangeDutyCycle(duty_cycle)

    def set_right_direction_clockwise(self, clockwise):
        if clockwise:
            self.p_a = GPIO.PWM(self.in1_pin, 1000)  # setting pin1 to pwm
            GPIO.output(self.in2_pin, GPIO.LOW) # and pin2 to 0 -> forward
        else:
            self.p_a = GPIO.PWM(self.in2_pin, 1000)  # setting pin2 to pwm
            GPIO.output(self.in1_pin, GPIO.LOW) # and pin1 to 0 -> backward

    def set_left_direction_clockwise(self, clockwise):
        if clockwise:
            self.p_b = GPIO.PWM(self.in3_pin, 1000)  # setting pin1 to pwm
            GPIO.output(self.in4_pin, GPIO.LOW) # and pin2 to 0 -> forward
        else:
            self.p_b = GPIO.PWM(self.in4_pin, 1000)  # setting pin1 to pwm
            GPIO.output(self.in3_pin, GPIO.LOW) # and pin2 to 0 -> forward

    def set_standby_right(self):
        GPIO.output(self.in1_pin, GPIO.LOW)
        GPIO.output(self.in2_pin, GPIO.LOW)

    def set_standby_left(self):
        GPIO.output(self.in3_pin, GPIO.LOW)
        GPIO.output(self.in4_pin, GPIO.LOW)

    def set_standby_both(self):
        self.set_standby_both()
        self.set_standby_both()

    def break_right(self):
        GPIO.output(self.in1_pin, GPIO.HIGH)
        GPIO.output(self.in2_pin, GPIO.HIGH)

    def break_left(self):
        GPIO.output(self.in3_pin, GPIO.HIGH)
        GPIO.output(self.in4_pin, GPIO.HIGH)

    def break_both(self):
        self.break_left()
        self.break_right()