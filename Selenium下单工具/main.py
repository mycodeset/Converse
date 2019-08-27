import json
import time
from converse_monitor import *
from converse_browser import *
from converse_post import *
def get_file_data():
    f = open('./货号.json','r',encoding = 'utf-8')
    data = f.read()
    data = data.encode('utf-8').decode('utf-8-sig').strip()
    f.close()
    return json.loads(data)['item']
def Timing_function(time_flag):
    while True:
        print('当前时间：',time.strftime("%Y-%m-%d %H:%M:%S", time.localtime()),end = '\r')
        now_time = int(time.time()*1000)
        if now_time >= time_flag:
            break
if __name__ == "__main__":
    time_flag = 1566436199000
    con_monitor = converse_monitor()
    con_browser = converse_browser()
    con_post = converse_post()
    item_list = get_file_data()
    con_browser.login()
    cookies = con_browser.get_cookies()
    con_post.set_cookies(cookies)
    con_post.set_user_email()
    # Timing_function(time_flag) #定时功能
    while True:
        try:
            for item in item_list:
                con_browser.login_status()
                item_skucode = item['item_skucode']
                item_name = item['item_name']
                item_url = item['item_url']
                item_size_list = item['item_size_list']
                jmskuCode_list = con_monitor.get_inventory(item_skucode,item_name,item_url,item_size_list)
                for jmskuCode in jmskuCode_list:
                    cookies = con_browser.get_cookies()
                    con_post.set_cookies(cookies)
                    isEnoughStock_result = con_post.isEnoughStock(item_jmskuCode = jmskuCode,item_url = item_url)
                    if isEnoughStock_result:
                        nowBuy_result = con_post.nowBuy(item_jmskuCode = jmskuCode,item_url = item_url)
                    else:
                        continue
                    if nowBuy_result == True:
                        con_browser.open_order_page()
                    elif nowBuy_result == 'ERROR':
                        break
                    else:
                        continue
                    # if nowBuy_result:
                    #     checkout_result = con_post.checkout(item_url)
                    # else:
                    #     continue
                    # if checkout_result:
                    #     createOrder_result = con_post.createOrder(item_name)
                    # if createOrder_result == False:
                    #     con_browser.open_order_page()
            time.sleep(random.randint(1000,3000)/1000.0)
        except Exception:
            traceback.print_exc()

