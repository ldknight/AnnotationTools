import json
import time
from flask import request

from flask import jsonify

from database.db_mysql import db_mysql_detail
from utils.HandleData import HandleData
from utils.MyResultRole import MyResultRole
from server.SegmentServer import SegmentServer

'''
    处理label表   增删改查
'''
class LabelServer():
    '''get all labels'''
    def getAllLabelList(self,proj_id=0):
        obj = db_mysql_detail()
        where_str = " delete_time is null and proj_id="+str(proj_id)+" "
        target_val = obj.selectAll(table='label', where=where_str,order=" create_time desc")
        return target_val
    
    '''增加label  加上create_time'''
    def addLabel(self, name="", proj_id=0):
        obj = db_mysql_detail()
        items = {'name': name, 'proj_id': proj_id, 'create_time': int(time.time())}
        obj.insert(table='label', items=HandleData.jsonToDict(items))
        where_str = " delete_time is null and proj_id="+str(proj_id)+" "
        target_val = obj.selectAll(table='label', where=where_str,order=" create_time desc")
        return target_val
        
    '''修改label  加上update_time'''
    def editLabel(self,proj_id=0):
        obj = db_mysql_detail()
        json_data = HandleData.request_parse(request)
        table_property_arr = obj.get_column_name(tablename='label')
        for key in json_data:
            if key not in table_property_arr:
                del json_data[key]
        where_str = "id="+json_data['id']
        dict_request_data = HandleData.jsonToDict(json_data)
        obj.update(table='label', where=where_str, items=dict_request_data)
        return LabelServer.getAllLabelList(self,proj_id=proj_id)

    '''删除label   即为表加上delete_time'''
    def deleteLabel(self, label_id=0,proj_id=0):
        obj = db_mysql_detail()
        #同时要修改所有与label相关的segment信息
        where_str = " delete_time is null and label_id="+str(label_id)+" "
        json_data={"label_id":"NULL"}
        dict_request_data = HandleData.jsonToDict(json_data)
        obj.update(table='segment', where=where_str, items=dict_request_data)
        obj.deleteItem(id=label_id, tablename='label')
        return LabelServer.getAllLabelList(self,proj_id=proj_id)

