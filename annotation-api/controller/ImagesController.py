from server.ImagesServer import ImagesServer
<<<<<<< HEAD
from server.SegmentServer import SegmentServer
=======
from server.PublicServer import PublicServer
>>>>>>> 6eac0e736ecc73de9b8a5eb1473dd22da812728a
from flask import Blueprint, request
from utils.HandleData import HandleData
from utils.MyResultRole import MyResultRole
from flask import Flask
import numpy as np
import cv2
import os
from config import sam_checkpoint,device,model_type
import sys
sys.path.append("/root/AnnotationTools/segment_anything")
from segment_anything import sam_model_registry, SamAutomaticMaskGenerator, SamPredictor
app = Flask(__name__)
image_api = Blueprint('image_api', __name__)
sam = sam_model_registry[model_type](checkpoint=sam_checkpoint)
sam.to(device=device)
predictor = SamPredictor(sam)

@image_api.route('/image/getImageList', methods=['POST', 'GET'])
# 分页查询images列表
def getImageList(pageNo=1, page_size=20, proj_id=0):
    page_size = HandleData.request_parse_equal(page_size, locals())
    pageNo = HandleData.request_parse_equal(pageNo, locals())
    proj_id = HandleData.request_parse_equal(proj_id, locals())

    res = ImagesServer.limit_offset_query(ImagesServer(), pageNo=pageNo, page_size=page_size,proj_id=proj_id)
    return MyResultRole.ResSuccess(data=res)

#
def ndarray_to_list(d):
    for value in d:
        for key, v in value.items():
            if key=="segmentation":
                value[key]=np.where(v, 255, 0)
                img=cv2.Canny(np.uint8(value[key]),50,100)
                img[img < 255] = 0
                row_indices, col_indices = np.where(img == 255)
                value[key] = list(zip(row_indices, col_indices))
                
            if isinstance(value[key], np.ndarray):
                value[key] = value[key].tolist()
    return d

@image_api.route('/image/get_segment', methods=['GET'])
def get_segment():
    proj_id = request.args.get('proj_id')
    img_id = request.args.get('img_id')
    img_path=ImagesServer.getImagePath(proj_id=proj_id,imgid=img_id)
    img_path=img_path["imgpath"]
    current_path = os.path.abspath(__file__)
    current_directory = os.path.dirname(current_path)
    parent_directory = os.path.dirname(current_directory)
    imgpath=os.path.join(parent_directory,img_path[0][1])
    # image=cv2.imread(imgpath)
    image=cv2.imread("/root/AnnotationTools/gray_image.jpg")
    image = cv2.cvtColor(image,cv2.COLOR_BGR2RGB)
    mask_generator = SamAutomaticMaskGenerator(sam)
    masks = mask_generator.generate(image)
    masks=ndarray_to_list(masks)
    SegmentServer.insertSegment(img_id=img_id,proj_id=proj_id,masks=masks)
    return MyResultRole.ResSuccess(data=masks)
    
    
    
    

@image_api.route('/image/clear_img_segment', methods=['POST', 'GET'])
# 分页查询images列表
def clear_img_segment(img_id=0):
    img_id = HandleData.request_parse_equal(img_id, locals())
    res = PublicServer.clear_img_segment(PublicServer(),img_id=img_id)
    return MyResultRole.ResSuccess(data=res)






