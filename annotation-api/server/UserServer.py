import json
import time

import requests
from flask import request

from flask import jsonify

from database.db_mysql import db_mysql_detail
from utils.HandleData import HandleData
from utils.MyResultRole import MyResultRole

'''
    处理用户表   增删改查
'''
class UserServer():
    #管理员

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
    def limit_offset_query(self,pageNo=1, page_size=20,user_type=0,user_name=''):
        # 数据总量
        obj = db_mysql_detail()
        where_str=" "
        if user_type:
            where_str += " and "+"type=" + str(user_type)
        if user_name:
            where_str += " and "+"name like '%" + user_name+"%'"
        total_count = obj.get_total_count(tablename='user',where_str=where_str)
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
        result_list = obj.get_tweet_by_page(startone,page_size,tablename='user',where_str=where_str)
        return {'data' : result_list , 'page_data' : page_data}
        # print(result_list)

    '''删除用户   即为表加上delete_time'''
    def deleteUser(self,user_id):
        obj = db_mysql_detail()
        return obj.deleteItem(id=user_id,tablename='user')

    '''增加管理员  加上create_time'''
    def addAdmin(self, name, phone, admin_type=1):
        obj = db_mysql_detail()
        items={'name':name,'type':admin_type,'create_time':int(time.time()),'phone':phone}
        if not phone:
            del items['phone']
        return obj.insert(table='user',items=HandleData.jsonToDict(items))

    '''用户编辑'''
    def editUser(self):
        json_data = HandleData.request_parse(request)
        obj = db_mysql_detail()
        table_property_arr = obj.get_column_name(tablename='user')
        for key in json_data:
            if key not in table_property_arr:
                del json_data[key]
        where_str = "id="+json_data['id']
        json_data['update_time'] = int(time.time())
        del json_data['delete_time']
        dict_request_data = HandleData.jsonToDict(json_data)
        return obj.update(table='user',where=where_str, items=dict_request_data)

    #非管理员，普通用户
    # 获取openid
    def getOpenid(self, name=''):
        appid = "wx5f8644f648f067fc"
        secret = "a4e59c8dd5e2de7c9e4b0fe01962918f"
        parmas = {'appid': appid, 'secret': secret, 'js_code': request.get_json()["code"],
                  'grant_type': 'authorization_code'}
        url = 'https://api.weixin.qq.com/sns/jscode2session'
        r = requests.get(url, params=parmas)
        openid = r.json().get('openid', '')
        targetuser = self.getMiniUser(openid=openid)
        if not targetuser:
            self.addMiniUser(name=name,openid=openid)
        return  r.json()

    #增加新用户
    def addMiniUser(self, name='',admin_type=2,openid=""):
        obj = db_mysql_detail()
        items = {'name': name, 'type': admin_type,'openid': openid, 'create_time': int(time.time())}
        return obj.insert(table='user', items=HandleData.jsonToDict(items))

    #根据openid 特定条件查询id
    def getMiniUser(self,openid='',id=0):
        obj = db_mysql_detail()
        # json_data = HandleData.request_parse(request)
        # where_str = "openid=" + json_data['openid']
        where_str =''
        if openid:
            where_str = "openid=" + "'"+openid+"' "
        if id:
            if where_str:
                where_str+=" and id="+str(id)+" "
            else:
                where_str = "id="+str(id)
        # obj.selectTopone('',table='user',where=where_str)
        if not where_str:
            return None
        return obj.selectTopone(table='user',where=where_str)

    #根据用户名 密码验证是否登录成功
    def getUserOne(self,name="",pwd=""):
        if not name or not pwd:
            return False
        obj = db_mysql_detail()
        where_str = ''
        if name:
            where_str = " name='" + str(name)+"'"
        if pwd:
            where_str += " and pwd='" + str(pwd)+"'"
        if not where_str:
            return None
        table_property_arr = obj.get_column_name(tablename='user')
        target_val = obj.selectTopone(table='user', where=where_str)
        # 根据列名生成 键值对
        target_data = {}
        for index, item in enumerate(target_val):
            for index2, item2 in enumerate(table_property_arr):
                if index == index2:
                    target_data[item2] = item
        return target_data