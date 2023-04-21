import os
import sys
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.append(BASE_DIR)
# #接后续代码

from os.path import dirname, abspath
from database.db_mysql import db_mysql_detail
from server.SegmentServer import SegmentServer
from utils.HandleData import HandleData
from server.PublicServer import PublicServer
from utils.MyResultRole import MyResultRole
import pandas as pd

from config import sam_checkpoint,device,model_type
from segment_anything import sam_model_registry, SamPredictor
import cv2
import numpy as np
import torch

import json

from flask import current_app
from segment_anything.utils.transforms import ResizeLongestSide
import time
'''
    处理images表   增删改查
'''

class ImagesServer():
    """
      分页查询
      :return:
    """
    def limit_offset_query(self, pageNo=1, page_size=20,proj_id=0):
        # 数据总量
        obj = db_mysql_detail()
        where_str = " and proj_id="+str(proj_id)
        total_count = obj.get_total_count(tablename='images', where_str=where_str)
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
        result_list = obj.get_tweet_by_page(startone, page_size, tablename='images', where_str=where_str)
        return {'data': result_list, 'page_data': page_data}
    
    '''
        获取图片segment
        list:[
            {segmentation_id,segmentation:[],area:xx,bbox:[]},
        ]
    '''
    def get_img_segment(self,img_id=0,proj_id=0,interest_field=[]):
        obj = db_mysql_detail()
        where_str = " delete_time is null and id="+str(img_id)+" "
        image_val = obj.selectTopone(table='images', where=where_str)
        if not len(image_val):
            return []
        if len(interest_field):
            #清空页面的标注点
            # clear_arr = PublicServer.clear_img_segment(PublicServer(),img_id=img_id)
            obj.deleteItem_condition(where_condition=" img_id="+str(img_id)+" ", tablename='segment')
            box_point_arr=[]
            for itemm in interest_field:
                input_point,input_label=HandleData.handle_points(itemm['points'])
                box_point_arr.append({"input_box":itemm['boxes'],"input_point":input_point,"point_labels":input_label})

            image_url=os.path.join(BASE_DIR,image_val[0]['img_url'])
            if current_app.image_url!=image_url:
                current_app.image_url=image_url
                current_app.image = cv2.cvtColor(cv2.imread(os.path.join(BASE_DIR,image_val[0]['img_url'])), cv2.COLOR_BGR2RGB)
                current_app.predictor.set_image(current_app.image) #耗时体现在这里
            target_masks=[]   
            
            if len(box_point_arr):
                print("boxes+points predict")
                for itemmmmm in box_point_arr:
                    masks, _, _ = current_app.predictor.predict(
                        point_coords=np.array(itemmmmm['input_point']) if len(itemmmmm['input_point']) else None,
                        point_labels=np.array(itemmmmm['point_labels']) if len(itemmmmm['point_labels']) else None,
                        box=np.array(itemmmmm["input_box"])[None, :] if len(itemmmmm['input_box']) else None,
                        multimask_output=False,
                    )
                    for i in masks:
                        target_masks.append(i)
            # print(len(target_masks))
            # 开始处理 加入segment表
            for index_mask,item_mask in enumerate(target_masks):
                # print(type(item_mask))
                # print(item_mask)
                items = {
                    "img_id": img_id,
                    "proj_id": proj_id,
                    "label_id": "",
                    "create_time": int(time.time()),
                    # "seg_field":HandleData.encode(json.dumps(HandleData.get_segboundery(item_mask.tolist()),ensure_ascii=False, default=HandleData.default_dump)),#只保存二维坐标点
                    "seg_field":HandleData.encode(json.dumps(HandleData.get_coco_res(item_mask,image_id=img_id),ensure_ascii=False, default=HandleData.default_dump)),#存segment json///,category_id=0,segment_id=0 后期补上
                    "field_items":HandleData.encode(json.dumps(interest_field[index_mask]["item"]))
                }
                # project_id = obj.insert(table='project', items=HandleData.jsonToDict(items))
                obj.insert(table="segment", items=HandleData.jsonToDict(items))
            return SegmentServer.getAllSegmentList(SegmentServer(),img_id=img_id)
        return [] #segmentlist
    
    
# if __name__=="__main__":
    # obj = db_mysql_detail()
    # # items = {
    # #                 "img_id": 12,
    # #                 "proj_id": 21,
    # #                 "create_time": int(time.time()),
    # #                 "seg_field":HandleData.encode(json.dumps([1,2,3])),
    # #                 "field_items":HandleData.encode(json.dumps(["sasasd"]))
    # #             }
    # # print(obj.insert(table="segment", items=HandleData.jsonToDict(items)))
    # getAllSegmentList = SegmentServer.getAllSegmentList(SegmentServer())

    # for item in getAllSegmentList:
    #     # seg_field = json.loads()
    #     # print(type(item['seg_field']))
    #     # print(type(json.loads(item['field_items'])))
        
    #     # print(type(json.loads(item["seg_field"].replace("\'","\""))))
    #     # print(json.loads(item["field_items"].replace("\'","\"")))/
    #     print(len(item["seg_field"]))
    #     print(item["seg_field"])
    #     target_seg_field=[]
    #     for item in item["seg_field"]:
    #         target_seg_field.append({"x":item[0],"y":item[1]})
    #     print(target_seg_field)
        # nums_1d = [item for sublist in item["seg_field"] for item in sublist]
        # print(len(nums_1d))
        # print(json.loads(item["seg_field"].replace("\'","\"")))
        # print(type(item['field_items']))

        # target_segboundery=np.where(item["seg_field"], 255, 0)
        # img=cv2.Canny(np.uint8(target_segboundery),50,100)
        # img[img < 255] = 0
        # row_indices, col_indices = np.where(img == 255)
        # target_segboundery = list(zip(row_indices, col_indices))
        # print(len(target_segboundery))


