'''
项目要求：获取百度图片的图片及其文本资料
使用工具：pycharm，postman，fiddler
难点在于请求头，有一个参数要上传，否则不会翻页，该参数只能pycharm测
'''
import requests
import time
import random
import re
import os
from jsonpath import jsonpath
import json

class Data ():
    def __init__(self):
        #请求头
        self.headers = {
            'Accept-Encoding': 'gzip, deflate, br',
            'Host': 'image.baidu.com',
            'Referer': 'https://image.baidu.com/search/index?tn=baiduimage&ps=1&ct=201326592&lm=-1&cl=2&nc=1&ie=utf-8&dyTabStr=MCwzLDQsMSw2LDUsMiw4LDcsOQ%3D%3D&word=jk%E5%A6%B9%E5%AD%90%E7%85%A7%E7%89%87',
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/102.0.5005.124 Safari/537.36 Edg/102.0.1245.44'
            }
        #代理ip，该网站封ip过于频繁
        self.proxies ={'http': '27.156.196.130:4245', 'https': '27.156.196.130:4245'}

    def get_data(self):  # 获取网站数据，获取接口，网页处理
        print (1)
        time.sleep (random.randint (3, 6))
        url = 'https://image.baidu.com/search/acjson'
        html_data = requests.get (url, headers=self.headers, proxies=self.proxies, params=self.parmas)
        data_1 = html_data.text#获取到接口数据
        data_2 = json.loads (data_1)
        return data_2#json化数据

    def fx_data(self, data):  # 解析数据，获取到图片以及文本，接口处理
        time.sleep (2)
        print (2)
        name = jsonpath (data, '$..fromPageTitleEnc')#文本，作用于文件创建时命名
        url_2 = jsonpath (data, '$..middleURL')#图片链接
        print(url_2)
        print(name)
        return name, url_2

    def bc_data(self, name, url_2, c,i,get):  # 保存数据，将数据进行进一步处理，图片链接处理
        print (3)
        dirs = rf'E:\\爬虫数据资料\爬虫资料\{get}'#文件夹位置
        if not os.path.exists (dirs):#判断文件夹是否存在，不存在则创建，方便后续查看
            os.makedirs (dirs)
        for username, url_jpg in zip (name, url_2):#循环拿出图片数据以及文本
            '''有一部分百度已经删除链接及文本，但框架还在占位置，
            进行判断，如果该链接不存在于百度中则跳过'''
            if not url_jpg:
                c += 1
                print(f'第{c}张照片网站缺失')
                continue
            headers = {
                'Host': 'image.baidu.com',
                'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/102.0.5005.124 Safari/537.36 Edg/102.0.1245.44',
            }
            url_jpg1 = requests.get (url_jpg,proxies=self.proxies,params=self.parmas)#图片数据
            tp = url_jpg1.content#图片的二进制数据
            a = re.findall (r'[^*"/:?\|<>]', username, re.S)#进行文件夹去除特殊符号
            chuli = "".join (a)
            with open (rf'{dirs}/{chuli}.jpg', 'wb') as f:#开始写入文件
                f.write (tp)
                c += 1
                print(f'这是第{i//30}页第{c}张')

    def main(self,get):
        print (4)
        c = 0#此为下载张数，方便用户随时查看下载进度
        for i in range (30, 600, 30):
            self.parmas = {
                #最新标签；lm为6以及同时配合latest:1
                'lm': '-1',#默认为-1，
                'latest':'',
                #最新标签
                #高清图片；如果该值为空，则为普通照片；如为1则为高清照片
                'hd':'1',
                #高清图片
                'tn':'resultjson_com',
                'word': f'{get}', # 应该为百度的搜索字符
                'pn': f'{i}'#翻页操作，该网站为异步网站，每次需要进行切换获取到接口的数据
            }
            print (f"这个接口是{i//30}页")
            data = self.get_data ()#获取到异步网页
            name, url_2 = self.fx_data (data)#获取到异步网页中数据
            if not name and not url_2:
                break
            self.bc_data (name, url_2, c,i,get)#进行保存
        print("所有图片抓取完成")

if __name__ == '__main__':
    print('想请求的图片类型')
    get=input("")#获取到用户想要下载的图片
    qd = Data ()  # 实例化
    qd.main (get)#调用Data中main方法，该方法主要进行程序运行
