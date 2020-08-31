#!/usr/bin/env python
# -*- coding: utf-8 -*-
from flask import render_template
from flask import Flask, flash, request, redirect, url_for, json
from werkzeug.utils import secure_filename
import io
import tensorflow as tf
import numpy as np
from keras.models import model_from_json
from PIL import Image
import os
import scipy
import base64
from skimage.transform import resize

ALLOWED_EXTENSIONS = {'jpg','png','jpeg'}

app = Flask(__name__,static_url_path='/static')

model = None
graph = None


def img_to_base64_str( img):
    buffered = io.BytesIO()
    img.save(buffered, format="PNG")
    buffered.seek(0)
    return "data:image/png;base64,{}".format(base64.b64encode(buffered.getvalue()).decode())


def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS


def compile_model():
    global model
    json_file = open(os.getenv('NN_MODEL', 'model.json'), 'r')
    loaded_model_json = json_file.read()
    json_file.close()
    model = model_from_json(loaded_model_json)
    model.load_weights(os.getenv('NN_WEIGHTS', 'test.h5'))
    print("Loaded model from disk")

    model.compile(
        optimizer= "adam",
        loss= "mse")

    global graph
    graph = tf.get_default_graph() 


@app.route('/predict',methods=['POST'])
def predict():
   
    file = request.files['file']
    if file.filename == '':
        response = app.response_class(
            response=json.dumps({"error":"No selected file"}),
            status=401,
            mimetype='application/json'
        )
        return response


    if file and allowed_file(file.filename):
        img = Image.open(io.BytesIO(file.stream.read()))
        old_shape = np.asarray( img, dtype="int32" ).shape
        old_image =  np.asarray( img, dtype="int32" )
        data = np.asarray( img.resize((256,256), Image.ANTIALIAS), dtype="int32" )
        x_image = np.array(data[...,:3])/127.5 - 1.

        global model
        global graph

        with graph.as_default():
            prediction= model.predict(x_image[np.newaxis,...])[0]

        prediction = np.stack([prediction[:,:,0]]*3,axis=2) * 255

        prediction = resize(prediction,old_shape,0,preserve_range=True)
        
        encoded_string = img_to_base64_str(Image.fromarray(np.uint8(np.clip(prediction , 0, 255) )))

        image_with_mask = np.where( prediction > 127.5, old_image, old_image * 0.5)

        encoded_string_2 = img_to_base64_str(Image.fromarray(np.uint8(image_with_mask)))

        response = app.response_class(
            response=json.dumps({"encoded":encoded_string,"encoded_2":encoded_string_2}),
            status=201,
            mimetype='application/json'
        )
        return response

    response = app.response_class(
            response=json.dumps({"error":"No allowed file"}),
            status=404,
            mimetype='application/json'
        )
    return response


@app.route('/', methods=['GET'])
def index():
    return render_template('index.html')


compile_model()
if __name__ == '__main__':
    app.config['SECRET_KEY'] = os.getenv('SECRET_KEY', 'O$%7kQgXKVOhT@refsbY;mQmt9lMWg')
    port = os.getenv('PORT', 9000)
    print('port=', port)
    app.run(host='0.0.0.0', debug=True, port=port)
