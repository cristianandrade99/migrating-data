import os
import sys
import datetime
import shutil
import json
import time
from pick import pick
from tqdm import tqdm

prepare='prepare'
migrate='migrate'
prepare_files='prepare_files'
migrate_files='migrate_files'
exit_process = 'Salir'
source = sys.argv[1]
action = sys.argv[2]
destiny = 'D:\Fotos y Videos'
json_destiny='./paths.json'
progress_destiny='./progress.json'
image_video_extensions=[
'.jpg',
'.png',
'.jpeg',
'.mp4',
'.JPG',
'.gif',
'.MOV',
'.m4a',
'.3gp',
'.JPG2468',
'.AVI',
'.wmv',
'.BMP',
'.NEF',
'.PNG',
'.CR2',
'.avi'
]
months = ['Enero','Febrero','Marzo','Abril','Mayo','Junio','Julio','Agosto','Septiembre','Octubre','Noviembre','Diciembre']

def print_array(array):
    for item in array:
        print(item)

def save_json(data,directory):
    json_object = json.dumps(data,ensure_ascii=False,indent=2)
    with open(directory, 'w', encoding='utf8') as outfile:
        outfile.write(json_object)

def get_date_data(key):
    year=key[0:4]
    month=key[5:7]
    return year,month

def get_all_file_paths():
    paths=[];
    for root, _, files in os.walk(source):
        for file in files:
            path = os.path.join(root,file)
            _,ext = os.path.splitext(path)
            modification = datetime.datetime.fromtimestamp(os.path.getmtime(path))
            key = modification.strftime('%Y-%m')
            paths.append([path,ext,key])
    return paths

def get_all_different_extensions(paths):
    extensions=[]
    for current_path in paths:
        _,ext,_=current_path
        if ext not in extensions:
            extensions.append(ext)
    return extensions

def get_image_video_paths(paths):
    image_video_paths=[]
    other_paths=[]
    for current_path in paths:
        _,ext,_=current_path
        if ext in image_video_extensions:
            image_video_paths.append(current_path)
        else:
            other_paths.append(current_path)
    return image_video_paths,other_paths

def get_group_by_date(paths):
    groups={}
    for current_path in paths:
        path,_,key=current_path
        if key not in groups:
            groups[key]=[path]
        else:
            groups[key].append(path)
    return groups

def get_list(groups):
    list_group=[]
    for key,value in groups.items():
        list_group.append({'key':key,'paths':value})
    list_group.sort(key=lambda group: group.get('key'))
    return list_group

def register_groups(array,json_destiny_param,progress_destiny_param):
    save_json(array,json_destiny_param)
    progress=[]
    for group in array:
        key = group['key']
        progress.append({'key':key,'migrated':False})
    save_json(progress,progress_destiny_param)

def load_data(source):
    with open(source,encoding='utf8') as file:
        data = json.load(file)
        return data

def find_index(array,value):
    index=-1
    for idx,item in enumerate(array):
        if item['key']==value:
            index=idx
            break
    return index

def save_progess(progress,new_index,progress_destiny_param):
    progress[new_index]['migrated']=True
    save_json(progress,progress_destiny_param)

def create_directory(directory):
    try:
        os.makedirs(directory)
    except:
        pass

def migrate_data():
    data = load_data(json_destiny)
    progress = load_data(progress_destiny)
    title = 'Escoge hasta qué fecha migrar'
    continue_app=True
    while(continue_app):
        options = [item['key'] for item in progress if item['migrated'] == False]+[exit_process]
        selected_option,_ = pick(options, title)
        if(selected_option==exit_process):
            continue_app=False
        else:
            for current_option in options:
                new_index = find_index(progress,current_option)
                if(new_index!=-1):
                    paths = data[new_index]['paths']
                    year,_=get_date_data(current_option)
                    directory=os.path.join(destiny,year)
                    create_directory(directory)
                    tqdm_paths=tqdm(paths)
                    tqdm_paths.set_description(current_option)
                    for path in tqdm_paths:
                        shutil.copy2(path,directory)
                    save_progess(progress,new_index,progress_destiny)
                if current_option==selected_option:
                    break   

def migrate_data_files():
    data = load_data('./paths-files.json')
    progress = load_data('./progress-files.json')
    title = 'Escoge hasta qué fecha migrar'
    continue_app=True
    while(continue_app):
        options = [item['key'] for item in progress if item['migrated'] == False]+[exit_process]
        selected_option,_ = pick(options, title)
        if(selected_option==exit_process):
            continue_app=False
        else:
            for current_option in options:
                new_index = find_index(progress,current_option)
                if(new_index!=-1):
                    paths = data[new_index]['paths']
                    tqdm_paths=tqdm(paths)
                    tqdm_paths.set_description(current_option)
                    for path in tqdm_paths:
                        removed_prefix=os.path.relpath(path, r'C:\Users\Games\Documents\Migracion')
                        destiny_directory=os.path.join('D:/Archivos',removed_prefix)
                        create_directory(destiny_directory)
                        shutil.copy2(path,destiny_directory)
                    save_progess(progress,new_index,'./progress-files.json')
                if current_option==selected_option:
                    break

# Image and videos
if action==prepare:
    all_file_paths=get_all_file_paths()
    image_video_paths,_=get_image_video_paths(all_file_paths)
    group_by_date=get_group_by_date(image_video_paths)
    array=get_list(group_by_date)
    register_groups(array,json_destiny,progress_destiny)
elif action==migrate:
    migrate_data()

# Other files
elif action==prepare_files:
    all_file_paths=get_all_file_paths()
    _,other_paths=get_image_video_paths(all_file_paths)
    group_by_date=get_group_by_date(other_paths)
    array=get_list(group_by_date)
    register_groups(array,'./paths-files.json','./progress-files.json')
elif action==migrate_files:
    migrate_data_files()

# cd C:\Users\Games\Downloads\migration-data 
# python files.py C:\Users\Games\Documents\Migracion migrate

# TO DO
# - Migrate files that are not images nor videos (maintaint path structure)