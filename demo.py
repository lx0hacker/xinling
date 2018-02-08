import os.path
import os







all_folder = [x for x in os.listdir('.') if os.path.isdir(x)]

for folder in all_folder:
    if folder!='.git' and folder!='venv':
        os.chdir(folder)
        print(os.getcwd())
        all_sub_folder = [x for x in os.listdir('.') if os.path.isdir(x)]
        print('total:',len(all_sub_folder))
        for sub_folder in all_sub_folder:
            os.chdir(sub_folder)
            all_jpg_file = [x for x in os.listdir('.') if os.path.isfile(x) and os.path.splitext(x)[1]=='.jpg']
            #print(len(e),os.path.basename(os.getcwd()))
            # 这里可以传入一个列表做为参数
            os.chdir('..')
            
        
        os.chdir('..')
