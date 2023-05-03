from flask import Flask, request, Response, render_template
import time
import os
import io
import json
from picamera import PiCamera

import RPi.GPIO as GPIO

from actuators import l298n_mini
from sensors import ina219

dir_path = os.path.dirname(os.path.realpath(__file__))
html_template_dir = os.path.join(dir_path, 'remote', 'python server')

app = Flask(__name__, template_folder=html_template_dir)

dir_path = os.path.dirname(os.path.realpath(__file__))
tmp_img_path = os.path.join(
    dir_path, 'remote', 'python server', 'tmp_photo', 'tmp_img.jpg')

# Camera settings
camera = PiCamera()
camera.resolution = (640, 480)
camera.framerate = 24
camera.rotation = 180

@app.route("/move")
def move():
    # parsing args
    left_speed = int(request.args.get('left_speed'))
    right_speed = int(request.args.get('right_speed'))
    print("Received speed values: left_speed:",left_speed,"| right_speed:", right_speed)
    # setting speed boundaries -100 > x < 100 
    left_speed = left_speed if left_speed > -100 else -100
    left_speed = left_speed if left_speed < 100 else 100
    right_speed = right_speed if right_speed > -100 else -100
    right_speed = right_speed if right_speed < 100 else 100
    print("Adjusted speed values: left_speed:",left_speed,"| right_speed:", right_speed)
    # setting rotation direction of left motor
    if left_speed < 0:
        motor_driver.set_left_direction_clockwise(False)
    else:
        motor_driver.set_left_direction_clockwise(True)
    # setting rotation direction of right motor
    if right_speed < 0:
        motor_driver.set_right_direction_clockwise(False)
    else:
        motor_driver.set_right_direction_clockwise(True)
    # controlling motors
    motor_driver.change_left_duty_cycle(abs(left_speed))
    motor_driver.change_right_duty_cycle(abs(right_speed))
    # setting standby if both cycles are 0
    if left_speed == 0 and right_speed == 0:
        motor_driver.set_standby_both()
    return "Done"

@app.route("/get_voltage")
def get_voltage():
    return json.dumps({"value":ina.get_voltage().split(" ")[0]})

@app.route("/")
def remote():
    return render_template('remote.html', js_path=js_path)

def gen():
    while True:
        with io.BytesIO() as output:
            camera.capture(output, format='jpeg', use_video_port=True, quality=20, resize=(640, 480))
            frame = output.getvalue()
        yield (b'--frame\r\n'
               b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n')

@app.route('/video_feed')
def video_feed():
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
    
    # voltage meter
    ina = ina219.ina219()

    # remote_html = prepare_remote()
    js_path = os.path.join(dir_path, 'remote', 'python server', 'joystick.js')
    with open(js_path, 'r') as file:
        js_str = file.read()

    app.run(host='0.0.0.0', port=5000)