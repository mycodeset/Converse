import requests
import json
import time
import re
import random
from user_agent_tool import *
class converse_post():
    def __init__(self):
        self._num = 1
        self._user_agent_tool = user_agent_tool()
        self._session = requests.session()
        self._isEnoughStock_response = {
            'returnUrl':'',
            'isEnoughStock':'',
            'uuid':''
        }
        self._orderId = None
        self._user_email = None

    def __requests_get(self,url,headers):
        response = self._session.get(url = url,headers = headers,verify = False)
        response.encoding = 'utf-8'
        if response.status_code == '403':
            print('在get访问{}时，服务器拒绝访问...'.format(url))
        return response

    def __requests_post(self,url,headers,data):
        response = self._session.post(url = url,headers = headers,data = data,verify = False)
        response.encoding = 'utf-8'
        if response.status_code == '403':
            print('在post访问{}时，服务器拒绝访问...'.format(url))
        return response
    
    def set_cookies(self,cookies_dict):
        self._session.cookies.clear_session_cookies()
        cookieJar = requests.cookies.RequestsCookieJar()
        for cookie in cookies_dict:
            cookieJar.set(cookie["name"], cookie["value"])
        self._session.cookies.update(cookieJar)
    
    def isEnoughStock(self,item_jmskuCode,item_url):
        url = 'https://m.converse.com.cn/isEnoughStock.json'
        headers = {
            'Host':'m.converse.com.cn',
            'User-Agent':self._user_agent_tool.get_user_agent(),
            'Accept':'*/*',
            'Accept-Language':'zh-CN,zh;q=0.8,zh-TW;q=0.7,zh-HK;q=0.5,en-US;q=0.3,en;q=0.2',
            'Accept-Encoding':'gzip, deflate, br',
            'Referer':item_url,
            'Content-Type':'application/x-www-form-urlencoded; charset=UTF-8',
            'X-Requested-With':'XMLHttpRequest',
            'Content-Length':'59',
            'Connection':'keep-alive'
        }
        data = {
            'challenge':'',
            'validate':'',
            'seccode':'',
            'jmskuCode':item_jmskuCode,
            'num':self._num
        }
        response = self.__requests_post(url,headers,data)
        print('isEnoughStock:',response.text)
        try:
            json_data = json.loads(response.text)
        except json.JSONDecodeError:
            print('处理{}的isEnoughStock时发生：json.decoder.JSONDecodeError错误'.format(item_jmskuCode))
            return False
        if 'uuid' in json_data:
            self._isEnoughStock_response['uuid'] = json_data['uuid']
        else:
            self._isEnoughStock_response['uuid'] = ''
        if 'returnUrl' in json_data:
            self._isEnoughStock_response['returnUrl'] = json_data['returnUrl']
        else:
            self._isEnoughStock_response['returnUrl'] = ''
        try:
            isEnoughStock_result = json_data['isEnoughStock']
        except:
            print('处理{}的json_data["isEnoughStock"]时出错，默认返回False'.format(item_jmskuCode))
            isEnoughStock_result = False
        return isEnoughStock_result
    
    def nowBuy(self,item_jmskuCode,item_url):
        if len(self._isEnoughStock_response['returnUrl']) < 1:
            url = 'https://m.converse.com.cn/nowBuy.htm?loxiaflag={}'.format(str(round(time.time() * 1000)))
        else:
            url = 'https://m.converse.com.cn'+str(self._isEnoughStock_response['returnUrl'])
        headers = {
            'Host':'m.converse.com.cn',
            'User-Agent':self._user_agent_tool.get_user_agent(),
            'Accept':'*/*',
            'Accept-Language':'zh-CN,zh;q=0.8,zh-TW;q=0.7,zh-HK;q=0.5,en-US;q=0.3,en;q=0.2',
            'Accept-Encoding':'gzip, deflate, br',
            'Referer':item_url,
            'Content-Type':'application/x-www-form-urlencoded; charset=UTF-8',
            'X-Requested-With':'XMLHttpRequest',
            'Content-Length':'66',
            'Connection':'keep-alive'
        }
        data_uid = {
            'jmskuCode':item_jmskuCode,
            'num':self._num,
            'uid':self._isEnoughStock_response['uuid']
        }
        data = {
            'jmskuCode':item_jmskuCode,
            'num':self._num,
        }
        if len(self._isEnoughStock_response['uuid']) > 1:
            data = data_uid
        response = self.__requests_post(url,headers,data)
        print(response.text)
        if '超过限制' in response.text:
            return 'ERROR'
        if '请先登录' in response.text:
            input('登录状态失效，请登录后回车继续...')
            return False
        json_data = json.loads(response.text)
        try:
            if json_data['returnCode'] == 'E':
                print('购买失败...')
                return False
        except Exception:
            pass
        return True
    def checkout(self,item_url):
        url = 'https://m.converse.com.cn/order/checkout.htm?isBuyNow=true'
        headers = {
            'Host':'m.converse.com.cn',
            'User-Agent':self._user_agent_tool.get_user_agent(),
            'Accept':'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
            'Accept-Language':'zh-CN,zh;q=0.8,zh-TW;q=0.7,zh-HK;q=0.5,en-US;q=0.3,en;q=0.2',
            'Accept-Encoding':'gzip, deflate, br',
            'Referer':item_url,
            'Connection':'keep-alive',
            'Upgrade-Insecure-Requests':'1'
        }
        response = self.__requests_get(url,headers)
        orderId_patton = '[0-9a-z]{8}-[0-9a-z]{4}-[0-9a-z]{4}-[0-9a-z]{4}-[0-9a-z]{12}'
        result = re.findall(orderId_patton,response.text)
        if len(result) > 0:
            self._orderId = result[0]
        else:
            self._orderId = ''
            print('获取订单ID失败...')
            return False
        
        print('订单ID:',self._orderId)
        return True

    def createOrder(self,item_name):
        url = 'https://m.converse.com.cn/order/createOrder.json'
        headers = {
            'Host':'m.converse.com.cn',
            'User-Agent':self._user_agent_tool.get_user_agent(),
            'Accept':'*/*',
            'Accept-Language':'zh-CN,zh;q=0.8,zh-TW;q=0.7,zh-HK;q=0.5,en-US;q=0.3,en;q=0.2',
            'Accept-Encoding':'gzip, deflate, br',
            'Referer':'https://m.converse.com.cn/order/checkout.htm?isBuyNow=true',
            'Content-Type':'application/x-www-form-urlencoded; charset=UTF-8',
            'X-Requested-With':'XMLHttpRequest',
            'Content-Length':'217',
            'Connection':'keep-alive'
        }
        data = {
            'invoiceType':'PERSON',
            'companyName':'',
            'companyTax':'',
            'paymentType':'601',
            'paymentBank':'zhifubao',
            'isBuyNow':'true',
            'orderId':self._orderId,
            'challenge':'',
            'validate':'',
            'seccode':'',
            'screenwidth':'360',
            'screenheight':'720',
            'track':[]
        }
        if len(self._orderId) == 0:
            print('订单编号不存在,订单提交失败...')
            return
        # response = self.session.post(url=url,headers=headers,data=data,verify=False,timeout = 30,proxies = self.proxies)
        response = self.__requests_post(url=url,headers=headers,data=data)
        print('status_code : ',response.status_code)
        if str(response.status_code) == '403':
            print('在创建订单时，服务器拒绝访问...')
            return False
        response.encoding = 'utf-8'
        f = open('./成功记录.txt','a+',encoding = 'utf-8')
        log = '{log_time}\t{item_name}\t{user_email}\t{result}\n'.format(log_time = str(time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())),item_name = item_name,user_email = self._user_email,result = str(response.text))
        f.write(log)
        f.close()
        print(response.text)
        return str(response.text)
    def set_user_email(self):
        url = 'https://m.converse.com.cn/myshop/updatememberinfo.htm?loxiaflag='+str(round(time.time() * 1000))
        headers = {
            'Host':'m.converse.com.cn',
            'User-Agent':self._user_agent_tool.get_user_agent(),
            'Accept':'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
            'Accept-Language':'zh-CN,zh;q=0.8,zh-TW;q=0.7,zh-HK;q=0.5,en-US;q=0.3,en;q=0.2',
            'Accept-Encoding':'gzip, deflate, br',
            'Referer':'https://m.converse.com.cn/member/addressList.htm?loxiaflag={}'.format(str(round(time.time()*1000)-random.randint(1000,3000))),
            'Connection':'keep-alive',
            'Upgrade-Insecure-Requests':'1'
        }
        response = self.__requests_get(url,headers)
        html_doc = response.text
        reg = "[\w!#$%&'*+/=?^_`{|}~-]+(?:\.[\w!#$%&'*+/=?^_`{|}~-]+)*@(?:[\w](?:[\w-]*[\w])?\.)+[\w](?:[\w-]*[\w])?"
        email_list = re.findall(reg,html_doc)
        result_list = []
        for emailAdd in email_list:
            if (emailAdd != 'example@converse.com'):
                result_list.append(emailAdd)
                
        print('当前账号的邮箱地址为：{}，若邮箱地址为空说明登录状态已经丢失'.format(result_list))
        self._user_email = str(result_list)