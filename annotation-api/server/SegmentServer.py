import json
import time
from flask import request

from flask import jsonify

from database.db_mysql import db_mysql_detail
from utils.HandleData import HandleData
from utils.MyResultRole import MyResultRole

'''
    处理segment表   增删改查
'''
class SegmentServer():
    '''get all Segment'''
    def getAllSegmentList(self,img_id=0):
        obj = db_mysql_detail()
        where_str = " delete_time is null "
        if img_id:
            where_str = " delete_time is null and img_id="+str(img_id)+" "
        target_val = obj.selectAll(table='segment', where=where_str,order=" create_time desc")
        return target_val
    
    '''Segment   即为表加上delete_time'''
    def deleteSegment(self,img_id=0, segment_id=0):
        obj = db_mysql_detail()
        obj.deleteItem(id=segment_id, tablename='segment')
        return SegmentServer.getAllSegmentList(self,img_id)


