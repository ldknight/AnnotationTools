from flask import Flask, render_template, request, session,redirect,url_for
from zipfile import ZipFile
from io import BytesIO
from PIL import Image
from werkzeug.utils import secure_filename
import os
import uuid
import glob

app = Flask(__name__)
ALLOWED_EXTENSIONS = {'zip'}
app.secret_key = 'annotationmycz'
static_path="web/static/images"
# 设置静态文件夹的路径
app.static_folder = os.path.join(os.path.abspath(os.path.dirname(__file__)), 'static')
image_extensions = ['.jpg', '.jpeg', '.png', '.gif']
global_imgpaths={}

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS


@app.route('/')
def index():
    return render_template('index.html')


@app.route('/upload', methods=['POST'])
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
def showdis():
    dirs = os.listdir(static_path)
    links = []
    
    for dir in dirs:
        dirname="_".join(dir.split("_")[1:])
        links.append([dir,dirname])
       
    return render_template('dirs.html',links=links)


    
# /annotation/<path:filepath>?id=0 代表当filepath目录下第一张图片
@app.route('/annotation/<path:imgs_path>', methods=['GET'])
def annotation(imgs_path):
    r_imgs_path=os.path.join(app.static_folder,"images", imgs_path)
    if imgs_path not in global_imgpaths:
        image_files = [os.path.join("images",imgs_path,os.path.basename(file)) for file in glob.glob(os.path.join(r_imgs_path, '*')) 
                       if os.path.splitext(file)[1] in image_extensions]
        
        global_imgpaths[imgs_path]=image_files
    id = request.args.get('id')
    if not id or int(id) <0:
        id=0
    id=int(id)
    if id>len(global_imgpaths[imgs_path])-1:
       id=len(global_imgpaths[imgs_path])-1
    
    return render_template('annotation.html',id=id,dirpath=imgs_path ,image_paths=[global_imgpaths[imgs_path][id]])

    # return f'User Profile for User ID: {id}'




if __name__ == '__main__':
    app.run(debug=True)
