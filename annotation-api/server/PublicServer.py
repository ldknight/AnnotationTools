import os
import sys
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.append(BASE_DIR)
# #接后续代码

from database.db_mysql import db_mysql_detail
import os
import json

from server.SegmentServer import SegmentServer
from utils.HandleData import HandleData

"""
    处理
"""


class PublicServer:
    '''清除画布信息 返回处理的行数'''
    def clear_img_segment(self,img_id=0):
        #删除图片对应的segment
        obj = db_mysql_detail()
        obj.deleteItem_condition(where_condition=" img_id="+str(img_id)+" ", tablename='segment')
        return SegmentServer.getAllSegmentList(SegmentServer(),img_id=img_id)
    
    '''获取所有的标注信息 返回数组'''
    def download_annotationtxt(self,proj_id):
        obj = db_mysql_detail()
        where_str = " delete_time is null "
        if proj_id:
            where_str = " delete_time is null and proj_id="+str(proj_id)+" and label_id!="+str("''")+" "
        target_val = obj.selectAll(table='segment', where=where_str,order=" create_time desc")
        annotation=[]
        for item in target_val:
            item["field_items"]=HandleData.decode(item["field_items"])
            item["field_items"]=json.loads(item["field_items"].replace("\'","\""))

            item["seg_field"]=HandleData.decode(item["seg_field"])
            item["seg_field"]=json.loads(item["seg_field"].replace("\'","\""))

            item["seg_field"]["category_id"]=item['label_id']
            item["seg_field"]["id"]=item['id']

            annotation.append(item["seg_field"])
        print(BASE_DIR)    
        HandleData.jsonWrite(annotation,os.path.join(BASE_DIR,"static/annotation.txt"))
        return HandleData.getStaticOnline()+"/annotation.txt"
    

if __name__=="__main__":
    print(len(PublicServer.download_annotationtxt(PublicServer,proj_id=21)))