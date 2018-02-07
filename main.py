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
'''
def get_referer_address(start,total):
    referer = []
    for page in range(start,total):
        r = requests.get('https://www.dongmanmanhua.cn/comedy/xin-xinlingdeshengyin/list?title_no=381&page='+str(page),verify=False)
        soup = BeautifulSoup(r.text,'html.parser')
        ul = soup.find(id='_listUl')
        all_li = ul.find_all('li')
        for li in all_li:
            #print(li.find('a').get('href'))
            with open('test.txt','a',encoding='utf-8')as f:
                f.write('https:'+li.find('a').get('href')+'\n')

            referer_url = 'https:'+li.find('a').get('href')
            referer.append(referer_url)
    return referer
'''
url = 'https://www.dongmanmanhua.cn/comedy/xin-xinlingdeshengyin/list?title_no=381&page='

# url is referer url
'''
@url : 这里的url是refer的url。也就是每一页具体的漫画
'''
def create_dir(url):
    o = urlparse(url)
    #print(o.path)
    s = re.match(r'\/comedy\/xin-xinlingdeshengyin\/(.*?)\/viewer',o.path)
    os.mkdir(unquote(s.group(1)))
    return unquote(s.group(1))

# 得到refer的地址，因为一个分页，有好多的refer的地址。所以调用的时候应该用循环，然后返回列表
'''
@url 这里的url参数是refer的url，也是每一页具体的漫画
@page 这里的page是分页的页码数
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

# 得到单个refer的地址，但是图片地址是多个
'''
@url 这里的url是refer的url，
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

# 开始保存图片
'''

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




#get_referer_address(1,23)

