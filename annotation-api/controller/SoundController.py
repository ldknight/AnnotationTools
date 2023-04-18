import json
import os
from datetime import time
from os.path import dirname, abspath
from random import random

import requests
import uuid

from werkzeug.utils import secure_filename


from server.SoundServer import SoundServer
from server.UserServer import UserServer
from flask import Blueprint, request
from utils.HandleData import HandleData
from utils.MyResultRole import MyResultRole

sound_api = Blueprint('sound_api', __name__)


@sound_api.route('/sound/getSoundList', methods=['POST', 'GET'])
# 分页查询sound列表
def getSoundList(pageNo=1, page_size=20, openid=''):
    pageNo = HandleData.request_parse_equal(pageNo, locals())
    page_size = HandleData.request_parse_equal(page_size, locals())
    openid = HandleData.request_parse_equal(openid, locals())
    res = SoundServer.limit_offset_query(SoundServer(), pageNo=pageNo, page_size=page_size, openid=openid)
    if res == -1:  # 根据openid没有获取到user_id
        return MyResultRole.ResError(msg='用户信息获取错误！')
    return MyResultRole.ResSuccess(data=res)

@sound_api.route('/sound/uploadSound', methods=['POST', 'GET'])
# 上传音频
def uploadSound():
    resflag = SoundServer.addSound(SoundServer())
    if resflag == -1:
        return MyResultRole.ResError(msg='openid参数获取失败')
    elif resflag==-2:
        return MyResultRole.ResError(msg="用户信息获取失败")
    elif resflag==-3:
        return MyResultRole.ResError(msg="识别错误")
    elif resflag == -4:
        return MyResultRole.ResError(msg="数据添加失败")
    elif resflag == -5:
        return MyResultRole.ResError(msg="标签获取失败")
    elif resflag == -6:
        return MyResultRole.ResError(msg="没有检测到有效音频！")
    else:
        temp_data = {}
        for k, v in resflag.items():
            temp_data[k]=str(v)
        return MyResultRole.ResSuccess(data=temp_data)

@sound_api.route('/sound/deleteSound', methods=['POST', 'GET'])
# 删除sound   即为表加上delete_time
def deleteSound(id=0):
    sound_id = HandleData.request_parse_equal(id, locals())
    res_flag = SoundServer.deleteSound(SoundServer(), sound_id)
    if res_flag:
        return MyResultRole.ResSuccess(msg='录音删除成功！')
    else:
        return MyResultRole.ResError(msg="录音删除失败")
@sound_api.route('/sound/editSound',methods=['POST','GET'])
#修改音频 id必传
def editSound():
    res_flag = SoundServer.editSound(SoundServer())
    if res_flag:
        return MyResultRole.ResSuccess(msg="标注成功！")
    return MyResultRole.ResError(msg="标注失败！")

@sound_api.route('/sound/downloadSound',methods=['POST','GET'])
#音频下载   输入：音频的人为标注label  id   eg. artificial_labels=[1,2]
def downloadSound():
    res_flag = SoundServer.downloadSound(SoundServer())
    if res_flag:
        return MyResultRole.ResSuccess(msg="下载文件生成成功！",data=res_flag)
    return MyResultRole.ResError(msg="下载失败！")

# '''微信小程序  前台'''
# @sound_api.route('/sound/deleteSoundwx', methods=['POST', 'GET'])
# # 删除sound   即为表加上delete_time
# def deleteSoundwx(id=0):
#     sound_id = HandleData.request_parse_equal(id, locals())
#     res_flag = SoundServer.deleteSound(SoundServer(), sound_id)
#     if res_flag:
#         return MyResultRole.ResSuccess(msg='录音删除成功！')
#     else:
#         return MyResultRole.ResError(msg="录音删除失败")