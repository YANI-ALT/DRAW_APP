import flask
from flask import Flask,render_template,url_for,request
import numpy as np
import cv2
import base64
import torch
import torch.nn as nn
import torchvision
import json
import math
from Mymodel import MyModel
init_base64=21
PATH='static/model.pth'
model = MyModel()
model.load_state_dict(torch.load(PATH))
# model = torch.load(PATH)
model.eval()

str1='abcdefghijklmnopqrstuvwxyz'
label={}
for i in range(len(str1)):
    label[i]=str1[i]

app=flask.Flask(__name__,template_folder='templates')


class NumpyEncoder(json.JSONEncoder):
    def default(self, obj):
        if isinstance(obj, np.ndarray):
            return obj.tolist()
        return json.JSONEncoder.default(self, obj)

@app.route('/')
def home():
    return render_template('index.html')

def get_prediciton(img):
    top_preds={}
    with torch.no_grad():
        y_val=model(img)
        print(y_val.data)
        predicted=torch.max(y_val.data,1)[1]
        pred_prob_sorted=torch.sort(y_val.data,descending=True)
        pred_prob=pred_prob_sorted.indices

        print("predicted:",pred_prob.indices)
        for pred in pred_prob[0][0:5]:
            print(pred.item())
            top_preds[label[pred.item()]]=y_val.data[0][pred.item()-1].item()
    print(top_preds)
    return label[predicted.item()],top_preds


@app.route('/predict',methods=["POST"])
def predict():
    if request.method=='POST':
        print("form here",request)
        req=request.get_json()
        draw=req['url']
        # draw=request.form['url']
        # sprint(draw)
        draw=draw[init_base64:]#the first 21 char are not data
        draw_decoded=base64.b64decode(draw)
        # print("here",draw_decoded)
        image=np.asarray(bytearray(draw_decoded),dtype='uint8')
        image=cv2.imdecode(image,cv2.IMREAD_GRAYSCALE)
        (thresh, im_bw) = cv2.threshold(image, 128, 255, cv2.THRESH_BINARY | cv2.THRESH_OTSU)
        resized=cv2.resize(im_bw,(28,28),interpolation=cv2.INTER_AREA)
        vect=np.asarray(resized,dtype="uint8")
        x = torchvision.transforms.functional.to_tensor(vect)
        x.unsqueeze_(0)
        # vect=vect.reshape(1,1,28,28)# image here is the input to the model
        result,top_result=get_prediciton(x)
        print("top predictions:",top_result.values())
        cv2.imwrite("img.png",resized)

    # return render_template('index.html',prediction=[1,2,3],x_val=['a','b','c'])
        value_=[ math.exp(x) for x in list(top_result.values())]
        print(value_)
        json_dump = json.dumps({"labels_x":list(top_result.keys()),"values":value_}, cls=NumpyEncoder)

    return (json_dump)


if __name__=='__main__':
    app.run(debug=True)
