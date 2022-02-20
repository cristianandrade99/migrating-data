import os
import sys
import datetime
import shutil

source = sys.argv[1]
destiny = 'D:/test'
image_video_extensions=['.jpg','.jpeg','.JPG','.gif','.png','.AVI','.wmv','.MOV','.BMP','.PNG','.mp4','.CR2','.3gp']
months = ['Enero','Febrero','Marzo','Abril','Mayo','Junio','Julio','Agosto','Septiembre','Octubre','Noviembre','Diciembre']

def print_array(array):
    for item in array:
        print(item)

def get_all_file_paths ():
    paths=[];
    for root, _, files in os.walk(source):
        for file in files:
            path = os.path.join(root,file)
            _,ext = os.path.splitext(path)
            creation = datetime.datetime.fromtimestamp(os.path.getctime(path))
            modification = datetime.datetime.fromtimestamp(os.path.getmtime(path))
            #creation_format = creation.strftime('%Y-%m')
            key = modification.strftime('%Y%m%d')
            year = modification.strftime('%Y')
            month = modification.strftime('%m')
            day = modification.strftime('%d')
            paths.append([path,ext,key,year,month,day])
    return paths

def get_all_different_extensions(paths):
    extensions=[]
    for current_path in paths:
        ext=current_path[1]
        if ext not in extensions:
            extensions.append(ext)
    return extensions

def get_image_video_paths(paths):
    image_video_paths=[]
    for current_path in paths:
        ext=current_path[1]
        if ext in image_video_extensions:
            image_video_paths.append(current_path)
    return image_video_paths

def group_by_year_month(paths):
    groups={}
    for current_path in paths:
        key = current_path[2]
        year = current_path[3]
        month = current_path[4]
        day = current_path[5]
        if key not in groups:
            groups[key]={'year':year,'month':month,'day':day,'paths':[current_path]}
        else:
            groups[key]['paths'].append(current_path)
    return groups

paths = get_all_file_paths()
extensions = get_all_different_extensions(paths)
image_video_paths = get_image_video_paths(paths)
groups = group_by_year_month(image_video_paths)

for key in groups:
    if('201908' in key):
        item = groups[key]
        year = item['year']
        month = item['month']
        day = item['day']
        directory=os.path.join(destiny,year)
        try:
            os.makedirs(directory)
        except:
            pass
        print(f'{year}/{month}')
        for current_path in item['paths']:
            path = current_path[0]
            print(path)
            shutil.copy2(path,directory)