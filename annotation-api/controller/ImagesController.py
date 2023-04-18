from server.ImagesServer import ImagesServer
from flask import Blueprint, request
from utils.HandleData import HandleData
from utils.MyResultRole import MyResultRole

image_api = Blueprint('image_api', __name__)

@image_api.route('/image/getImageList', methods=['POST', 'GET'])
# 分页查询images列表
def getImageList(pageNo=1, page_size=20, proj_id=0):
    pageNo = HandleData.request_parse_equal(pageNo, locals())
    page_size = HandleData.request_parse_equal(page_size, locals())
    proj_id = HandleData.request_parse_equal(proj_id, locals())

    res = ImagesServer.limit_offset_query(ImagesServer(), pageNo=pageNo, page_size=page_size,proj_id=proj_id)
    return MyResultRole.ResSuccess(data=res)







