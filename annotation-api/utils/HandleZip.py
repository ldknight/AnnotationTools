import os
import zipfile
#对文件进行压缩
class HandleZip:
    def __init__(self, zip_path='Zipped_file.zip'):
        if os.path.exists(zip_path):  # 如果文件存在
            os.remove(zip_path)
        self.zipf = zipfile.ZipFile(zip_path, 'w', zipfile.ZIP_DEFLATED)
    '''生成zip压缩文件 path:需要压缩的文件路径  ziph为zipfile实例  eg.zipfile.ZipFile('Zipped_file.zip', 'w', zipfile.ZIP_DEFLATED)'''
    def zipdir(self,path):
        if os.path.exists(path):
            self.zipf.write(path)
        # ziph is zipfile handle
        # for root, dirs, files in os.walk(path):
        #     for file in files:
        #         self.zipf.write(os.path.join(root, file))
    # Deleting (Calling destructor)
    def __del__(self):
        # 析构函数  每次结束时候调用
        self.zipf.close()

if __name__ == '__main__':
    #测试专用
    obj = HandleZip()
    obj.zipdir(path='HandleData.py')
    obj.zipdir(path='MyResultRole.py')