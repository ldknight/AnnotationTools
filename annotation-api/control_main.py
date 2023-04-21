from flask import Flask,current_app
import os
import sys

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.append(BASE_DIR)

sys.path.append("..")
from segment_anything import sam_model_registry, SamPredictor
import numpy as np
import cv2
from config import sam_checkpoint,device,model_type

app = Flask(__name__)

from flask_cors import CORS, cross_origin

from controller.ProjectController import  project_api
from controller.ImagesController import  image_api
from controller.LabelController import  label_api
from controller.SegmentController import  segment_api

app.register_blueprint(project_api)
app.register_blueprint(image_api)
app.register_blueprint(label_api)
app.register_blueprint(segment_api)


#处理跨域
CORS(app,supports_credentials=True)
###########主函数  直接运行main
# 处理 json  返回格式
# app.config['JSON_AS_ASCII'] = False
# app.after_request(after_request(app))
@app.route('/')
# def index():
#     return "hello"
def test():
    return 'test'

# @app.before_first_request
# def first_request():
#     print(1)


if __name__ == "__main__":
    sam = sam_model_registry[model_type](checkpoint=BASE_DIR+sam_checkpoint)
    sam.to(device=device)
    predictor = SamPredictor(sam)
    # image = cv2.imread('/Users/liudun/Desktop/anno_tools/AnnotationTools/notebooks/images/truck.jpg')
    # image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
    # predictor.set_image(image)
    
    with app.app_context():  # 全局变量
        current_app.predictor=predictor
        current_app.sam=sam
        current_app.image=None
        current_app.image_url=""

    app.run()
