from server.LabelServer import LabelServer
from flask import Blueprint, request
from utils.HandleData import HandleData
from utils.MyResultRole import MyResultRole

label_api = Blueprint('label_api', __name__)

@label_api.route('/label/getLabelList', methods=['POST', 'GET'])
# 分页查询label列表
def getLabelList(pageNo=1, page_size=20, name="", status=0):
    pageNo = HandleData.request_parse_equal(pageNo, locals())
    page_size = HandleData.request_parse_equal(page_size, locals())
    label_name = HandleData.request_parse_equal(name, locals())
    label_status = HandleData.request_parse_equal(status, locals())

    res = LabelServer.limit_offset_query(LabelServer(), pageNo=pageNo, page_size=page_size, label_name=label_name,
                                         label_status=label_status)
    return MyResultRole.ResSuccess(data=res)


@label_api.route('/label/deleteLabel', methods=['POST', 'GET'])
# 删除label
def deleteLabel(label_id=0):
    label_id = HandleData.request_parse_equal(label_id, locals())
    res_flag = LabelServer.deleteLabel(LabelServer(), label_id)
    if res_flag:
        return MyResultRole.ResSuccess(msg='删除成功！')
    else:
        return MyResultRole.ResError(msg="删除失败")


@label_api.route('/label/addLabel', methods=['POST', 'GET'])
# 添加label
def addLabel(name='', status=2):
    name = HandleData.request_parse_equal(name, locals())
    status = HandleData.request_parse_equal(status, locals())
    res_flag = LabelServer.addLabel(LabelServer(), name=name, status=status)
    if res_flag:
        return MyResultRole.ResSuccess('添加成功！')
    return MyResultRole.ResError('添加失败！')


@label_api.route('/label/editLabel', methods=['POST', 'GET'])
# 更新label id必传
def editLabel(name=''):
    name = HandleData.request_parse_equal(name, locals())
    res_flag = LabelServer.editLabel(LabelServer())
    if res_flag:
        return MyResultRole.ResSuccess(msg="'" + name + "' 信息修改成功！")
    return MyResultRole.ResError(msg="'" + name + "'信息修改失败！")


