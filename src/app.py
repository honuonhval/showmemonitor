#!/usr/bin/env python

from flask import Flask, render_template, Response, send_file
import subprocess
try:
    from camera import Camera
except ImportError:
    from stream import LocalStream as camera

app = Flask(__name__)


@app.route('/')
def hello():
    return render_template('index.html')

def gen(camera):
    while True:
        frame = camera.get_frame()
        yield (b'--frame\r\n'
               b'Content-Type: image\r\n\r\n' + frame + b'\r\n')

@app.route('/stream')
def video_stream():
    def generate():
        p = subprocess.Popen('cat src/sf.mp4 | ffmpeg -i - ' \
                             ' -movflags frag_keyframe+empty_moov' \
                             ' -vf scale=640:-1' \
                             ' -f mp4 -', shell=True, stdin=subprocess.PIPE, stdout=subprocess.PIPE)

        for data in iter(p.stdout.readline, b''):
            yield data
    return Response(generate(), mimetype='video/mp4')

@app.route('/video')
def video():
    return render_template('stream.html')

@app.route('/monitor')
def monitor():
    return Response(gen(Camera()),
                    mimetype='multipart/x-mixed-replace; boundary=frame')

@app.route('/get/<path:file>')
def get(file):
    return send_file(file)


if __name__ == '__main__':
    app.run(debug=True)
