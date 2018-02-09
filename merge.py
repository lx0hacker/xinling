#-*-coding：utf-8-*-
import os.path
import os
from PIL import Image
import shutil

def image_merge(images,filename):
    total_height=0
    for img in images:
        img = Image.open(img)
        width,height = img.size
        total_height += height
    new_image = Image.new('RGB',(width,total_height),255)
    x=y=0
    for img in images:
        img = Image.open(img)
        width,height = img.size
        new_image.paste(img,(x,y))
        y+=height
    new_image.save('../'+filename+'.png')


if __name__ == "__main__":

    parent_folder = input('请输入你要整合的漫画的文件夹名：')
    os.chdir(parent_folder)
    all_folder = [x for x in os.listdir('.') if os.path.isdir(x)]

    for sub_folder in all_folder:
        os.chdir(sub_folder)
        print('现在位于：'+os.getcwd())
        all_jpg_file = [x for x in os.listdir('.') if os.path.isfile(x) and os.path.splitext(x)[1]=='.jpg']
        a = []
        for num in range(len(all_jpg_file)-1):
            a.append(str(num)+'.jpg')
        print('Start to merge')
        image_merge(a,sub_folder)
        print(sub_folder+" Done....")
        os.chdir('..')
        print("开始删除文件夹.......删除",sub_folder)
        shutil.rmtree(sub_folder)
    os.chdir('..')

