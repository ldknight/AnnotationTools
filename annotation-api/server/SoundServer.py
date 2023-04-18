import json
import os
import time
from os.path import dirname, abspath

from flask import request

from flask import jsonify
from werkzeug.utils import secure_filename

from database.db_mysql import db_mysql_detail
from myModel.PredictWav import PredictWav
from myModel.JudgeBabysound import JudgeBabysound
from myModel.PredictWavCNN import PredictWavCNN
from server.LabelServer import LabelServer
from server.UserServer import UserServer
from utils.HandleData import HandleData
from utils.HandleZip import HandleZip
from utils.MyResultRole import MyResultRole
import pandas as pd

'''
    处理sound表   增删改查
'''


class SoundServer():
    '''增加音频资源   本地+数据库  加上create_time'''

    def addSound(self):
        # 本地上传
        # Base_rootfile = dirname(dirname(abspath(__file__)))
        # data_path = os.path.abspath(Base_rootfile + '\\uploadResourcesFile')
        # if not os.path.exists(data_path): os.mkdir(data_path)  # 如果不存在这个excelReport文件夹，就自动创建一个
        # data_path = data_path.replace('\\', '/')
        data_path = HandleData.getSoundsContents()
        f = request.files['file']
        f.save(os.path.join(data_path, secure_filename(f.filename)))
        temp_filename = str(data_path) + "/" + str(secure_filename(f.filename))
        target_filename = str(data_path) + "/x" + str(secure_filename(f.filename))
        resdata = HandleData.transformWavToNewWav(temp_filename, target_filename)
        if os.path.exists(target_filename) and os.path.exists(temp_filename):
            os.remove(temp_filename)
        # print(resdata)
        # 处理音频的识别率  使用深度学习
        # DNN
        # predictwav = PredictWav()
        # dnn_res = predictwav.getPredictRes(filename=target_filename)
        # CNN
        judgebabysound = JudgeBabysound()
        JudgeBabysound_bool = judgebabysound.print_prediction_sta(filename=target_filename)
        if not JudgeBabysound_bool:
            os.remove(target_filename)
            return -6
        predictwavcnn = PredictWavCNN()
        dnn_res = predictwavcnn.gotoPredict_CNN(filename=target_filename)
        # print(dnn_res)
        # print(str(data_path)+"/"+str(secure_filename(f.filename)))
        # dnn_res = predictwav.getPredictRes(filename=filename)
        if not dnn_res:
            return -3
        # 向数据库添加 音频数据
        # 获取userid
        openid = ''
        openid = HandleData.request_parse_equal(openid, locals())
        if openid == '':
            return -1
        user_res = UserServer.getMiniUser(UserServer(), openid=openid)
        if not user_res:
            return -2
        obj = db_mysql_detail()
        # label_system_id=dnn_res.get('label_index')
        recognition_rate = dnn_res.get('acc')
        # 根据label_id  获取label_name
        # label_details = LabelServer.getLabelTopone(LabelServer(),id=int(dnn_res.get('label_index'))+1)
        obj = db_mysql_detail()
        label_details = obj.getmodellabel(offset_No=int(dnn_res.get('label_index')))
        print(label_details)
        if not label_details:
            return -5
        items = {
            # 'filepath': data_path,
            'filename': 'x' + secure_filename(f.filename),
            'create_time': int(time.time()),
            'user_id': user_res[0],
            'label_system_id': int(label_details[0]['id']),
            'recognition_rate': str(recognition_rate)
        }
        # 返回自增的id
        insert_sourceflag = obj.insert(table='sound', items=HandleData.jsonToDict(items))
        if not insert_sourceflag:
            return -4
        return {"label_name": str(label_details[0]['name']), "recognition_rate": str(recognition_rate)}

    """
      分页查询
      :return:
    """

    def limit_offset_query(self, pageNo=1, page_size=20, openid=''):
        # 数据总量
        obj = db_mysql_detail()
        where_str = " "
        if openid:
            user_res = UserServer.getMiniUser(UserServer(), openid=openid)
            if user_res:
                where_str += " and " + "user_id=" + str(user_res[0])
            else:
                return -1
        # if user_name:
        #     where_str += " and " + "name like '%" + user_name + "%'"
        total_count = obj.get_total_count(tablename='sound', where_str=where_str)
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
        result_list = obj.get_tweet_by_page(startone, page_size, tablename='sound', where_str=where_str)
        for item in result_list:
            item['filepath']=HandleData.getStaticOnline()+'/uploadResourcesSound'
            if item['user_id']:
                user_data = UserServer.getMiniUser(UserServer(), id=item['user_id'])
                print(user_data)
                if user_data:
                    item['user_name'] = user_data[1]
            # 通过id获取标签信息  人为标注的标签artificial_label
            if item['artificial_label_id']:
                label_data = LabelServer.getLabelTopone(LabelServer(), id=item['artificial_label_id'])
                if label_data:
                    item['artificial_label'] = label_data['name']
            # 通过id获取标签信息  系统自动识别的标签
            if item['label_system_id']:
                label_data = LabelServer.getLabelTopone(LabelServer(), id=item['label_system_id'])
                if label_data:
                    item['label_name'] = label_data['name']
        return {'data': result_list, 'page_data': page_data}
        # print(result_list)

    '''删除音频   即为表加上delete_time'''

    def deleteSound(self, sound_id):
        if not sound_id:
            return 0
        obj = db_mysql_detail()
        return obj.deleteItem(id=sound_id, tablename='sound')

    '''音频编辑'''

    def editSound(self):
        json_data = HandleData.request_parse(request)
        obj = db_mysql_detail()
        table_property_arr = obj.get_column_name(tablename='sound')
        for key in list(json_data):
            if key not in table_property_arr:
                del json_data[key]
        where_str = "id=" + str(json_data['id'])
        json_data['update_time'] = int(time.time())
        del json_data['delete_time']
        del json_data['create_time']
        dict_request_data = HandleData.jsonToDict(json_data)
        return obj.update(table='sound', where=where_str, items=dict_request_data)

    '''根据特定条件获取Sound信息'''

    def getSoundTopone(self, artificial_label_id=0, id=0):
        if not artificial_label_id and not id:
            return False
        obj = db_mysql_detail()
        where_str = ''
        if artificial_label_id:
            where_str = " artificial_label_id='" + str(artificial_label_id) + "'"
        if id:
            if where_str:
                where_str += " and id='" + str(id) + "'"
            else:
                where_str += " id='" + str(id) + "'"
        if not where_str:
            return None
        table_property_arr = obj.get_column_name(tablename='sound')
        target_val = obj.selectTopone(table='sound', where=where_str)
        # 根据列名生成 键值对
        target_data = {}
        for index, item in enumerate(target_val):
            for index2, item2 in enumerate(table_property_arr):
                if index == index2:
                    target_data[item2] = item
        return target_data

    '''音频文件下载'''

    def downloadSound(self):
        # 根据传过来的标签id 查找 sound 表
        random_time = str(int(round(time.time() * 100000)))
        zipfilename = '/' + random_time + '.zip'
        handlezip = HandleZip(HandleData.getStaticLocal() + zipfilename)

        csv_path = HandleData.getStaticLocal() + "/" + random_time + ".csv"

        json_data = HandleData.request_parse(request)
        temp_filename_arr = []
        system_label_id_arr = []
        system_recognition_rate_arr = []
        temp_filename_class = []
        if json_data and json_data['artificial_labels']:
            for item in json.loads(json_data['artificial_labels']):
                if not item:
                    continue
                sound_items = SoundServer.queryAllSound(SoundServer(), artificial_label_id=item)
                if sound_items:
                    for itemx in sound_items:
                        # handlezip.zipdir(path=itemx['filepath'] + '/' + itemx['filename'])
                        handlezip.zipdir(path=HandleData.getSoundsContents() + '/' + itemx['filename'])
                        temp_filename_arr.append(itemx['filename'])
                        system_label_id_arr.append(itemx['label_system_id'])
                        system_recognition_rate_arr.append(itemx['recognition_rate'])
                        temp_filename_class.append(item)
        dataframe = pd.DataFrame({'filename': temp_filename_arr,'label_system_id': system_label_id_arr,'recognition_rate': system_recognition_rate_arr,'artificial_label_id': temp_filename_class})

        dataframe.to_csv(csv_path, index=False, sep=',')
        if os.path.exists(csv_path):
            handlezip.zipdir(path=csv_path)

        if os.path.exists(HandleData.getStaticLocal() + zipfilename):
            return HandleData.getStaticOnline() + zipfilename
        return False


        """
          数据批量查询
        """
    def queryAllSound(self, artificial_label_id=0):
        if not artificial_label_id:
            return False
        # 数据总量
        obj = db_mysql_detail()
        where_str = " artificial_label_id=" + str(artificial_label_id) + " "
        target_val = obj.selectAll(table='sound', where=where_str)
        return target_val


if __name__ == "__main__":
    #测试区
    res = SoundServer.queryAllSound(SoundServer(), artificial_label_id=1)
    print(res)
