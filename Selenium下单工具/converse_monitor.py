import requests
import winsound
import urllib3
import random
import json
import time
class converse_monitor():
    def __init__(self):
        self._session = requests.session()
        urllib3.disable_warnings()

    def __requests_get(self,url,headers):
        response = self._session.get(url = url,headers = headers,verify = False)
        response.encoding = 'utf-8'
        if response.status_code == '403':
            print('在获取库存时，服务器拒绝访问...')
        return response

    def __requests_post(self,url,headers,data):
        response = self._session.post(url = url,headers = headers,data = data,verify = False)
        response.encoding = 'utf-8'
        if response.status_code == '403':
            print('在获取库存时，服务器拒绝访问...')
        return response
    
    def get_inventory(self,item_skucode,item_name,item_url,item_size_list):
        result = []
        url = 'https://m.converse.com.cn/inventory/{}.json'.format(item_skucode)
        headers = {
            'Host':'m.converse.com.cn',
            'User-Agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.{rand_1} (KHTML, like Gecko) Chrome/76.0.3809.{rand_2} Safari/537.{rand_3}'.format(rand_1 = random.randint(10,100),rand_2 = random.randint(10,100),rand_3 = random.randint(10,100)),
            'Accept':'*/*',
            'Accept-Language':'zh-CN,zh;q=0.8,zh-TW;q=0.7,zh-HK;q=0.5,en-US;q=0.3,en;q=0.2',
            'Accept-Encoding':'gzip, deflate, br',
            'Referer':item_url,
            'X-Requested-With':'XMLHttpRequest',
            'Connection':'keep-alive'
        }
        response = self.__requests_get(url,headers)
        response_text = response.text
        
        try:
            json_data = json.loads(response_text)
        except Exception:
            print('库存response返回内容有误...')
            print(response_text)
        
        if 'skuStatus' in json_data:
            print(item_name,'无货...')
            return result
        
        print(time.strftime("%Y-%m-%d %H:%M:%S", time.localtime()),item_name,'库存详情')
        sizeRefList = json_data['sizeRefList']
        sizeRefList.sort(key = lambda k: (k.get('inventoryStatus')),reverse=True)
        for sizeRef in sizeRefList:
            chinaSize = sizeRef['chinaSize']
            inventoryStatus = sizeRef['inventoryStatus']
            jmskuCode = sizeRef['jmskuCode']
            print('尺码：',chinaSize,'\t库存：',inventoryStatus,'\t编号：',jmskuCode)
            if str(inventoryStatus) == 'T':
                for item_size in item_size_list:
                    if str(chinaSize) == str(item_size):
                        result.append(jmskuCode)
        
        if len(result)>0:
            try:
                winsound.Beep(1200,500)
            except:
                pass
        return result