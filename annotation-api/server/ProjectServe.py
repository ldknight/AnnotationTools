import os
import sys
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.append(BASE_DIR)
# #接后续代码

import json
import time
from flask import request
from flask import jsonify
from database.db_mysql import db_mysql_detail
from utils.HandleData import HandleData
from utils.MyResultRole import MyResultRole
import os
from glob import glob

from server.ImagesServer import ImagesServer
from server.LabelServer import LabelServer
from server.SegmentServer import SegmentServer

"""
    处理project表   增删改查
"""


class ProjectServer:

    def addProject(self, proj_url):
        # 数据库查询 不能已存在
        obj = db_mysql_detail()
        where_str = ""
        if proj_url:
            where_str = " proj_url_ago='" + str(proj_url) + "'"
        if not where_str:
            return {"proj_id": 0}
        target_val = obj.selectTopone(table="project", where=where_str)
        if target_val:
            # 项目已经存在
            return {"proj_id": 0}
        # 判断proj_url是文件夹并且 存在
        # 将内容拷贝到指定位置 并重命名
        # 删除其中不是图片的文件
        # 数据库添加项目
        # 遍历拷贝之后的图片目录名称 添加到image 表
        # 分页查询image数据表中对应proj_id 的数据，并返回
        if os.path.isdir(proj_url) and os.path.exists(proj_url):
            image_path = os.path.join("static", str(int(time.time())))
            # project 插入数据库 增加project  加上create_time
            items = {
                "proj_url": image_path,
                "proj_url_ago": proj_url,
                "create_time": int(time.time()),
            }
            # project_id = obj.insert(table='project', items=HandleData.jsonToDict(items))
            proj_id = obj.insert(table="project", items=HandleData.jsonToDict(items))
            print(proj_id)
            if not proj_id:
                return {"proj_id": 0}
            for srcfile in glob(proj_url + "/*"):  # glob获得路径下所有文件，可根据需要修改
                _, fname = os.path.split(srcfile)  # 分离文件名和路径
                if HandleData.copyfileTodict(
                    srcfile=srcfile,
                    dstpath=os.path.join(BASE_DIR, "static", str(int(time.time()))),
                    fname=fname,
                ):
                    # 将图片地址添加到数据库
                    img_info = {
                        "img_url": os.path.join(image_path, fname),
                        "proj_id": proj_id,
                    }
                    image_id = obj.insert(
                        table="images", items=HandleData.jsonToDict(img_info)
                    )
                    if not image_id:
                        print(img_info["img_url"] + "图片添加失败！")
            # 分页返回images列表
            imagelist = ImagesServer.limit_offset_query(
                ImagesServer(), pageNo=1, page_size=50, proj_id=proj_id
            )
            return {"imagelist": imagelist, "proj_id": proj_id}

    def getProjectList(self):
        # 数据总量
        obj = db_mysql_detail()
        where_str = " delete_time is null "
        target_val = obj.selectAll(table='project', where=where_str,order=" create_time desc")
        imagelist=[]
        label_list=[]
        segment_list=[]
        if(target_val and len(target_val)):
            # 分页返回images列表
            imagelist = ImagesServer.limit_offset_query(
                ImagesServer(), pageNo=1, page_size=50, proj_id=target_val[0]['id']
            )
            #获取label列表
            label_list = LabelServer.getAllLabelList(
                LabelServer(),proj_id=target_val[0]['id']
            )
            #获取segment列表
            if(len(imagelist["data"])):
                segment_list = SegmentServer.getAllSegmentList(
                    SegmentServer(),img_id=imagelist["data"][0]['id']
                )
        return {"imagelist": imagelist, "project_list": target_val,"label_list":label_list,"segment_list":segment_list}

    def del_proj(self, proj_id):
        # 删除与项目相关的 图片
        # 删除与项目相关的 label
        # 删除与项目相关的 segment
        # 删除项目
        print(1)


if __name__ == "__main__":
    # proj_url="/Users/liudun/Desktop/anno_tools/AnnotationTools/demo_imgs"
    res=ProjectServer.getProjectList(
        ProjectServer()
    )
    print(res)
