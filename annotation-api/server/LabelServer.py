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
    '''get all labels'''
    def getAllLabelList(self,proj_id=0):
        obj = db_mysql_detail()
        where_str = " delete_time is null and proj_id="+str(proj_id)+" "
        target_val = obj.selectAll(table='label', where=where_str,order=" create_time desc")
        return target_val
