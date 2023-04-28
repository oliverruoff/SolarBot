import RPi.GPIO as GPIO

class servo:

    def __init__(self, pin, gpio_mode=GPIO.BCM):
        self.pin = pin

        # initializing pins
        GPIO.setmode(gpio_mode)
        GPIO.setup(pin, GPIO.OUT)

        self.p = GPIO.PWM(pin, 50)
        self.p.start(0)

    def move_to_angle(self, degree):
        self.p.ChangeDutyCycle(2+(degree/18))