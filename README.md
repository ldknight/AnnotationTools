# AnnotationTools
## demo
<img width="1435" alt="image" src="https://user-images.githubusercontent.com/44898094/233643477-79a0330c-dcf2-4fdc-bc53-cc499ba45d2c.png">

# 安装
参考segment anything安装方式

# 运行：
python annotation-api/control_main.py
配置文件：annotation-api/config.py
默认使用cpu计算、模型选择sam_vit_h_4b8939.pth 可在配置文件中更改

前端页面：annotool/index.html


# 使用流程：
1-添加项目（输入本地图片文件夹地址）；
2-添加本项目所需标签；
3-目标标记与识别；
4-对识别结果进行标注标签；
5-切换图片继续执行操作；
6-导出coco style annotation.txt


# 快捷键       
1--左击==>正样本点；
2--右击==>负样本点；
3--左键点击选中目标可拖拽；
4--左键绘制矩形；
5--滚轮缩放画布；
6--右键+alt键可拖拽画布；
7--空格键==>执行检索识别画布区域

**前端目录**       
/AnnotationTools/annotool

**后端目录**       
/annotation-api

**数据库**      
/test.db
