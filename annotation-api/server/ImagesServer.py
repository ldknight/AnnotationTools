from os.path import dirname, abspath
from database.db_mysql import db_mysql_detail
from server.LabelServer import LabelServer
from utils.HandleData import HandleData
from utils.HandleZip import HandleZip
from utils.MyResultRole import MyResultRole
import pandas as pd

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



