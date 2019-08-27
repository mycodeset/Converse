import requests
from urllib.parse import urlencode
import re
import winsound
import time
from skimage import io
import traceback
if __name__ == "__main__":
    """
    用于监控converse中国官网商品上新
    """
    URL = 'https://www.converse.com.cn/sneakers/category.htm?'
    query_string = {
        'attributeParams':'',
        'propertyCode':'',
        'size':'',
        'maxprice':'',
        'minprice':'',
        'sort':'showOrder',
        'pageNo':'1',
        'rowsNum':'',
        'isPaging':'false'
    }
    headers = {
        'Host':'www.converse.com.cn',
        'user-agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:68.0) Gecko/20100101 Firefox/68.0',
        'accept':'*/*',
        'accept-language':'zh-CN,zh;q=0.8,zh-TW;q=0.7,zh-HK;q=0.5,en-US;q=0.3,en;q=0.2',
        'accept-encoding':'gzip, deflate, br',
        'x-requested-with':'XMLHttpRequest',
        'dnt':'1',
        'referer':'https://www.converse.com.cn/sneakers/category.htm'
    }
    skuCode_list = [] #存放商品信息
    first_flag = True

    while True:
        item_sum = 0
        try:
            for index in range(1,100):
                query_string['pageNo'] = index
                url = URL + urlencode(query = query_string)
                response = requests.get(url = url,headers = headers)
                response.encoding = 'utf-8'
                # pattern = '(<dl.*?</dl>)'
                pattern = '<dl.*?skuCode="(.*?)".*?lazy_src="(.*?)".*?</dl>'
                item_list = re.findall(pattern = pattern,string = response.text)
                for item in item_list:
                    item_sum += 1
                    skuCode = item[0]
                    img_url = 'https:{}'.format(item[1])
                    if skuCode not in skuCode_list:
                        skuCode_list.append(skuCode)
                        if not first_flag:
                            print('发现新商品：{},图片链接为：{}'.format(skuCode,img_url))
                            try:
                                winsound.Beep(1200,1000)
                                image = io.imread(img_url)
                                io.imshow(image)
                                io.show()
                            except:
                                pass
                if len(item_list) == 0:
                    msg = '{now_time} \t Response_Code:{response_code} \t 最后页码为:{index} \t 鞋类商品总数为:{item_sum}'.format(now_time = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime()),response_code = response.status_code,index = index,item_sum = item_sum)
                    print(msg)
                    break
            first_flag = False
        except Exception:
            traceback.print_exc()
