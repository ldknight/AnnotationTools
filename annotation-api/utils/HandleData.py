import json
import os
from os.path import dirname, abspath
import shutil
from flask import Blueprint,request
class HandleData:
    '''
    将json对象转成dict  便返回，方便遍历 for index,item in jsondata
    '''
    @staticmethod
    def jsonToDict(data={},sort_keys=False):
        # data = {
        #     'mame': 1,
        #     'pwd': 123
        # }
        json_str = json.dumps(data, sort_keys=sort_keys)
        params_json = json.loads(json_str)
        items = params_json.items()
        return items
        # for key, value in items:
        #     print(str(key) + '=' + str(value))

    '''解析请求数据并以json形式返回'''
    @staticmethod
    def request_parse(req_data):
        if req_data.method == 'POST':
            data = req_data.form.to_dict()
            if not bool(data):
                data=req_data.get_json()
        elif req_data.method == 'GET':
            data = req_data.args
        return data

    '''判断某个参数 是否在传输参数列表中'''
    @staticmethod
    def request_parse_exist(param_name):
        return param_name in HandleData.request_parse(request)

    '''获取实参名称'''
    @staticmethod
    def get_variable_name(variable, locals):
        loc = locals
        for key in loc:
            if loc[key] == variable:
                return key

    '''用传输参数列表中参数  为参数赋值'''
    @staticmethod
    def request_parse_equal(param_name,locals):
        param_name_str = HandleData.get_variable_name(param_name,locals)
        json_data = HandleData.request_parse(request)
        if HandleData.request_parse_exist(param_name_str):
            return HandleData.tansform_type(param_name,json_data[param_name_str])
        else:
            return param_name

    '''参数类型转换'''
    @staticmethod
    def tansform_type(variate,param_data):
        if isinstance(variate, int):
            if not param_data:
                return 0
            return int(param_data)
        elif isinstance(variate, str):
            return str(param_data)
        elif isinstance(variate, float):
            return float(param_data)
        elif isinstance(variate, list):
            return list(param_data)
        elif isinstance(variate, tuple):
            return tuple(param_data)
        elif isinstance(variate, dict):
            return dict(param_data)
        elif isinstance(variate, set):
            return set(param_data)

    '''传入json  转成sql的拼接字符串'''
    @staticmethod
    def jsonToSqlwhere(json_data={}):
        target_str = ""
        for key, val in HandleData.jsonToDict(json_data):
            # 判断参数类型  并转型
            if isinstance(val, str):
                val = "'" + val + "'"
            target_str += " and '" + str(key) + "'=" + str(val)
        return target_str

    '''为string   添加转义字符'''
    @staticmethod
    def strToFormtype(temp_str):
        if temp_str and isinstance(temp_str, str):
            temp_str=temp_str.replace("'", "\\'")
            temp_str=temp_str.replace('"', '\\"')
        return temp_str


    '''获取model模型的文件目录地址'''
    @staticmethod
    def getModelContents():
        Base_rootfile = dirname(dirname(abspath(__file__)))
        data_path = os.path.abspath(Base_rootfile + '\\myModel\\uploadModels')
        data_path = data_path.replace('\\', '/')
        return data_path

    '''获取sound模型的文件目录地址'''
    @staticmethod
    def getSoundsContents():
        Base_rootfile = dirname(dirname(abspath(__file__)))
        data_path = os.path.abspath(Base_rootfile + '\\static\\uploadResourcesSound')
        data_path = data_path.replace('\\', '/')
        return data_path
    #获取静态目录  线上地址
    @staticmethod
    def getStaticOnline():
        request_url = request.url
        request_url_arr = request_url.split(request.path)
        return request_url_arr[0]+'/static'
    #获取静态文件  线下地址
    @staticmethod
    def getStaticLocal():
        Base_rootfile = dirname(dirname(abspath(__file__)))
        data_path = os.path.abspath(Base_rootfile + '\\static')
        data_path = data_path.replace('\\', '/')
        return data_path

    #将文件复制到指定文件夹
    @staticmethod
    def copyfileTodict(srcfile,dstpath,fname):                       # 复制函数
        if not os.path.isfile(srcfile):
            print ("%s not isfile!"%(srcfile))
            return False
        else:
            if not os.path.exists(dstpath):
                os.makedirs(dstpath)                       # 创建路径
            if HandleData.judgeIncludeAnyjpg(fname):
                shutil.copy(srcfile, os.path.join(dstpath,fname))          # 复制文件
                print ("copy %s -> %s"%(srcfile, dstpath + fname))
                return True
            else:
                return False
    @staticmethod
    def judgeIncludeAnyjpg(fname):
        if ".jpg" in fname or ".jpeg" in fname or ".png" in fname or ".gif" in fname:
            return True
        else:
            return False


