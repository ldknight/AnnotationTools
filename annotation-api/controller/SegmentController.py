from server.SegmentServer import SegmentServer
from flask import Blueprint, request
from utils.HandleData import HandleData
from utils.MyResultRole import MyResultRole

segment_api = Blueprint('segment_api', __name__)

# 查询label列表
@segment_api.route('/label/getSegmentList', methods=['POST', 'GET'])
def getSegmentList(img_id=0):
    img_id = HandleData.request_parse_equal(img_id, locals())
    res = SegmentServer.getAllSegmentList(SegmentServer(), img_id)
    return MyResultRole.ResSuccess(data=res)

# 删除label
@segment_api.route('/label/deleteSegment', methods=['POST', 'GET'])
def deleteSegment(img_id=0, segment_id=0):
    img_id = HandleData.request_parse_equal(img_id, locals())
    segment_id = HandleData.request_parse_equal(segment_id, locals())
    res_ = SegmentServer.deleteSegment(SegmentServer(),img_id=img_id, segment_id=segment_id)
    return MyResultRole.ResSuccess(data=res_)













