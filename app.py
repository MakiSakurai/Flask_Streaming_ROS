import time
from flask import Flask, render_template, Response
import cv2 as cv

app=Flask(__name__)
camera = cv.VideoCapture(0)

def gen_frames():

    while True:
        success, frame = camera.read()

        if not success:
            print("video capture error")
            break
        
        else:
            result, img = cv.imencode('.jpg', frame)
            frame = img.tobytes()        
            yield (b'--frame\r\n' + b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n')

@app.route('/feed')
def feed():
    return Response(gen_frames(), mimetype='multipart/x-mixed-replace; boundary=frame')


@app.route('/')
@app.route('/index')
def index():
    return render_template('index.html')

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=8080)
