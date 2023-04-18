import json
import time
from flask import request

from flask import jsonify

from database.db_mysql import db_mysql_detail
from utils.HandleData import HandleData
from utils.MyResultRole import MyResultRole

'''
    处理label表   增删改查
'''
class SegmentServer():

    '''get all Segment'''
    def getAllSegmentList(self,img_id=0):
        obj = db_mysql_detail()
        where_str = " delete_time is null and img_id="+str(img_id)+" "
        target_val = obj.selectAll(table='segment', where=where_str,order=" create_time desc")
        return target_val

    @staticmethod
    def insertSegment(img_id,proj_id,masks):
        obj = db_mysql_detail()
        items={}
        sucess=0
        for mask in masks:
            items["seg_field"]=str(mask['segmentation'])
            items["img_id"]=int(img_id)
            items["proj_id"]=int(proj_id)
            sucess+=obj.insert(table="segment",items=items.items())
        return sucess
        