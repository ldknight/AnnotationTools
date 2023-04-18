from server.LabelServer import LabelServer
from flask import Blueprint, request
from utils.HandleData import HandleData
from utils.MyResultRole import MyResultRole

label_api = Blueprint('label_api', __name__)

# 查询label列表
@label_api.route('/label/getLabelList', methods=['POST', 'GET'])
def getLabelList(proj_id=0):
    proj_id = HandleData.request_parse_equal(proj_id, locals())
    res = LabelServer.getAllLabelList(LabelServer(), proj_id)
    return MyResultRole.ResSuccess(data=res)

@label_api.route('/label/addLabel', methods=['POST', 'GET'])
def addLabel(name="",proj_id=0):
    name = HandleData.request_parse_equal(name, locals())
    proj_id = HandleData.request_parse_equal(proj_id, locals())
    res = LabelServer.addLabel(LabelServer(),name=name,proj_id=proj_id)
    return MyResultRole.ResSuccess(data=res)

@label_api.route('/label/deleteLabel', methods=['POST', 'GET'])
def deleteLabel(label_id=0,proj_id=0):
    label_id = HandleData.request_parse_equal(label_id, locals())
    proj_id = HandleData.request_parse_equal(proj_id, locals())
    res = LabelServer.deleteLabel(LabelServer(),label_id=label_id,proj_id=proj_id)
    return MyResultRole.ResSuccess(data=res)


@label_api.route('/label/editLabel', methods=['POST', 'GET'])
def editLabel(proj_id=0):
    proj_id = HandleData.request_parse_equal(proj_id, locals())
    res = LabelServer.editLabel(LabelServer(),proj_id=proj_id)
    return MyResultRole.ResSuccess(data=res)





