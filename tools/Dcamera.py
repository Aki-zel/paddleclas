# First import the library
import pyrealsense2 as rs
# Import Numpy for easy array manipulation
import numpy as np
# Import OpenCV for easy image rendering
import cv2


class Dcamera:

    def __init__(self,limit):
        self.pipeline = rs.pipeline()
        self.config = rs.config()
        # 获取摄像头内参
        self.pipeline_wrapper = rs.pipeline_wrapper(self.pipeline)
        self.pipeline_profile = self.config.resolve(self.pipeline_wrapper)
        self.device = self.pipeline_profile.get_device()
        self.device_product_line = str(
            self.device.get_info(rs.camera_info.product_line))
        # 判断是否有RGB图像
        found_rgb = False
        for s in self.device.sensors:
            if s.get_info(rs.camera_info.name) == 'RGB Camera':
                found_rgb = True
                break
        if not found_rgb:
            print("The demo requires Depth camera with Color sensor")
            exit(0)

        self.config.enable_stream(rs.stream.depth, 1280, 720, rs.format.z16, 30)
        self.config.enable_stream(rs.stream.color, 1280, 720, rs.format.bgr8, 30)
        self.profile = self.pipeline.start(self.config)
        # 超过的距离屏蔽图像
        self.depth_sensor = self.profile.get_device().first_depth_sensor()
        self.depth_scale = self.depth_sensor.get_depth_scale()
        print("Depth Scale is: ", self.depth_scale)

        self.clipping_distance_in_meters = limit  # 1 米
        self.clipping_distance = self.clipping_distance_in_meters / self.depth_scale
        # 对齐摄像头的数据流
        self.align_to = rs.stream.color
        self.align = rs.align(self.align_to)

    def getFrame(self):
        frames = self.pipeline.wait_for_frames()
        # 对齐深度帧和颜色帧
        aligned_frames = self.align.process(frames)
        # 校准画面
        aligned_depth_frame = aligned_frames.get_depth_frame()
        color_frame = aligned_frames.get_color_frame()
        # 获取图像以及深度信息
        depth_image = np.asanyarray(aligned_depth_frame.get_data())
        color_image = np.asanyarray(color_frame.get_data())
        return depth_image, color_image

    def getNoBackFrame(self):
        depth_image, color_image = self.getFrame()
        # 设置被屏蔽的背景颜色
        grey_color = 0
        # depth image is 1 channel, color is 3 channels
        depth_image_3d = np.dstack(
            (depth_image, depth_image, depth_image))
        bg_removed = np.where((depth_image_3d > self.clipping_distance) | (
                depth_image_3d <= 0), grey_color, color_image)
        depth_colormap = cv2.applyColorMap(cv2.convertScaleAbs(depth_image, alpha=0.03), cv2.COLORMAP_JET)
        return depth_colormap, bg_removed

    def getHstack(self):
        depth_colormap, bg_removed = self.getNoBackFrame()
        images = np.hstack((bg_removed, depth_colormap))
        return images
    def adjust_brightness(self,image, brightness_factor):
        # 转换图像颜色空间为 HSV
        hsv_image = cv2.cvtColor(image, cv2.COLOR_BGR2HSV)
        
        # 调整亮度
        hsv_image[:,:,2] = hsv_image[:,:,2] * brightness_factor
        
        # 转换回 BGR 颜色空间
        bgr_image = cv2.cvtColor(hsv_image, cv2.COLOR_HSV2BGR)
        
        return bgr_image
    def close(self):
        self.pipeline.stop()