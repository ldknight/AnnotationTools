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
        for item in target_val:
            item["seg_field"]=HandleData.decode(item["seg_field"])
            item["field_items"]=HandleData.decode(item["field_items"])

            item["seg_field"]=json.loads(item["seg_field"].replace("\'","\""))
            item["field_items"]=json.loads(item["field_items"].replace("\'","\""))
        
        return target_val
    
    '''Segment   即为表加上delete_time'''
    def deleteSegment(self,img_id=0, segment_id=0):
        obj = db_mysql_detail()
        obj.deleteItem(id=segment_id, tablename='segment')
        return SegmentServer.getAllSegmentList(self,img_id)
    
    def update_segment(self,id=0,label_id=0):
        obj = db_mysql_detail()
        json_data = HandleData.request_parse(request)
        table_property_arr = obj.get_column_name(tablename='segment')
        for key in json_data:
            if key not in table_property_arr:
                del json_data[key]
        where_str = "id="+json_data['id']
        dict_request_data = HandleData.jsonToDict(json_data)
        obj.update(table='segment', where=where_str, items=dict_request_data)

        where_str = " delete_time is null and id="+str(json_data['id'])+" "
        return obj.selectTopone(table='segment', where=where_str)

    def selectSegmentTopone(self,segment_id=0,label_id=0):
        obj = db_mysql_detail()
        where_str = " delete_time is null "
        if segment_id:
            where_str = " delete_time is null and id="+str(segment_id)+" "
        if label_id:
            where_str = " delete_time is null and label_id="+str(label_id)+" "
        return obj.selectTopone(table='segment', where=where_str)

