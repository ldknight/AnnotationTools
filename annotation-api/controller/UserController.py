import requests
import uuid

from aiohttp.web_response import json_response

from server.UserServer import UserServer
from flask import Blueprint,request
from utils.HandleData import HandleData
from utils.MyResultRole import MyResultRole

user_api = Blueprint('user_api', __name__)

#管理员用户
@user_api.route('/user/getUserList',methods=['POST','GET'])
#分页查询用户列表
def getUserList(pageNo=1,page_size=20,type=0,name=""):
    pageNo = HandleData.request_parse_equal(pageNo, locals())
    page_size = HandleData.request_parse_equal(page_size, locals())
    user_type = HandleData.request_parse_equal(type, locals())
    user_name = HandleData.request_parse_equal(name, locals())
    print(user_name)
    res = UserServer.limit_offset_query('',pageNo=pageNo, page_size=page_size,user_type=user_type,user_name=user_name)
    return MyResultRole.ResSuccess(data=res)


@user_api.route('/user/deleteUser',methods=['POST','GET'])
#分页查询用户列表
def deleteUser(user_id=1):
    user_id = HandleData.request_parse_equal(user_id, locals())
    res_flag = UserServer.deleteUser('',user_id)
    if res_flag:
        return MyResultRole.ResSuccess(msg='用户删除成功！')
    else:
        return MyResultRole.ResError(msg="用户删除失败")

@user_api.route('/user/addAdmin',methods=['POST','GET'])
#用户增加
def addAdmin(name='',phone=0):
    name = HandleData.request_parse_equal(name, locals())
    phone = HandleData.request_parse_equal(phone, locals())
    res_flag = UserServer.addAdmin('',name=name, phone=phone)
    if res_flag:
        return MyResultRole.ResSuccess('添加成功！')
    return MyResultRole.ResError('添加失败！')

@user_api.route('/user/editUser',methods=['POST','GET'])
#分页查询用户列表 id必传
def editUser(name=''):
    name = HandleData.request_parse_equal(name, locals())
    res_flag = UserServer.editUser('')
    if res_flag:
        return MyResultRole.ResSuccess(msg="'"+name+"' 信息修改成功！")
    return MyResultRole.ResError(msg="'"+name+"'信息修改失败！")

@user_api.route('/user/getUserOne',methods=['POST','GET'])
#获取单个用户信息
def getUserOne(username="",password=""):
    username = HandleData.request_parse_equal(username, locals())
    password = HandleData.request_parse_equal(password, locals())
    # password = HandleData.request_parse_equal(password, locals())
    res = UserServer.getUserOne(UserServer(), name=username,pwd=password)
    if res:
        return MyResultRole.ResSuccess()
    else:
        return MyResultRole.ResError()

@user_api.route('/user/updateAdminpwd',methods=['POST','GET'])
#管理员密码重置
def updateAdminpwd():
    res_flag = UserServer.editUser(UserServer())
    if res_flag:
        return MyResultRole.ResSuccess(msg="密码重置成功！")
    return MyResultRole.ResError(msg="密码重置失败！")



#普通用户
@user_api.route('/user/getOpenid',methods=['POST','GET'])
#获取用户的openid  并将未存储的用户放入user表
def getOpenid(name=''):
    name = HandleData.request_parse_equal(name, locals())
    openid_json = UserServer.getOpenid(UserServer())
    return MyResultRole.ResSuccess(data=openid_json)















@user_api.route('/user/testone',methods=['POST','GET'])
#测试
def testone():
    json_data = {
        'name': 1,
        'path': "sasdas"
    }
    target_str = " where "
    for key,val in HandleData.jsonToDict(json_data):
        #判断参数类型  并转型
        if isinstance(val, str):
            val="'"+val+"'"
        target_str+= "'"+str(key)+"'="+str(val)+","
    return MyResultRole.ResSuccess(data=target_str)

#修改用户信息
# def updateUser():
#     #直接修改












#草稿
# HandleData.request_parse(request)   #该函数用于获取GET或POST传来的参数
    # 'user' in HandleData.request_parse(request)    判断某个参数是否在里面
    # temp_json = HandleData.jsonToDict(HandleData.request_parse(request))
    # print(HandleData.request_parse_exist('pageNo'))
    # for key,value in HandleData.jsonToDict(HandleData.request_parse(request)):
    #     print(key,value)
    # print(res)  数组
    # res.append(HandleData.request_parse(request))