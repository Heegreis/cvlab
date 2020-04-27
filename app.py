from flask import Flask, render_template, make_response, request , jsonify
from PIL import Image
import os , io , sys
import numpy as np 
import cv2
import base64

from utils.imgProcess import imgProcess

app = Flask(__name__)


@app.route('/process', methods=['POST'])
def process():
    # print(request.files , file=sys.stderr)
    file = request.files['image'].read() ## byte file
    npimg = np.frombuffer(file, np.uint8)
    img = cv2.imdecode(npimg,cv2.IMREAD_COLOR)
    ######### Do preprocessing here ################
    algorithm = request.form.get('algorithm')
    print(algorithm)
    # img = imgProcess(img, algorithm)
    ################################################
    img = Image.fromarray(img.astype("uint8"))
    rawBytes = io.BytesIO()
    img.save(rawBytes, "JPEG")
    rawBytes.seek(0)
    img_base64 = base64.b64encode(rawBytes.read())
    return jsonify({'status':str(img_base64)})


@app.after_request
def after_request(response):
    print("log: setting cors" , file = sys.stderr)
    response.headers.add('Access-Control-Allow-Origin', '*')
    response.headers.add('Access-Control-Allow-Headers', 'Content-Type,Authorization')
    response.headers.add('Access-Control-Allow-Methods', 'GET,PUT,POST,DELETE')
    return response

@app.route('/test', methods=['POST'])
def test():
    algorithm = request.form.getlist('algorithm')
    # hello = request.form.getlist('hello')
    print(algorithm)
    b_th = request.form.get('b:th')
    print(b_th)
    return render_template('test.html')

@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        algorithm = request.form.getlist('algorithm')
        print(algorithm)
        b_th = request.form.get('b:th')
        print(b_th)
        img = request.form.get('img')
        print(img)
    return render_template('index.html')

if __name__ == '__main__':
    app.run(debug=True)