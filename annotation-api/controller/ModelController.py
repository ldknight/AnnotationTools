import os
from os.path import dirname, abspath

from server.LabelServer import LabelServer
from flask import Blueprint, request

from server.ModelServer import ModelServer
from utils.HandleData import HandleData
from utils.MyResultRole import MyResultRole

model_api = Blueprint('model_api', __name__)

@model_api.route('/model/getModelList', methods=['POST', 'GET'])
# 分页查询模型列表
def getModelList(pageNo=1, page_size=20, status=0,name=''):
    pageNo = HandleData.request_parse_equal(pageNo, locals())
    page_size = HandleData.request_parse_equal(page_size, locals())
    model_status = HandleData.request_parse_equal(status, locals())
    model_name = HandleData.request_parse_equal(name, locals())
    res = ModelServer.limit_offset_query(ModelServer(), pageNo=pageNo, page_size=page_size, model_status=model_status,model_name=model_name)
    return MyResultRole.ResSuccess(data=res)

@model_api.route('/model/addModel',methods=['POST','GET'])
#model模型增加
def addModel():
    res_flag = ModelServer.addModel(ModelServer())
    if res_flag:
        return MyResultRole.ResSuccess('添加成功！')
    return MyResultRole.ResError('添加失败！')

@model_api.route('/model/uploadModel',methods=['POST','GET'])
#模型上传
def uploadModel():
    res_flag = ModelServer.uploadModel(ModelServer())
    if res_flag:
        return MyResultRole.ResSuccess(msg='文件上传成功！',data=res_flag)
    return MyResultRole.ResError('添加失败！')

@model_api.route('/model/deleteModelfile',methods=['POST','GET'])
#模型删除-文件
def deleteModelfile(filename=""):
    filename = HandleData.request_parse_equal(filename, locals())
    data_path_final = HandleData.getModelContents()+'/'+ filename
    # 删除文件
    if os.path.exists(data_path_final):
        os.remove(data_path_final)
        if not os.path.exists(data_path_final):
            return MyResultRole.ResSuccess(msg='模型文件删除成功！')
    return MyResultRole.ResError(msg='模型文件删除失败！')


@model_api.route('/model/delModel',methods=['POST','GET'])
#模型删除-记录
def delModel(model_id=1):
    model_id = HandleData.request_parse_equal(model_id, locals())
    res_flag = ModelServer.delModel(ModelServer(),model_id=model_id)
    if res_flag:
        return MyResultRole.ResSuccess(msg='模型删除成功！',data=res_flag)
    return MyResultRole.ResError('模型删除失败！')


@model_api.route('/model/useThisModel',methods=['POST','GET'])
#模型修改使用状态 使用该模型
def useThisModel(model_id=1):
    model_id = HandleData.request_parse_equal(model_id, locals())

    target_model_detail = ModelServer.getModelTopone(ModelServer(),id=model_id)
    model_path = HandleData.getModelContents()
    if not os.path.exists(model_path+'/'+target_model_detail['file_path']):
        return MyResultRole.ResError(msg='模型文件不存在！')

    temp_model = ModelServer.editModelStatus(ModelServer())
    this_model = ModelServer.editModelStatus(ModelServer(),target_status=1,id=model_id)
    if this_model and temp_model:
        return MyResultRole.ResSuccess(msg='模型修改成功！')
    return MyResultRole.ResError(msg='模型修改失败！')
