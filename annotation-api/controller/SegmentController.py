from server.SegmentServer import SegmentServer
from server.PublicServer import PublicServer
from flask import Blueprint, request
from utils.HandleData import HandleData
from utils.MyResultRole import MyResultRole

segment_api = Blueprint('segment_api', __name__)

# 查询segment列表
@segment_api.route('/segment/getSegmentList', methods=['POST', 'GET'])
def getSegmentList(img_id=0):
    img_id = HandleData.request_parse_equal(img_id, locals())
    res = SegmentServer.getAllSegmentList(SegmentServer(), img_id)
    return MyResultRole.ResSuccess(data=res)

# 删除segment
@segment_api.route('/segment/deleteSegment', methods=['POST', 'GET'])
def deleteSegment(img_id=0, segment_id=0):
    img_id = HandleData.request_parse_equal(img_id, locals())
    segment_id = HandleData.request_parse_equal(segment_id, locals())
    res_ = SegmentServer.deleteSegment(SegmentServer(),img_id=img_id, segment_id=segment_id)
    return MyResultRole.ResSuccess(data=res_)

# 编辑segment
@segment_api.route('/segment/update_segment', methods=['POST', 'GET'])
def update_segment(id=0, label_id=0):
    res_ = SegmentServer.update_segment(SegmentServer())
    return MyResultRole.ResSuccess(data=res_)


# segment
@segment_api.route('/segment/selectSegmentTopone', methods=['POST', 'GET'])
def selectSegmentTopone(segment_id=0,label_id=0):
    segment_id = HandleData.request_parse_equal(segment_id, locals())
    label_id = HandleData.request_parse_equal(label_id, locals())
    res_ = SegmentServer.selectSegmentTopone(SegmentServer(),segment_id=segment_id,label_id=label_id)
    return MyResultRole.ResSuccess(data=res_)

# download_annotationtxt
@segment_api.route('/segment/download_annotationtxt', methods=['POST', 'GET'])
def download_annotationtxt(proj_id=0):
    proj_id = HandleData.request_parse_equal(proj_id, locals())
    res_ = PublicServer.download_annotationtxt(PublicServer(),proj_id=proj_id)
    return MyResultRole.ResSuccess(data=res_)






