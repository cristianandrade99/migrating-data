import os
import sys
import datetime
import shutil
import json
import time
from pick import pick
from tqdm import tqdm
from itertools import groupby

prepare='prepare'
migrate='migrate'
prepare_files='prepare_files'
migrate_files='migrate_files'
validation='validation'
exit_process = 'Salir'
source = sys.argv[1]
action = sys.argv[2]
destiny = 'D:/Fotos y Videos'
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

def get_all_file_paths(source_param):
    paths=[];
    for root, _, files in os.walk(source_param):
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

def get_all_files_names(file_paths):
    return [ [path[0],os.path.basename(path[0]),path[1]] for path in file_paths]

def all_equal(iterable):
    g = groupby(iterable)
    return next(g, True) and not next(g, False)

def run_validation(all_files_names_source,all_files_names_destiny):
    # destinies_names = [ item[1] for item in  all_files_names_destiny]
    # results=[];
    # tqdm_sources=tqdm(all_files_names_source)
    # for source in tqdm_sources:
    #     if source[1] not in destinies_names:
    #        results.append(source[0]) 
    # save_json(results,'./validation.json')
    # save_json(destinies_names,'./destinies_names.json')

    # extensions={}
    # tqdm_sources=tqdm(all_files_names_source)
    # for source in tqdm_sources:
    #     ext=source[2]
    #     if ext not in extensions:
    #         extensions[ext]={'source':0,'destiny':0}
    #     else:
    #         extensions[ext]['source']+=1
    # tqdm_destinies=tqdm(all_files_names_destiny)
    # for destiny in tqdm_destinies:
    #     ext=destiny[2]
    #     if ext not in extensions:
    #         extensions[ext]={'source':0,'destiny':0}
    #     else:
    #         extensions[ext]['destiny']+=1
    # save_json(extensions,'./validation.json')
    
    # results=[]
    # tqdm_sources=tqdm(all_files_names_source)
    # for item in tqdm_sources:
    #     current_path=item[0]
    #     ext=item[2]
    #     if ext in image_video_extensions and r'C:\\Users\\Games\\Documents\\Migracion\\Eduar\\Instaladores' not in current_path:
    #         paths=[]
    #         for item2 in all_files_names_source:
    #             if item[1] == item2[1]:
    #                 paths.append(item2[0])
    #         if len(paths)>1:
    #             data=[]
    #             sizes=[]
    #             for path in paths:
    #                 size=os.path.getsize(path)
    #                 sizes.append(size)
    #                 data.append([path,size])
    #             if not all_equal(sizes):
    #                 results.append(data)
    # save_json(results,'./validation.json')

    # data = load_data('./validation.json')
    # new_data=[]
    # for repeateds in data:
    #     if 'Eduar\\Instaladores' not in repeateds[0][0]:
    #         new_data.append(repeateds)
    # save_json(new_data,'./validation.json')

    # data = load_data('./validation.json')
    # last_step_data=[]
    # for repeateds in tqdm(data):
    #     for i in range(len(repeateds)):
    #         old_path = repeateds[i][0]
    #         year = datetime.datetime.fromtimestamp(os.path.getmtime(old_path)).strftime('%Y')
    #         base_name=os.path.basename(old_path)
    #         file_name,ext = os.path.splitext(base_name)
    #         new_path=os.path.join(destiny,year,f'{file_name}_{i}{ext}')
    #         last_step_data.append([old_path,new_path])
    # save_json(last_step_data,'./last_step_data.json')

    last_step_data = load_data('./last_step_data.json')
    for item in tqdm(last_step_data):
        source = item[0]
        destiny = item[1]
        shutil.copy2(source,destiny)


# Image and videos
if action==prepare:
    all_file_paths=get_all_file_paths(source)
    image_video_paths,_=get_image_video_paths(all_file_paths)
    group_by_date=get_group_by_date(image_video_paths)
    array=get_list(group_by_date)
    register_groups(array,json_destiny,progress_destiny)
elif action==migrate:
    migrate_data()

# Other files
elif action==prepare_files:
    all_file_paths=get_all_file_paths(source)
    _,other_paths=get_image_video_paths(all_file_paths)
    group_by_date=get_group_by_date(other_paths)
    array=get_list(group_by_date)
    register_groups(array,'./paths-files.json','./progress-files.json')
elif action==migrate_files:
    migrate_data_files()

# Validation
elif action==validation:
    all_file_paths_source=get_all_file_paths(r'C:\Users\Games\Documents\Migracion')
    all_file_paths_destiny=get_all_file_paths(r'D:/')
    all_files_names_source=get_all_files_names(all_file_paths_source)
    all_files_names_destiny=get_all_files_names(all_file_paths_destiny)
    run_validation(all_files_names_source,all_files_names_destiny)
# cd C:\Users\Games\Downloads\migration-data 
# python files.py C:\Users\Games\Documents\Migracion migrate

# TO DO
# - Migrate files that are not images nor videos (maintaint path structure)