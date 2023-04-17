import json
import time
from flask import request

from flask import jsonify

from database.db_mysql import db_mysql_detail
from utils.HandleData import HandleData
from utils.MyResultRole import MyResultRole

'''
    处理model表   增删改查
'''


class MessageServer():
    '''根据特定条件获取message标签信息'''

    def getMessageOne(self, id=0):
        obj = db_mysql_detail()
        where_str = ''
        if id:
            where_str = " id=" + str(id)
        if not where_str:
            return None
        table_property_arr = obj.get_column_name(tablename='message')
        target_val = obj.selectTopone(table='message', where=where_str)
        #根据列名生成 键值对
        target_data = {}
        for index,item in enumerate(target_val):
            for index2,item2 in enumerate(table_property_arr):
                if index==index2:
                    target_data[item2] =item
        return target_data

    """
          分页查询
          :return:
        """

    def limit_offset_query(self, pageNo=1, page_size=20):
        # 数据总量
        obj = db_mysql_detail()
        where_str = " "
        total_count = obj.get_total_count(tablename='message', where_str=where_str)
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
        result_list = obj.get_tweet_by_page(startone, page_size, tablename='message', where_str=where_str)
        return {'data': result_list, 'page_data': page_data}

    '''文案编辑'''
    def editMessage(self):
        json_data = HandleData.request_parse(request)
        obj = db_mysql_detail()
        table_property_arr = obj.get_column_name(tablename='message')
        for key in json_data:
            if key not in table_property_arr:
                del json_data[key]
        where_str = "id="+json_data['id']
        json_data['update_time'] = int(time.time())
        del json_data['delete_time']
        dict_request_data = HandleData.jsonToDict(json_data)
        return obj.update(table='message',where=where_str, items=dict_request_data)
