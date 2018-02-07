#!/usr/bin/env python 
#-*- coding:utf-8 -*-
'''
@author: lx0hacker
@date:2018-02-07
'''
import requests
from urllib.parse import unquote,urlparse
import re
import os
import os.path
from bs4 import BeautifulSoup
requests.packages.urllib3.disable_warnings()
import time
import random

'''
@url : 漫画的入口
@return 创建的文件夹的名字
'''
def is_exists(url):
    o = urlparse(url)
    s = re.match(r'\/comedy\/(.*?)\/(.*?)\/viewer',o.path)
    folder = unquote(s.group(1))+'/'+unquote(s.group(2))

    if not os.path.exists(unquote(s.group(1))):
        os.mkdir(unquote(s.group(1)))

    if not os.path.exists(folder):
        return False,folder
    else:
        return True,'emmm.... 这个文件夹'+unquote(s.group(2))

'''
@url 这里的url是refer的url
@return 每个图片的实际地址
'''
def get_img(url):
    data_url = []
    r = requests.get(url,verify=False)
    soup = BeautifulSoup(r.text,"html.parser")
    img_list = soup.find(id='_imageList').find_all('img')
    for img in img_list:
        data_url.append(img.get('data-url'))
    return data_url

'''
@referer 漫画的入口
@folder 存储的文件夹
'''
def save_img(referer,folder):
    headers = {
        "Referer":referer
    }
    data_url = get_img(referer)
    i=0
    for img_url in data_url:
        time.sleep(random.uniform(0.1,0.8))
        r =requests.get(img_url,headers=headers,verify=False)
        if r.status_code != 200:
            print('估计网络出现问题。status code : {}'.format(r.status_code))
            print('先暂停5秒')
            time.sleep(5)
            r = requests.get(img_url,headers=headers,verify=False)
            if r.status_code !=200:
                print("error! status code :{}".format(r.status_code))
                return 

        print('正在爬取漫画里面每个图片的地址.........')
        with open(folder+'/'+str(i)+'.jpg','wb')as f:
            f.write(r.content)
        i+=1

'''
@url 这里的url参数是refer的url，也是每一页具体的漫画
@page 这里的page是分页的页码数
返回每一页具体漫画的地址列表
'''
def start(url):
    flag,folder = is_exists(url)
    if not flag:
        print('往'+folder+'写入图片..........')
        os.mkdir(folder)
        save_img(url,folder)
    else:
        print(folder+'已经存在了!!!!!!!!!!!')


if __name__ == "__main__":
    url = input('输入第一话漫画的地址: ')
    num = 1 
    while True:
        #在这里增加参数从而爬取所有的漫画。注意选取的是跳转的url
        url = re.sub('episode_no=.*','episode_no='+str(num),url)
        r= requests.get(url)
        url =r.url
        if r.status_code == 200:
            start(url)
            num+=1
        elif r.status_code ==404:
            print('网页404, 没有更多了......')
            break
        else:
            print('网络出错了: %s'%status_code)
            break

        
        
        


