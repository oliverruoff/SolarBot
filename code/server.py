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

# -100 > y < 100 --> forward / backward
# -100 > x < 100 --> left    / right
@app.route("/move")
def move():
    x = int(request.args.get('x'))
    y = int(request.args.get('y'))

    # cleaning x data
    if x > 100:
        x = 100
    elif x < -100:
        x = -100
    # cleaning y data
    if y > 100:
        y = 100
    elif y < -100:
        y = -100

    print('x:', x)
    print('y:', y)
    abs_y = abs(y)
    abs_x = abs(x)
    if x == 0 and y == 0:
        motor_driver.set_standby_both()
        return 'Stopped motors.'

    if y > 0:
        motor_driver.set_both_direction_clockwise(True)
    elif y < 0:
        motor_driver.set_both_direction_clockwise(False)

    if x == 0:
        motor_driver.change_both_duty_cycles(abs_y)
        return 'Done'

    if x > 0:
        left = abs_y
        right = int(abs_y - (abs_x*(abs_y/100)))
    elif x < 0:
        right = abs_y
        left = int(abs_y - (abs_x*(abs_y/100)))
    print('Left:', left)
    print('Right:', right)
    motor_driver.change_left_duty_cycle(left)
    motor_driver.change_right_duty_cycle(right)
    return 'Done'


@app.route("/joystickscript")
def joystickscript():
    return js_str


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