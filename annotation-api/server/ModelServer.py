import json
import os
import time
from os.path import dirname, abspath

from flask import request

from flask import jsonify
from werkzeug.utils import secure_filename

from database.db_mysql import db_mysql_detail
from server.LabelModelServer import LabelModelServer
from utils.HandleData import HandleData
from utils.MyResultRole import MyResultRole

'''
    处理model表   增删改查
'''


class ModelServer():
    """
      分页查询
      :return:
    """
    def limit_offset_query(self, pageNo=1, page_size=20, model_status=0, model_name=''):
        # 数据总量
        obj = db_mysql_detail()
        where_str = " "
        if model_name:
            where_str += " and " + "name like '%" + str(model_name) + "%'"
        if model_status:
            where_str += " and " + "status=" + str(model_status)
        total_count = obj.get_total_count(tablename='model', where_str=where_str)
        page_data = {
            'current_page': pageNo,
            'pageNo': pageNo,
            'page_size': page_size,
            'total': total_count,
            'total_page': 0
        }
        if total_count <= 0:
            page_data['total'] = 0
        # 总页数
        total_page = int(total_count / page_size) + 1
        page_data['total_page'] = total_page
        # 查询数据
        startone = (pageNo - 1) * page_size
        result_list = obj.get_tweet_by_page(startone, page_size, tablename='model', where_str=where_str)
        return {'data': result_list, 'page_data': page_data}

    '''删除model   即为表加上delete_time'''
    def delModel(self, model_id):
        if not model_id:
            return 0
        obj = db_mysql_detail()
        return obj.deleteItem(id=model_id, tablename='model')
    '''model 文件上传    返回文件存储的实际名称'''
    def uploadModel(self):
        data_path = HandleData.getModelContents()
        f = request.files['file']
        temp_filename = str(int(round(time.time() * 100000)))
        # 这里的名字最好需要是随机数
        f.save(os.path.join(data_path, secure_filename(temp_filename + f.filename)))
        return secure_filename(temp_filename + f.filename)

    '''增加Model  加上create_time'''
    def addModel(self):
        # model表处理
        json_data = HandleData.request_parse(request)
        obj = db_mysql_detail()
        if json_data['status'] and json_data['name'] and json_data['file_path']:
            items = {
                'name': json_data['name'],
                'status': json_data['status'],
                'create_time': int(time.time()),
                'file_path': json_data['file_path']
            }
        if str(json_data['status']) == '1':
            ModelServer.editModelStatus(ModelServer())
        model_id = obj.insert(table='model', items=HandleData.jsonToDict(items))
        if not model_id:
            return False
        json_temp_data = json.loads(json_data['select_data'])
        # print(type(json_temp_data))
        # print(list(json_temp_data))
        for item in json.loads(json_data['select_data']):
            #向关系表中添加数据
            LabelModelServer.addLabelModelRelation(LabelModelServer(),item,model_id)
        return True

    '''前端修改model状态  加上update_time'''
    def editModelStatus(self,status=1,target_status=2,id=0):
        if not status:
            return False
        where_str=''
        if not id:
            where_str = "status=" + str(status)
        else:
            where_str = "id=" + str(id)
        json_data={}
        json_data['status']=str(target_status)
        json_data['update_time'] = int(time.time())
        # del json_data['delete_time']
        dict_request_data = HandleData.jsonToDict(json_data)
        obj = db_mysql_detail()
        return obj.update(table='model', where=where_str, items=dict_request_data)


    '''前端修改model  加上update_time'''
    def editModel(self):
        json_data = HandleData.request_parse(request)
        obj = db_mysql_detail()
        table_property_arr = obj.get_column_name(tablename='model')
        for key in json_data:
            if key not in table_property_arr:
                del json_data[key]
        where_str = "id="+json_data['id']
        print(json_data)
        json_data['update_time'] = int(time.time())
        # del json_data['delete_time']
        dict_request_data = HandleData.jsonToDict(json_data)
        return obj.update(table='model', where=where_str, items=dict_request_data)

    '''根据特定条件获取model信息'''
    def getModelTopone(self, name="",status=0,id=0):
        if not name and not status and not id:
            return False
        obj = db_mysql_detail()
        where_str = ''
        if name:
            where_str = " name='" + str(name) + "'"
        if status:
            if where_str:
                where_str += " and status='" + str(status) + "'"
            else:
                where_str += "  status='" + str(status) + "'"
        if id:
            if where_str:
                where_str += " and id='" + str(id) + "'"
            else:
                where_str += " id='" + str(id) + "'"
        if not where_str:
            return None
        table_property_arr = obj.get_column_name(tablename='model')
        target_val = obj.selectTopone(table='model', where=where_str)
        # 根据列名生成 键值对
        target_data = {}
        for index, item in enumerate(target_val):
            for index2, item2 in enumerate(table_property_arr):
                if index == index2:
                    target_data[item2] = item
        return target_data
