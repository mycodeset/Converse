from selenium import webdriver
from user_agent_tool import *
import time
import random
class browser_tool(object):
    def __init__(self):
        _user_agent_tool = user_agent_tool()
        _user_agent = _user_agent_tool.get_user_agent()
        chromeOptions = webdriver.ChromeOptions()
        chromeOptions.add_argument('--disable-gpu')
        chromeOptions.add_argument('--log-level=3')
        # chromeOptions.add_argument('user-agent='+_user_agent)
        self.driver = webdriver.Chrome(chrome_options=chromeOptions)
        self.driver.set_window_size(500,1000)
        # self.driver.maximize_window()  
    #获取窗口驱动
    def get_driver(self):
        return self.driver
    def get_url(self,url):
        self.__open_url(url)
    #打开匡威商城界面
    def open_converse(self):
        self.__open_url('https://m.converse.com.cn/member/login.htm')
    def get_cookies(self):
        return self.driver.get_cookies()
    #返回上一页界面
    def back_page(self):
        self.driver.back()
    #刷新界面
    def refresh_page(self):
        self.driver.refresh()
    #截图
    def screenshot(self,FileName):
        self.driver.get_screenshot_as_file(FileName)
    #关闭浏览器
    def close_chrome(self):
        self.driver.delete_all_cookies()
        self.driver.quit()
    def __open_url(self,url):
        try:
            self.driver.get(url)
        except Exception:
            print('打开网页超时')
            try:
                self.driver.get(url)
            except Exception:
                print('打开网页超时')
                self.driver.quit()