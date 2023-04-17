from server.LabelServer import LabelServer
from flask import Blueprint, request

from server.MessageServer import MessageServer
from server.ModelServer import ModelServer
from utils.HandleData import HandleData
from utils.MyResultRole import MyResultRole

message_api = Blueprint('message_api', __name__)

@message_api.route('/message/getMessageOne', methods=['POST', 'GET'])
# 获取单个message
def getMessageOne(id=0):
    id = HandleData.request_parse_equal(id, locals())
    res = MessageServer.getMessageOne(MessageServer(), id=id)
    return MyResultRole.ResSuccess(data=res)

@message_api.route('/message/getMessageList', methods=['POST', 'GET'])
#分页查询用户列表
def getMessageList(pageNo=1,page_size=20):
    pageNo = HandleData.request_parse_equal(pageNo, locals())
    page_size = HandleData.request_parse_equal(page_size, locals())
    res = MessageServer.limit_offset_query(MessageServer(),pageNo=pageNo, page_size=page_size)
    return MyResultRole.ResSuccess(data=res)


@message_api.route('/message/editMessage',methods=['POST','GET'])
#编辑用户信息
def editMessage():
    res_flag = MessageServer.editMessage(MessageServer())
    if res_flag:
        return MyResultRole.ResSuccess(msg="信息修改成功！")
    return MyResultRole.ResError(msg="信息修改失败！")
