from server.ImagesServer import ImagesServer
from server.PublicServer import PublicServer
from flask import Blueprint, request
from utils.HandleData import HandleData
from utils.MyResultRole import MyResultRole
import json
image_api = Blueprint('image_api', __name__)

@image_api.route('/image/getImageList', methods=['POST', 'GET'])
# 分页查询images列表
def getImageList(pageNo=1, page_size=20, proj_id=0):
    pageNo = HandleData.request_parse_equal(pageNo, locals())
    page_size = HandleData.request_parse_equal(page_size, locals())
    proj_id = HandleData.request_parse_equal(proj_id, locals())

    res = ImagesServer.limit_offset_query(ImagesServer(), pageNo=pageNo, page_size=page_size,proj_id=proj_id)
    return MyResultRole.ResSuccess(data=res)


@image_api.route('/image/clear_img_segment', methods=['POST', 'GET'])
# 分页查询images列表
def clear_img_segment(img_id=0):
    img_id = HandleData.request_parse_equal(img_id, locals())
    res = PublicServer.clear_img_segment(PublicServer(),img_id=img_id)
    return MyResultRole.ResSuccess(data=res)


@image_api.route('/image/get_img_segment', methods=['POST', 'GET'])
# 分页查询images列表
def get_img_segment(img_id=0,proj_id=0,interest_field=[]):
    img_id = HandleData.request_parse_equal(img_id, locals())
    proj_id = HandleData.request_parse_equal(proj_id, locals())
    interest_field = HandleData.request_parse_equal(interest_field, locals())
    #处理interest_field 起初是dict 但每个元素都是单一元素
    a=""
    for item in interest_field:
        a=a+item
    interest_field_dist = json.loads(a)

    res = ImagesServer.get_img_segment(ImagesServer(),img_id=img_id,proj_id=proj_id,interest_field=interest_field_dist)
    return MyResultRole.ResSuccess(data=res)





