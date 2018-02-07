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
from bs4 import BeautifulSoup
requests.packages.urllib3.disable_warnings()

url = 'https://www.dongmanmanhua.cn/comedy/xin-xinlingdeshengyin/list?title_no=381&page='

# url is referer url
'''
@url : 这里的url是refer的url。也就是每一页具体的漫画
返回创建的文件夹的名字
'''
def create_dir(url):
    o = urlparse(url)
    s = re.match(r'\/comedy\/xin-xinlingdeshengyin\/(.*?)\/viewer',o.path)
    os.mkdir(unquote(s.group(1)))
    return unquote(s.group(1))

# 得到refer的地址，因为一个分页，有好多的refer的地址。所以调用的时候应该用循环，然后返回列表
'''
@url 这里的url参数是refer的url，也是每一页具体的漫画
@page 这里的page是分页的页码数
返回每一页具体漫画的地址列表
'''
def get_referer_address(url,page):
    referers = []
    r = requests.get(url+str(page),verify=False)
    soup = BeautifulSoup(r.text,'html.parser')
    ul = soup.find(id='_listUl')
    all_li = ul.find_all('li')
    for li in all_li:
        referer_url = 'https:'+li.find('a').get('href')
        referers.append(referer_url)

    return referers

'''
@url 这里的url是refer的url
@返回每个图片的实际地址
'''
def get_img(url):
    data_url = []
    r = requests.get(url,verify=False)
    soup = BeautifulSoup(r.text,"html.parser")
    img_list = soup.find(id='_imageList').find_all('img')
    for img in img_list:
        print(img.get('data-url'))
        data_url.append(img.get('data-url'))
    return data_url

'''
@referers 指的是一个分页里面的每个漫画的url
'''
def save_img(referers):
    for referer in referers:
        headers = {
            "Referer":referer
        }
        folder = create_dir(referer)
        data_url = get_img(referer)
        i=0
        for img_url in data_url:
            r =requests.get(img_url,headers=headers,verify=False)
            with open(folder+'/'+str(i)+'.jpg','wb')as f:
                f.write(r.content)
            i+=1

if __name__ == "__main__":
    for num in range(1,23):
        referers = get_referer_address(url,num)
        save_img(referers)


