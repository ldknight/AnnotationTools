from flask import Blueprint, request
from utils.HandleData import HandleData
from utils.MyResultRole import MyResultRole
from server.ProjectServe import ProjectServer

project_api = Blueprint('project_api', __name__)

@project_api.route('/project/addProject', methods=['POST', 'GET'])
# 添加Project
def addProject(proj_url=""):
    proj_url = HandleData.request_parse_equal(proj_url, locals())
    res_ = ProjectServer.addProject(ProjectServer(), proj_url=proj_url)
    if res_['proj_id']:
        return MyResultRole.ResSuccess(data=res_)
    return MyResultRole.ResError('添加失败！')

@project_api.route('/project/getProjectList', methods=['POST', 'GET'])
# 添加Project
def getProjectList():
    res_ = ProjectServer.getProjectList(ProjectServer())
    return MyResultRole.ResSuccess(data=res_)



@project_api.route('/project/deleteProject', methods=['POST', 'GET'])
# 删除label
def deleteProject(proj_id=0):
    proj_id = HandleData.request_parse_equal(proj_id, locals())
    res_flag = ProjectServer.del_proj(ProjectServer(), proj_id)
    if res_flag:
        return MyResultRole.ResSuccess(msg='删除成功！')
    else:
        return MyResultRole.ResError(msg="删除失败")

@project_api.route('/project/getProjectInfo', methods=['POST', 'GET'])
# 添加Project
def getProjectInfo(proj_id=0):
    proj_id = HandleData.request_parse_equal(proj_id, locals())
    res_ = ProjectServer.getProjectInfo(ProjectServer(),proj_id)
    return MyResultRole.ResSuccess(data=res_)


