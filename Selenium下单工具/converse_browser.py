from browser_tool import *
import traceback
import time
from selenium.webdriver.common.action_chains import ActionChains
class converse_browser():
    def __init__(self):
        self._browser = browser_tool()
        self._driver = self._browser.get_driver()
        self._window_handle = None
        self._login_status_flag = True
    
    def login(self):
        self._browser.open_converse()
        js = 'window.open("http://127.0.0.1/");'
        self._driver.execute_script(js)
        try:
            self._driver.switch_to_window(self._driver.window_handles[0])
            self._window_handle = self._driver.current_window_handle
        except:
            pass
        input('登录成功后，回车继续...')
    
    def open_order_page(self):
        try:
            self._driver.switch_to_window(self._driver.window_handles[1])
        except:
            print('窗口切换失败...')
        self._driver.get('https://m.converse.com.cn/order/checkout.htm?isBuyNow=true')
        submit_order = self._driver.find_element_by_id('submit_order')
        goods_img = self._driver.find_element_by_class_name('goods-img')
        # ActionChains(self._driver).drag_and_drop(submit_order, goods_img).perform() #防止403
        ActionChains(self._driver).move_to_element(submit_order).double_click().perform()
    
    def login_status(self):
        driver = self._driver
        H = int(time.strftime("%H",time.localtime()))
        M = int(time.strftime("%M",time.localtime()))
        S = int(time.strftime("%S",time.localtime()))

        if (M % 10 == 3 or M % 10 == 8) and (S % random.randint(10,60) < 9):
            if self._login_status_flag:
                self._login_status_flag  = False #只有在此条件才会继续执行后面的代码
            else:
                return
        elif (S % 10 == 4 or S % 10 == 9):
            self._login_status_flag = True
            return
        else:
            return
        
        if self._driver.current_window_handle != self._window_handle:
            self._driver.switch_to_window(self._driver.window_handles[0])
            self._window_handle = self._driver.current_window_handle
        try:
            url = 'https://m.converse.com.cn/myshop/updatememberinfo.htm'
            self._driver.get(url)
            ico_menu = driver.find_element_by_class_name('ico-menu') #菜单
            ActionChains(driver).move_to_element(ico_menu).click().perform()
            time.sleep(random.randint(500,1000)/1000.0)
            e_menu_btn = driver.find_element_by_class_name('e-menu-btn') #返回
            ActionChains(driver).move_to_element(e_menu_btn).click().perform()
            time.sleep(random.randint(500,1000)/1000.0)
            ico_cart = driver.find_element_by_class_name('ico-cart') #购物车
            ActionChains(driver).move_to_element(ico_cart).double_click().perform()
        except:
            print('login_status点击元素失败...')
            traceback.print_exc()

    def get_cookies(self):
        cookies = self._browser.get_cookies()
        return cookies
        