from PIL import Image
import numpy as np


class Get_Slide_IMG_Position(object):
    def __init__(self, bg_img_path=None, slide_img_path=None, fullbg_img_path=None) -> None:
        super().__init__()
        self.bg_img_path = bg_img_path
        self.slide_img_path = slide_img_path
        self.fullbg_img_path = fullbg_img_path

    # 比较两张图片的像素点，获得坐标缺口
    def defference_between_bg_fullbg(self):

        # 两张图同时存在则进行处理
        if self.bg_img_path and self.fullbg_img_path:

            # 读取bg所有像素点数组
            bg = Image.open(self.bg_img_path)
            bg_pixel_array = np.asarray(bg)

            # 读取fullbg所有像素点数组
            fullbg = Image.open(self.fullbg_img_path)
            fullbg_pixel_array = np.asarray(fullbg)

            # 图片尺寸
            size = fullbg_pixel_array.shape
            width = size[1]
            height = size[0]

            # 遍历所有像素点
            position = 260
            for row in range(height):  # 遍历每一行
                for col in range(width):  # 遍历每一列

                    # 获取两张图片同一位置的像素点
                    bg_pixel = bg_pixel_array[row, col]
                    fullbg_pixel = fullbg_pixel_array[row, col]

                    # 设置一个Δ值
                    defference = 40
                    # 两张图像素点的r/g/b值之差大于defference则说明找到缺口坐标
                    if abs(int(bg_pixel[0]) - int(fullbg_pixel[0])) > defference and abs(
                            int(bg_pixel[1]) - int(fullbg_pixel[1])) > defference and abs(
                            int(bg_pixel[2]) - int(fullbg_pixel[2])) > defference:
                        if position > col:
                            position, col = col, position
                        # 只需要水平方向的距离，返回position即可
                        return position
        else:
            raise ValueError('缺少bg_img_path或fullbg_img_path参数')

    # 如果没有获取到bg_img_path/fullbg_img_path则单独处理slide_img_path
    def single_img_position(self):
        # 功能待完成
        # image_file = Image.open("./20210720184120.png") # open colour image
        # # 改变图片灰度
        # image_file = image_file.convert('L') # convert image to black and white
        # image_file.save('result.png')
        # 检测同一张图片上的直线缺口位置
        if self.slide_img_path:
            pass
        else:
            raise ValueError('缺少slide_img_path参数')


# slide = Get_Slide_IMG_Position()
# slide.bg_img_path = './static/bg.png'
# slide.fullbg_img_path = './static/fullbg.png'
# # 获取滑动距离
# position = slide.defference_between_bg_fullbg()
# print(position)