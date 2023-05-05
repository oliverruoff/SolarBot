import RPi.GPIO as GPIO
import time

class servo:

    def __init__(self, pin, gpio_mode=GPIO.BCM):
        self.pin = pin

        # initializing pins
        GPIO.setmode(gpio_mode)
        GPIO.setup(pin, GPIO.OUT)
        self.p = GPIO.PWM(pin, 50)

    def move_to_angle(self, degree):
        self.p.start(0)
        self.p.ChangeDutyCycle(int(2+(degree/18)))

    def stop_pwm(self):
        self.p.stop()

    def test_routine(self):
        import time
        for dc in range(12):
            print('Changing servo dutycycle to:', dc)
            self.p.ChangeDutyCycle(dc)
            time.sleep(1)