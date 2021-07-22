import base64
import os
import random
from time import sleep

from selenium.webdriver import ActionChains, Chrome, ChromeOptions

from utils.slide_img_position import Get_Slide_IMG_Position
from utils.generate_array import generate_move_array


class BilibiliSelenium(object):
    def __init__(self) -> None:
        super().__init__()
        self.position = None
        self.options = ChromeOptions()
        self.options.add_argument('-–ignore-certificate-errors')
        self.options.add_argument('--start-maximized')
        # 此步骤很重要，设置为开发者模式，防止被各大网站识别出来使用了Selenium
        self.options.add_experimental_option('excludeSwitches', ['enable-automation'])

    def login(self):
        browser = Chrome(executable_path='./chromedriver.exe', options=self.options)
        browser.get('https://passport.bilibili.com/login')
        start_url = browser.current_url
        # 定位输入框
        element = browser.find_element_by_id('login-username')
        # 清除浏览器保存的数据
        element.clear()
        # 输入账号
        element.send_keys('xxxxxxx')

        # 定位密码框
        sleep(0.5)
        element = browser.find_element_by_id('login-passwd')
        # 清除浏览器保存的数据
        element.clear()
        # 输入密码
        element.send_keys('123456')
        sleep(0.2)
        # 点击登录按钮
        btn = browser.find_element_by_xpath(
            '//*[@id="geetest-wrap"]/div/div[5]/a[1]')
        btn.click()

        # 验证错误后重试
        while start_url == 'https://passport.bilibili.com/login':
            # 等待验证码加载完成
            sleep(3)
            # 获取fullbg
            get_fullbg = self.get_fullbg(browser)
            # 获取当前滑动验证码
            get_bg = self.get_bg(browser)
            # 如果可以获取到fullbg/bg,则调用defference_between_bg_fullbg
            if get_fullbg and get_bg:
                # 实例化Slide_IMG_Position对象
                slide = Get_Slide_IMG_Position()
                slide.bg_img_path = './static/bg.png'
                slide.fullbg_img_path = './static/fullbg.png'
                # 获取滑动距离
                self.position = slide.defference_between_bg_fullbg()
                # print(self.position)
            # 如果无法获取到fullbg/bg,则直接截取验证码图片,调用single_img_position
            else:
                screenshot = browser.save_screenshot('./static/screenshot.png')
            if self.position:
                self.slide_img(browser, self.position)

            # 登录成功后等待跳转加载
            sleep(2)
            start_url = browser.current_url
            if start_url == '':
                # 验证码不能一次通过时重试
                fresh_btn = browser.find_element_by_xpath('/html/body/div[2]/div[2]/div[6]/div/div[2]/div/a[2]')
                fresh_btn.click()
        return browser

    # 获得验证码原图
    @staticmethod
    def get_fullbg(browser):
        try:
            fullbg = browser.execute_script(
                'return document.getElementsByClassName("geetest_canvas_fullbg")[0].toDataURL("image/png");')
            fullbg = fullbg.split(',')[1]
            fullbg = base64.b64decode(fullbg)
            file_path = './static/'
            if not os.path.exists(file_path):
                os.mkdir(file_path)
            if os.path.exists(file_path + 'fullbg.png'):
                os.remove(file_path + 'fullbg.png')
            with open(file_path + 'fullbg.png', 'wb')as f:
                f.write(fullbg)
            return True
        except Exception:
            return False

    # 获取滑动图片
    @staticmethod
    def get_bg(browser):
        try:
            bg = browser.execute_script(
                'return document.getElementsByClassName("geetest_canvas_bg")[0].toDataURL("image/png");')
            bg = bg.split(',')[1]
            bg = base64.b64decode(bg)
            file_path = './static/'
            if not os.path.exists(file_path):
                os.mkdir(file_path)
            with open(file_path + 'bg.png', 'wb')as f:
                f.write(bg)
            return True
        except Exception as e:
            print(e)
            return False

    @staticmethod
    def slide_img(browser, position):
        # 实际验证码图片经过css样式调整，实际大小只有252，滑块边缘还有8像素间隙
        # position=int(position*252/260)-8
        position = position - 8
        print(position)
        # 定位滑动按钮
        slide_btn = browser.find_element_by_xpath("/html/body/div[2]/div[2]/div[6]/div/div[1]/div[2]/div[2]")
        # 绑定ActionChains
        action_chains = ActionChains(browser)
        # 点击按住滑动按钮
        action_chains.click_and_hold(on_element=slide_btn).perform()
        action_chains.pause(random.randint(1, 2) / 10)

        move_array = generate_move_array()
        move = 0
        for dis in move_array:
            # b站会检测鼠标轨迹和速度，人实际滑动鼠标时y轴不可能没有任何动作，这里要特别注意
            action_chains.move_by_offset(xoffset=dis, yoffset=2)
            move += dis
            if move > position:
                break
        action_chains.move_by_offset(xoffset=position - move, yoffset=-2)
        # # 返回-10，防止被检测
        # action_chains.move_by_offset(xoffset=-10, yoffset=0)
        # 释放按钮
        action_chains.release()
        action_chains.perform()


if __name__ == '__main__':
    bb = BilibiliSelenium()
    bro = bb.login()
    # input_btn=bro.find_element_by_xpath('//*[@id="nav_searchform"]/input')
    # input_btn.clear()
    # key_word=input('请输入：')
    # input_btn.send_keys(key_word)
    # search_btn=bro.find_element_by_xpath('//*[@id="nav_searchform"]/div')
    # search_btn.click()
