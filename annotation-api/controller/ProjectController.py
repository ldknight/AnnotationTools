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





