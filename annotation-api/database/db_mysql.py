import os
import sys
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.append(BASE_DIR)
#接后续代码

import time
from utils.HandleData import HandleData
import sqlite3

class db_mysql_detail():
    def __init__(self, name='test.db'):
        self.__name = name
        self.__conn = self.build_conn(name)
        self.__cursor = self.__conn.cursor()

    @property
    def conn(self):
        return self.__conn
    def build_conn(self, name):
        try:
            con = sqlite3.connect(name)
            return con
        except:
            print('Something wrong: not connect!')
    '''
        # 删除并 返回影响行数
        table         表名
        where         条件   name='小明',phone=110
    '''
    @property
    def delete(self, **kwargs):
        table = kwargs['table']
        where = kwargs['where']
        sql = 'DELETE FROM %s where %s' % (table, where)
        print(sql)
        try:
            # 执行SQL语句
            self.__cursor.execute(sql)
            # 提交到数据库执行
            self.__conn.commit()
            # 影响的行数
            rowcount = self.__cursor.rowcount
        except:
            # 发生错误时回滚
            self.__conn.rollback()
        return rowcount

    '''
        # 新增并 返回新增ID
        table   表名（必传
        items   数据（json  键值对）  eg.  {name:'小明',phone:13271390735}
    '''

    def insert(self, **kwargs):
        # print(kwargs)
        table = kwargs['table']
        del kwargs['table']
        sql = 'insert into %s(' % table
        fields = ""
        values = ""
        for k, v in kwargs['items']:
            fields += "%s," % k
            values += "'%s'," % v
        fields = fields.rstrip(',')
        values = values.rstrip(',')
        sql = sql + fields + ") values(" + values + ")"
        print(sql)
        res=0
        try:
            # 执行SQL语句
            self.__cursor.execute(sql)
            # 提交到数据库执行
            self.__conn.commit()
            # 获取自增id
            res = self.__cursor.lastrowid
            # res = self.__cursor.fetchone()
        except:
            # 发生错误时回滚
            self.__conn.rollback()
        return res

    '''
        # 修改数据并返回影响的行数
        table   表名（必传
        items   数据（json  键值对）  eg.  {name:'小明',phone:13271390735}
        where   条件   name='小明',phone=110
    '''

    def update(self, **kwargs):
        table = kwargs['table']
        # del kwargs['table']
        # kwargs.pop('table')
        where = kwargs['where']
        # kwargs.pop('where')
        sql = 'update %s set ' % table
        for k, v in kwargs['items']:
            #处理包含引号的字符串HandleData.strToFormtype
            sql += "%s='%s'," % (k, HandleData.strToFormtype(v))
        sql = sql.rstrip(',')
        sql += ' where %s ' % where
        print(sql)
        rowcount=0
        try:
            # 执行SQL语句
            self.__cursor.execute(sql)
            # 提交到数据库执行
            self.__conn.commit()
            # 影响的行数
            rowcount = self.__cursor.rowcount
        except:
            # 发生错误时回滚
            self.__conn.rollback()
        return rowcount

    '''
        # 查-一条条数据
        table   表名（必传
        field   域(数组)   eg.  [name,phone]
        where   条件       eg.  name='小明',phone=110
        order   排序条件         id
    '''

    def selectTopone(self, **kwargs):
        table = kwargs['table']
        field = 'field' in kwargs and kwargs['field'] or '*'
        where = 'where' in kwargs and 'where ' + kwargs['where'] or ''
        order = 'order' in kwargs and 'order by ' + kwargs['order'] or ''
        sql = 'select %s from %s %s %s limit 1' % (field, table, where, order)
        print(sql)
        temp_arr=[]
        try:
            # 执行SQL语句
            self.__cursor.execute(sql)
            # 使用 fetchone() 方法获取单条数据.
            data = self.__cursor.fetchone()
            tablename_arr = self.get_column_name(table)
            if tablename_arr:
                temp_json = {}
                for index3, item3 in enumerate(data):
                    temp_json[tablename_arr[index3]] = item3
                temp_arr.append(temp_json)
        except:
            # 发生错误时回滚
            self.__conn.rollback()
        return temp_arr

    '''
        # 查所有数据
        table   表名（必传
        field   域(数组)   eg.  [name,phone]   或者不传
        where   条件       eg.  name='小明',phone=110
        order   排序条件    eg.   id
    '''

    def selectAll(self, **kwargs):
        table = kwargs['table']
        field = 'field' in kwargs and kwargs['field'] or '*'
        where = 'where' in kwargs and 'where ' + kwargs['where'] or ''
        order = 'order' in kwargs and 'order by ' + kwargs['order'] or ''
        sql = 'select %s from %s %s %s ' % (field, table, where, order)
        print(sql)
        temp_arr = []
        try:
            # 执行SQL语句
            self.__cursor.execute(sql)
            # 使用 fetchone() 方法获取单条数据.
            rst = self.__cursor.fetchall()
            tablename_arr = self.get_column_name(table)
            if rst and len(rst):
                for index2, item2 in enumerate(rst):
                    temp_json = {}
                    for index3, item3 in enumerate(item2):
                        temp_json[tablename_arr[index3]] = item3
                    temp_arr.append(temp_json)
        except:
            # 发生错误时回滚
            self.__conn.rollback()
        return temp_arr

    '''
        表中数据的总量
    '''
    # def totalItem(self, **kwargs):
    #     table = kwargs['table']
    #     where = 'where' in kwargs and 'where ' + kwargs['where'] or ''
    #     sql = 'select count(*) from %s %s' % (table, where)
    #     try:
    #         # 执行SQL语句
    #         self.__cursor.execute(sql)
    #         # 使用 fetchone() 方法获取单条数据.
    #         data = self.__cursor.fetchall()
    #     except:
    #         # 发生错误时回滚
    #         self.__conn.rollback()
    #     return data

    """
       分页查询
       :param tablename 表名
       :param start:
       :param pagesize:
       :return:
    """

    def get_tweet_by_page(self, start, pagesize, tablename, where_str=""):
        sql = "select * from " + tablename + " where delete_time is null "+ where_str + " ORDER BY id DESC limit "+str(pagesize)+" offset "+str(start)
        self.__cursor.execute(sql)
        rst = self.__cursor.fetchall()
        tablename_arr = self.get_column_name(tablename)
        temp_arr = []
        if rst and len(rst):
            for index2, item2 in enumerate(rst):
                temp_json = {}
                for index3, item3 in enumerate(item2):
                    temp_json[tablename_arr[index3]] = item3
                temp_arr.append(temp_json)
        return temp_arr

    """
        获取总数量
        :return:
    """

    def get_total_count(self, tablename, where_str=''):
        sql = "select count(*) from " + tablename + " where delete_time is null "+where_str
        print(sql)
        self.__cursor.execute(sql)
        rst = self.__cursor.fetchone()
        if rst is None:
            return 0
        return rst[0]

    '''
        返回所有列名
        eg.    ['id', 'name', 'type', 'phone', 'create_time', 'update_time', 'delete_time']
    '''
    def get_column_name(self, tablename='user'):
        sql = "select * from " + tablename +" limit 1"
        # 执行SQL语句
        cursor = self.__cursor.execute(sql)
        target_arr = list(map(lambda x: x[0], cursor.description))
        return target_arr

    '''
        以下为未封装的sql，调用特定函数，传入完整sql即可
    '''

    def getAll_sql(self, sql):
        self.__cursor.execute(sql)
        return self.__cursor.fetchall()

    def insert_sql(self, sql):
        result = self.__cursor.execute(sql)
        self.__conn.commit()
        return result

    def update_sql(self, sql):
        result = self.__cursor.execute(sql)
        self.__conn.commit()
        return result

    def delete_sql(self, sql):
        # 执行SQL语句
        self.__cursor.execute(sql)
        # 提交到数据库执行
        self.__conn.commit()
        # 影响的行数
        return self.__cursor.rowcount

    #删除某条数据
    def deleteItem(self, id, tablename):
        sql = 'update %s set ' % tablename
        sql += 'delete_time=' + str(int(time.time()))
        sql += ' where id=%s ' % id
        print(sql)
        try:
            # 执行SQL语句
            self.__cursor.execute(sql)
            # 提交到数据库执行
            self.__conn.commit()
            # 影响的行数
            rowcount = self.__cursor.rowcount
        except:
            # 发生错误时回滚
            self.__conn.rollback()
        return rowcount
    
    #删除某条数据 在某个条件下 返回处理了多少行
    def deleteItem_condition(self, where_condition, tablename):
        sql = 'update %s set ' % tablename
        sql += 'delete_time=' + str(int(time.time()))
        sql += ' where %s ' % where_condition
        print(sql)
        rowcount=0
        try:
            # 执行SQL语句
            self.__cursor.execute(sql)
            # 提交到数据库执行
            self.__conn.commit()
            # 影响的行数
            rowcount = self.__cursor.rowcount
        except:
            # 发生错误时回滚
            self.__conn.rollback()
        return rowcount

    '''获取当前模型的对应标签 '''
    def getmodellabel(self,offset_No=1):
        sql = "select * from project"
        # sql = "select label.* from label inner join label_model_relation on (label_model_relation.label_id=label.id)  inner join model on (model.id=label_model_relation.model_id and model.status=1) limit 1 offset "+str(offset_No)
        label_name_arr = self.get_column_name(tablename='project')
        # print(label_name_arr)
        temp_arr = []
        try:
            # 执行SQL语句
            self.__cursor.execute(sql)
            # 使用 fetchone() 方法获取单条数据.
            data = self.__cursor.fetchall()
            for item1 in data:
                temp_json = {}
                for index,item in  enumerate(item1):
                    temp_json[label_name_arr[index]]=item
                temp_arr.append(temp_json)
        except:
            # 发生错误时回滚
            self.__conn.rollback()
        return temp_arr


    # Deleting (Calling destructor)
    def __del__(self):
        # 析构函数  每次结束时候调用
        self.__cursor.close()
        self.__conn.close()

if __name__ == '__main__':
    #测试专用
    obj = db_mysql_detail()
    print(obj.getmodellabel())