from flask import Flask

app = Flask(__name__)

from flask_cors import CORS, cross_origin

from controller.ProjectController import  project_api
from controller.ImagesController import  image_api

app.register_blueprint(project_api)
app.register_blueprint(image_api)


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
if __name__ == "__main__":
    app.run()
