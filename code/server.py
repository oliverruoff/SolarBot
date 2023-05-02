from flask import Flask, request, Response, render_template
import time
import os

import cv2
import RPi.GPIO as GPIO

from actuators import l298n_mini

dir_path = os.path.dirname(os.path.realpath(__file__))
html_template_dir = os.path.join(dir_path, 'remote', 'python server')

app = Flask(__name__, template_folder=html_template_dir)
vc = cv2.VideoCapture(0)

dir_path = os.path.dirname(os.path.realpath(__file__))
tmp_img_path = os.path.join(
    dir_path, 'remote', 'python server', 'tmp_photo', 'tmp_img.jpg')

@app.route("/forward_curve_left")
def forward_curve_left():
    motorspeed = int(request.args.get('motorspeed', default=100))
    motor_driver.set_left_direction_clockwise(True)
    motor_driver.set_right_direction_clockwise(True)
    motor_driver.change_right_duty_cycle(motorspeed)
    second_motor_speed = motorspeed - 40 if motorspeed > 40 else 0
    motor_driver.change_left_duty_cycle(second_motor_speed)
    return "Done"

@app.route("/forward_curve_right")
def forward_curve_right():
    motorspeed = int(request.args.get('motorspeed', default=100))
    motor_driver.set_left_direction_clockwise(True)
    motor_driver.set_right_direction_clockwise(True)
    motor_driver.change_left_duty_cycle(motorspeed)
    second_motor_speed = motorspeed - 40 if motorspeed > 40 else 0
    motor_driver.change_right_duty_cycle(second_motor_speed)
    return "Done"

@app.route("/turn_left")
def turn_left():
    motorspeed = int(request.args.get('motorspeed', default=100))
    motor_driver.set_left_direction_clockwise(False)
    motor_driver.set_right_direction_clockwise(True)
    motor_driver.change_both_duty_cycles(motorspeed)
    return "Done"

@app.route("/turn_right")
def turn_right():
    motorspeed = int(request.args.get('motorspeed', default=100))
    motor_driver.set_left_direction_clockwise(True)
    motor_driver.set_right_direction_clockwise(False)
    motor_driver.change_both_duty_cycles(motorspeed)
    return "Done"

@app.route("/move_forward")
def move_forward():
    motorspeed = int(request.args.get('motorspeed', default=100))
    motor_driver.set_left_direction_clockwise(True)
    motor_driver.set_right_direction_clockwise(True)
    motor_driver.change_both_duty_cycles(motorspeed)
    return "Done"

@app.route("/move_backward")
def move_backward():
    motorspeed = int(request.args.get('motorspeed', default=100))
    motor_driver.set_left_direction_clockwise(False)
    motor_driver.set_right_direction_clockwise(False)
    motor_driver.change_both_duty_cycles(motorspeed)
    return "Done"

@app.route("/stop")
def stop():
    motor_driver.change_both_duty_cycles(0)
    motor_driver.set_standby_both()
    return "Done"

@app.route("/")
def remote():
    return render_template('remote.html', js_path=js_path)


def gen():
    """Video streaming generator function."""
    while True:
        rval, frame = vc.read()
        frame = cv2.flip(frame, flipCode=-1)
        cv2.imwrite(tmp_img_path, frame)
        yield (b'--frame\r\n'
               b'Content-Type: image/jpeg\r\n\r\n' + open(tmp_img_path, 'rb').read() + b'\r\n')


@app.route('/video_feed')
def video_feed():
    """Video streaming route. Put this in the src attribute of an img tag."""
    return Response(gen(),
                    mimetype='multipart/x-mixed-replace; boundary=frame')


if __name__ == "__main__":
    GPIO_MODE = GPIO.BCM
    GPIO.setmode(GPIO_MODE)

    motor_driver = l298n_mini.l298n(
        in1_pin=13,
        in2_pin=6,
        in3_pin=26,
        in4_pin=19,
        gpio_mode=GPIO_MODE)

    # remote_html = prepare_remote()
    js_path = os.path.join(dir_path, 'remote', 'python server', 'joystick.js')
    with open(js_path, 'r') as file:
        js_str = file.read()

    app.run(host='0.0.0.0', port=5000)