from flask import Flask, render_template, request, session,redirect,url_for,jsonify
from zipfile import ZipFile
from io import BytesIO
from PIL import Image
from werkzeug.utils import secure_filename
import os
import uuid
import glob
import numpy as np
import torch
import json
import matplotlib.pyplot as plt
import cv2
from config import sam_checkpoint,device,model_type
import sys
from functools import wraps
from segment_anything import sam_model_registry, SamAutomaticMaskGenerator, SamPredictor

sys.path.append("..")
sam = sam_model_registry[model_type](checkpoint=sam_checkpoint)
sam.to(device=device)
predictor = SamPredictor(sam)
mask_generator = SamAutomaticMaskGenerator(sam)

app = Flask(__name__)
ALLOWED_EXTENSIONS = {'zip'}
app.secret_key = 'annotationmycz'
static_path="web/static/images"
# 设置静态文件夹的路径
app.static_folder = os.path.join(os.path.abspath(os.path.dirname(__file__)), 'static')
image_extensions = ['.jpg', '.jpeg', '.png', '.gif']
global_imgpaths={}

def login_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        # 检查用户是否有有效的会话
        if 'user_info' not in session:
            # 如果没有会话，重定向到登录页面
            return redirect(url_for(''))
        # 如果有会话，继续处理请求
        return f(*args, **kwargs)
    return decorated_function

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

@app.route('/')
def index():
    session['user_info']={}
    return render_template('index.html')

@app.route('/upload', methods=['POST'])
@login_required
def upload():
    file = request.files['file']
    if file and allowed_file(file.filename):
        filename = secure_filename(file.filename)
        folder_name = str(uuid.uuid4())
        folder_path = os.path.join('images', folder_name+"_"+filename.split(".")[0])
        os.makedirs(os.path.join(app.static_folder, folder_path))
        file_path = os.path.join(app.static_folder, folder_path, filename)
        file.save(file_path)
        with ZipFile(file_path, 'r') as zip_file:
            image_paths = []
            for file_name in zip_file.namelist():
                if file_name.endswith(('.jpg', '.jpeg', '.png')):
                    # 解压缩并保存图片到静态文件夹中
                    image_data = zip_file.read(file_name)
                    image_stream = BytesIO(image_data)
                    image = Image.open(image_stream)
                    image_path = os.path.join(folder_path, file_name)
                    image.save(os.path.join(app.static_folder, image_path))
                    image_paths.append(image_path)
        # 删除上传的压缩包
        os.remove(file_path)
        return render_template('index.html', image_paths=image_paths)

    return "Failed to process uploaded file"

@app.route('/dirs', methods=['GET'])
@login_required
def showdis():
    dirs = os.listdir(static_path)
    links = []
    
    for dir in dirs:
        dirname="_".join(dir.split("_")[1:])
        links.append([dir,dirname])
       
    return render_template('dirs.html',links=links)
    
    
# /annotation/<path:filepath>?id=0&lens=2 从0开始返回两张图片地址
@app.route('/annotation/<path:imgs_path>', methods=['GET'])
@login_required
def annotation(imgs_path):
    r_imgs_path=os.path.join(app.static_folder,"images", imgs_path)
    if imgs_path not in global_imgpaths:
        image_files = [os.path.join("images",imgs_path,os.path.basename(file)) for file in glob.glob(os.path.join(r_imgs_path, '*')) 
                       if os.path.splitext(file)[1] in image_extensions]
        
        global_imgpaths[imgs_path]=image_files
    totallens=len(global_imgpaths[imgs_path])
    id = request.args.get('id')
    if not id or int(id) <0:
        id=0
    id=int(id)
    if id>totallens-1:
       id=totallens-1
    lens=request.args.get('lens')
    if not lens:
        lens=1
    lens=int(lens)
    if lens<=0:
        lens=1
    elif lens>totallens:
        lens=totallens
    # return global_imgpaths[imgs_path][id:id+lens]
    return render_template('annotation.html',id=id,dirpath=imgs_path ,image_paths=[global_imgpaths[imgs_path][id]])

@app.route('/annotation_label')
@login_required
def annotation_label():
    data = request.get_json()
    masks = data['mask']
    imageSrc = data["imageSrc"]
    label = data["label"]
    session['user_info'][imageSrc].append([imageSrc, masks, label])
    return [imageSrc,masks,label]

def ndarray_to_list(d):
    for value in d:
        for key, v in value.items():
            if key=="segmentation":
                value[key]=np.where(v, 255, 0)
                img=cv2.Canny(np.uint8(value[key]),50,100)
                img[img < 255] = 0
                row_indices, col_indices = np.where(img == 255)
                value[key] = list(zip(row_indices, col_indices))
                
            if isinstance(value[key], np.ndarray):
                value[key] = value[key].tolist()
    return d

class NpEncoder(json.JSONEncoder):
    def default(self, obj):
        if isinstance(obj, np.integer):
            return int(obj)
        if isinstance(obj, np.floating):
            return float(obj)
        if isinstance(obj, np.ndarray):
            return obj.tolist()
        return super(NpEncoder, self).default(obj)

@app.route('/handle_autosegment', methods=['POST'])
@login_required
def autosegment():
    data = request.get_json()
    path=os.path.join(app.static_folder,data["imageSrc"][1:]).replace("/static/", "/", 1)
    image = cv2.imread(path)
    image = cv2.cvtColor(image,cv2.COLOR_BGR2RGB)
    path=os.path.join(app.static_folder,data["imageSrc"][1:]).replace("/static/", "/", 1)
    masks = mask_generator.generate(image)
    masks=ndarray_to_list(masks)
    senddata={
        'masks':masks,
    }
    
    session['user_info'][data["imageSrc"]]=[]
    senddata=json.dumps(senddata, cls=NpEncoder)
    return jsonify(senddata)
    
@app.route('/handle_segment', methods=['POST'])
@login_required
def segment():
    data = request.get_json()
    input_point=None
    input_label=None
    input_box=None
    if 'points' in data:
        input_point=[]
        input_label=[]
        points = data['points']
        for point in points:
            input_point.append([point["x"],point["y"]])
            input_label.append(point["label"])
        input_point=np.array(input_point)
        input_label=np.array(input_label)
    if 'boxs' in data:
        input_box=[]
        boxs=data["boxs"]
        for box in boxs:
            input_box.append(box)
        input_box=np.array(input_box)  
    path=os.path.join(app.static_folder,data["imageSrc"][1:]).replace("/static/", "/", 1)
    image = cv2.imread(path)
    image = cv2.cvtColor(image,cv2.COLOR_BGR2RGB)
    predictor.set_image(image)
    masks, scores, _ = predictor.predict(
    point_coords=input_point,
    point_labels=input_label,
    box=input_box,
    multimask_output=True,
    )
    senddata={
        'masks':masks.tolist(),
        'scores':scores.tolist(),
    }
    session['user_info'][data["imageSrc"]]=[]
    return jsonify(senddata)


@app.route('/get_labels', methods=['get'])
@login_required
def get_labels():
    with open('labels.txt', 'r') as f:
        content = f.read()
    
    # 按逗号分割字符串
    data = content.split(',')
    
    # 返回给前端
    return jsonify({'labels': data})

@app.route('/set_labels', methods=['POST'])
@login_required
def set_labels():
    data = request.get_json()
    labels = data['labels']
    with open('labels.txt', 'w') as f:
        f.write(",".join(labels))
        
    return "set_labels_ok"


if __name__ == '__main__':
    app.run(debug=True)
