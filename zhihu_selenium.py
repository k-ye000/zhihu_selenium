import os
import random
from time import sleep
from selenium.common.exceptions import ElementClickInterceptedException
import requests
from selenium.webdriver import ActionChains, Chrome, ChromeOptions

from utils.generate_array import generate_move_array
from utils.slide_img_position import Get_Slide_IMG_Position
from utils.user_agent_list import random_ua


class ZhihuSelenium(object):
    def __init__(self) -> None:
        super().__init__()
        self.position = None
        self.options = ChromeOptions()
        self.options.add_argument('--disable-gpu')
        self.options.add_argument('-–ignore-certificate-errors')
        self.options.add_argument('--start-maximized')
        # self.options.add_argument('user-agent='+random_ua())
        # 此步骤很重要，设置为开发者模式，防止被各大网站识别出来使用了Selenium
        self.options.add_experimental_option('useAutomationExtension', False)
        self.options.add_experimental_option('excludeSwitches', ['enable-automation'])
        # 屏蔽webdriver特征
        self.options.add_argument("--disable-blink-features")
        self.options.add_argument("--disable-blink-features=AutomationControlled")
    
    def login(self):
        browser = Chrome(executable_path='./chromedriver.exe',
                          options=self.options)
        
        browser.execute_cdp_cmd("Page.addScriptToEvaluateOnNewDocument", {
                                "source": """
                                    Object.defineProperty(navigator, 'webdriver', {
                                    get: () => undefined
                                    })
                                """
                                })
        browser.get('https://www.zhihu.com/signin')

        # 定位密码登录
        login_elemnt = browser.find_element_by_xpath(
            '//*[@id="root"]/div/main/div/div/div/div[1]/div/form/div[1]/div[2]')
        login_elemnt.click()
        sleep(0.2)

        # 定位输入框
        element = browser.find_element_by_xpath(
            '//*[@id="root"]/div/main/div/div/div/div[1]/div/form/div[2]/div/label/input')
        # 清除浏览器保存的数据
        element.clear()
        # 输入账号
        element.send_keys('zhanghao')

        # 定位密码框
        sleep(0.5)
        element = browser.find_element_by_xpath(
            '//*[@id="root"]/div/main/div/div/div/div[1]/div/form/div[3]/div/label/input')
        # 清除浏览器保存的数据
        element.clear()
        # 输入密码
        element.send_keys('mima')

        sleep(0.2)
        # 点击登录按钮
        login_btn = browser.find_element_by_xpath(
            '//*[@id="root"]/div/main/div/div/div/div[1]/div/form/button')

        while login_btn:
            try:
                login_btn.click()
            except ElementClickInterceptedException:
                pass
            # 等待验证码加载
            sleep(3)
            # 获取当前滑动验证码图片
            bg_src = browser.find_element_by_xpath(
                "/html/body/div[4]/div[2]/div/div/div[2]/div/div[1]/div/div[1]/img[1]").get_attribute('src')
            print(bg_src)
            bg = self.get_bg(bg_src)

            # 如果可以获取到fullbg/bg,则调用difference_between_bg_fullbg
            if bg:
                # 实例化Slide_IMG_Position对象
                slide = Get_Slide_IMG_Position()
                if os.path.exists('./static/bg.png') and os.path.exists('./static/fullbg.png'):
                    slide.bg = './static/bg.png'
                    slide.fullbg = './static/fullbg.png'
                    self.position = slide.difference_between_bg_fullbg()

                if os.path.exists('./static/bg.png') or os.path.exists('./static/screenshot.png'):
                    # 此处预留当验证码图片已经无法获取或获取难度大时，从页面截图获取验证码图片
                    if os.path.exists('./static/bg.png'):
                        slide.slide_img_path = './static/bg.png'
                    else:
                        # 从页面截取的验证码图需要裁剪掉带滑块的部分
                        slide.slide_img_path = './static/screenshot.png'
                    self.position = slide.single_img_position()
                # 获取滑动距离

                print(self.position)

            if self.position:
                self.slide_img(browser, self.position)
            else:
                # 刷新验证码
                fresh_img_btn = browser.find_element_by_xpath(
                    '/html/body/div[4]/div[2]/div/div/div[2]/div/div[1]/div/div[3]/div')
                fresh_img_btn.click()
                sleep(0.2)

            login_btn = browser.find_element_by_xpath(
            '//*[@id="root"]/div/main/div/div/div/div[1]/div/form/button')
        
        return

    # 获取滑动图片
    @staticmethod
    def get_bg(bg_src):
        try:
            bg = requests.get(url=bg_src, headers={
                              'User-Agent': random_ua()}).content
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
        position = position
        print(position)

        # 定位滑动按钮
        slide_btn = browser.find_element_by_xpath(
            "/html/body/div[4]/div[2]/div/div/div[2]/div/div[2]/div[2]")

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

        # 释放按钮
        action_chains.release()
        action_chains.perform()


if __name__ == '__main__':
    zh = ZhihuSelenium()
    bro = zh.login()
