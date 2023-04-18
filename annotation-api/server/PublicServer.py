import os
import sys
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.append(BASE_DIR)
# #接后续代码

import json
import time
from flask import request
from flask import jsonify
from database.db_mysql import db_mysql_detail
from utils.HandleData import HandleData
from utils.MyResultRole import MyResultRole
import os
from glob import glob

from server.ImagesServer import ImagesServer
from server.LabelServer import LabelServer
from server.SegmentServer import SegmentServer

"""
    处理
"""


class PublicServer:
    '''清除画布信息 返回处理的行数'''
    def clear_img_segment(self,img_id=0):
        #删除图片对应的segment
        obj = db_mysql_detail()
        obj.deleteItem_condition(where_condition=" img_id="+str(img_id)+" ", tablename='segment')
        return SegmentServer.getAllSegmentList(SegmentServer(),img_id=img_id)
    


# if __name__=="__main__":
#     print(PublicServer.clear_img_segment(PublicServer,img_id=1))