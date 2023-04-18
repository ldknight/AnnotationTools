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
class LabelServer():
    # '''
    #     用户查询（分页）
    # '''
    # def userSelectAll(self):
    #     obj = db_mysql_detail()
    #     sql = 'select * from user'
    #     data = obj.getAll_sql(sql)
    #     return MyResultRole.ResSuccess(data=data)
    """
      分页查询
      :return:
    """
    def limit_offset_query(self,pageNo=1, page_size=20, label_name='', label_status=0):
        # 数据总量
        obj = db_mysql_detail()
        where_str=" "
        if label_name:
            where_str += " and "+"name like '%" + str(label_name)+"%'"
        if label_status:
            where_str += " and "+"status=" + str(label_status)
        total_count = obj.get_total_count(tablename='label', where_str=where_str)
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
        total_page = int(total_count / page_size)+1
        page_data['total_page'] = total_page
        # 查询数据
        startone = (pageNo-1)*page_size
        result_list = obj.get_tweet_by_page(startone, page_size, tablename='label', where_str=where_str)
        return {'data': result_list, 'page_data': page_data}
        # print(result_list)

    '''删除label   即为表加上delete_time'''
    def deleteLabel(self, label_id):
        if not label_id:
            return 0
        obj = db_mysql_detail()
        return obj.deleteItem(id=label_id, tablename='label')

    '''增加label  加上create_time'''
    def addLabel(self, name, status=2):
        obj = db_mysql_detail()
        items = {'name': name, 'status': status, 'create_time': int(time.time())}
        return obj.insert(table='label', items=HandleData.jsonToDict(items))

    '''修改label  加上update_time'''
    def editLabel(self):
        json_data = HandleData.request_parse(request)
        obj = db_mysql_detail()
        table_property_arr = obj.get_column_name(tablename='label')
        for key in json_data:
            if key not in table_property_arr:
                del json_data[key]
        where_str = "id="+json_data['id']
        print(json_data)
        json_data['update_time'] = int(time.time())
        del json_data['delete_time']
        dict_request_data = HandleData.jsonToDict(json_data)
        return obj.update(table='label', where=where_str, items=dict_request_data)

    '''根据特定条件获取label标签信息'''
    def getLabelTopone(self,id=0,name='',status=0):
        obj = db_mysql_detail()
        # json_data = HandleData.request_parse(request)
        # where_str = "openid=" + json_data['openid']
        where_str = ''
        if name:
            where_str = "name=" + "'" + name + "' "
        if id:
            if where_str:
                where_str += " and id=" + str(id) + " "
            else:
                where_str = "id=" + str(id)
        if status:
            if where_str:
                where_str += " and status=" + str(status) + " "
            else:
                where_str = "status=" + str(status)
        # obj.selectTopone('',table='user',where=where_str)
        if not where_str:
            return None

        table_property_arr = obj.get_column_name(tablename='label')
        target_val = obj.selectTopone(table='label', where=where_str)
        # 根据列名生成 键值对
        target_data = {}
        for index, item in enumerate(target_val):
            for index2, item2 in enumerate(table_property_arr):
                if index == index2:
                    target_data[item2] = item
        return target_data
