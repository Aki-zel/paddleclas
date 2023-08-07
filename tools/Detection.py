import fastdeploy.vision as vision
import fastdeploy as fd
import os
import sys
#改成自己的根目录
ROOT_DIR = os.path.abspath('C:/Users/LiMei/Desktop/Second shopping/AI-Visual')
sys.path.append(ROOT_DIR)

class Detection:
    score = 0.7

    def __init__(self, model_file, params_file, config_file):
        self.result = None
        self.model = None
        self.model_file = model_file
        self.params_file = params_file
        self.config_file = config_file
        # self.loadModel()

    def loadModel(self):
        self.model = vision.detection.PPYOLOE(self.model_file,
                                              self.params_file,
                                              self.config_file,
                                              runtime_option=self.option)

    def setScore(self, score):
        self.score = score

    def Predicts(self, img):
        # 图片格式注意需为HWC，BGR格式
        self.result = self.model.predict(img)
        # boxes(list of list(float)): 成员变量，表示单张图片检测出来的所有目标框坐标。
        # boxes是一个list，其每个元素为一个长度为4的list， 表示为一个框，每个框以4个float数值依次表示xmin, ymin, xmax, ymax， 即左上角和右下角坐标
        # scores(list of float): 成员变量，表示单张图片检测出来的所有目标置信度
        # label_ids(list of int): 成员变量，表示单张图片检测出来的所有目标类别
        return self.result

    def visual(self, img):
        vis_im = vision.vis_detection(img, self.result, score_threshold=self.score)
        return vis_im

    def setOption(self,type,trt):
        self.option = fd.RuntimeOption()
        if type== "kunlunxin":
            self.option.use_kunlunxin()
        if type== "ascend":
            self.option.use_ascend()
        if type== "gpu":
            self.option.use_gpu()
        if type=="cpu":            self.option.use_cpu()
        if trt:
            self.option.use_trt_backend()
            # self.option.use_paddle_infer_backend()
            # self.option.paddle_infer_option.enable_trt = True
            # self.option.set_trt_cache_file("cache/model.trt")
            self.option. trt_option.serialize_file = "cache/model.trt"
        return self.option
