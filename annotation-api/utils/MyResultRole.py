from flask import jsonify
'''
    返回结果
'''
class MyResultRole:
    @staticmethod
    def ResSuccess(msg='处理成功！',data={}):
        resdata={
            'code':200,
            'msg':msg,
            'success':True,
            'data':data
        }
        return jsonify(resdata)

    @staticmethod
    def ResError(code=201,msg='处理失败！', data={}):
        resdata = {
            'code': code,
            'msg': msg,
            'success': False,
            'data': data
        }
        return jsonify(resdata)
