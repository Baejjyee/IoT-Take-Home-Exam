from flask import Flask,render_template, request, redirect, url_for
import serial
import time
import cv2

app = Flask(__name__)

arduino = serial.Serial('/dev/ttyACM0',9600,timeout=1)
time.sleep(2)


@app.route('/')
def index():
    return render_template('index.html')

@app.route('/capture', methods=['POST'])
def capture():
    cap = cv2.VideoCapture(0)
    ret,frame = cap.read()
    if ret:
        timestamp = time.strftime("%Y%m%d-%H%M%S")
        image_path = f'./photo_{timestamp}.jpg'
        cv2.imwrite(image_path,frame)
        arduino.write(b'CAPTURE\n')
        arduino.write(b'MELODY\n')
    cap.release()
    return redirect(url_for('index'))

@app.route('/7segment', methods=['POST'])
def display_segment():
    number = request.form['number']
    arduino.write(f'SEGMENT:{number}\n'.encode())
    return redirect(url_for('index'))

@app.route('/lcd',methods=['POST'])
def display_lcd():
    text = request.form['text']
    arduino.write(f'LCD:{text}\n'.encode())
    return redirect(url_for('index'))

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)

