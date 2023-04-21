import json
import os
from os.path import dirname, abspath
import shutil
from flask import Blueprint,request
import numpy as np
import torch
import cv2

from pycocotools import mask
from skimage import measure

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

    '''工具函数 处理boxes'''
    @staticmethod
    def handle_points(points=[]):
        target_points=[]
        target_label=[]
        for item in points:
            temp_arr=[]
            temp_arr.append(item[0])
            temp_arr.append(item[1])
            target_label.append(item[2])
            target_points.append(temp_arr)
        return target_points,target_label
    
    '''工具函数 预测时处理图片'''
    @staticmethod
    def prepare_image(image, transform, device):
        image = transform.apply_image(image)
        image = torch.as_tensor(image, device=device.device) 
        return image.permute(2, 0, 1).contiguous()
    
    '''以下两个函数用来解决sql插入引号冲突问题'''
    '''字符串编码'''
    @staticmethod
    def encode(s):
        return ' '.join([bin(ord(c)).replace('0b', '') for c in s])
    '''字符串解码'''
    @staticmethod
    def decode(s):
        return ''.join([chr(i) for i in [int(b, 2) for b in s.split(' ')]])
    

    '''获取mask的边界区域'''
    @staticmethod
    def get_segboundery(s):
        target_segboundery=np.where(s, 255, 0)
        img=cv2.Canny(np.uint8(target_segboundery),50,100)
        img[img < 255] = 0
        row_indices, col_indices = np.where(img == 255)
        return list(zip(row_indices, col_indices))
    @staticmethod
    def default_dump(obj):
        """Convert numpy classes to JSON serializable objects."""
        if isinstance(obj, (np.integer, np.floating, np.bool_)):
            return obj.item()
        elif isinstance(obj, np.ndarray):
            return obj.tolist()
        else:
            return obj

    '''
        生成coco格式的数据内容
        @param ground_truth_binary_mask np.array[true/false] eg.[255,258]  2-d
        @param image_id 
        @param category_id 
        @param segment_id 
    '''
    @staticmethod
    def get_coco_res(ground_truth_binary_mask,image_id=0,category_id=0,segment_id=0):
        temp_ground_truth_binary_mask = ground_truth_binary_mask.astype(int)
        # ground_truth_binary_mask = np.array([[  0,   0,   0,   0,   0,   0,   0,   0,   0,   0],
        #                                     [  0,   0,   0,   0,   0,   0,   0,   0,   0,   0],
        #                                     [  0,   0,   0,   0,   0,   1,   1,   1,   0,   0],
        #                                     [  0,   0,   0,   0,   0,   1,   1,   1,   0,   0],
        #                                     [  0,   0,   0,   0,   0,   1,   1,   1,   0,   0],
        #                                     [  0,   0,   0,   0,   0,   1,   1,   1,   0,   0],
        #                                     [  1,   0,   0,   0,   0,   0,   0,   0,   0,   0],
        #                                     [  0,   0,   0,   0,   0,   0,   0,   0,   0,   0],
        #                                     [  0,   0,   0,   0,   0,   0,   0,   0,   0,   0]], dtype=np.uint8)
        fortran_ground_truth_binary_mask = np.asfortranarray(temp_ground_truth_binary_mask)
        encoded_ground_truth = mask.encode(fortran_ground_truth_binary_mask.astype('uint8'))
        ground_truth_area = mask.area(encoded_ground_truth)
        ground_truth_bounding_box = mask.toBbox(encoded_ground_truth)
        contours = measure.find_contours(ground_truth_binary_mask, 0.5)
        annotation = {
                "segmentation": [],
                "area": ground_truth_area.tolist(),
                "iscrowd": 0,
                "image_id": image_id,
                "bbox": ground_truth_bounding_box.tolist(),
                "category_id": category_id,
                "id": segment_id,
                "size":[ground_truth_binary_mask.shape[0],ground_truth_binary_mask.shape[1]]
            }
        for contour in contours:
            contour = np.flip(contour, axis=1)
            segmentation = contour.ravel().tolist()
            annotation["segmentation"].append(segmentation)

        return annotation
    @staticmethod
    def jsonWrite(infoData,jsonFile):
        with open(jsonFile, 'w', encoding='utf-8') as jsonhandle:
            jsoncontent = json.dumps(infoData, indent=4)
            jsonhandle.write(jsoncontent)
