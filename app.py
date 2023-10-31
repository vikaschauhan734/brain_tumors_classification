from flask import Flask, render_template, request
import numpy as np
import cv2
import os
from tensorflow.keras.models import load_model

app= Flask(__name__)
model = load_model('model.h5')

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/submit',methods=['POST','GET'])
def submit():
    if request.method=='POST':
        image = request.files['image']
        image = request.files['image']
        if image.filename != '':
            image.save(os.path.join('uploads', image.filename))

        img = cv2.imread(str(os.path.join('uploads', image.filename)))
        resized_img = cv2.resize(img, (256,256))
        resized_img = np.array(resized_img)
        resized_img = resized_img/255
        resized_img = resized_img.reshape(1,256,256,3)

        prediction = model.predict(resized_img)
        prediction = np.argmax(prediction, axis=1)[0]
        output = ""
        if prediction == 0:
            output="It is a Glioma Tumor."
        elif prediction == 1:
            output="It is a Meningioma Tumor."
        elif prediction == 2:
            output="Congratulations! Your report is Normal."
        elif prediction == 3:
            output="It is a Pituitary Tumor."
        else:
            output="Error Occured! Please use different image."
    return render_template('prediction.html',result=output)

if __name__=='__main__':
    app.run(debug=True)
