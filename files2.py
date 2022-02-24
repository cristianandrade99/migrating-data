import sys
import os
import datetime
import shutil
import json

instructions_dir='./create_folders.json'
work_folder = 'D:/test/'
months = ['Enero','Febrero','Marzo','Abril','Mayo','Junio','Julio','Agosto','Septiembre','Octubre','Noviembre','Diciembre']

def load_data(source):
    with open(source,encoding='utf8') as file:
        data = json.load(file)
        return data

def list_dirs(path):
    dirs = os.listdir(path)
    return dirs

def create_directory(directory):
    try:
        os.makedirs(directory)
    except:
        pass

def run():
    instructions=load_data(instructions_dir)
    year=instructions['year']
    groups=instructions['groups']
    current_path = os.path.join(work_folder,year)
    for group in groups:
        start=group['start']
        end=group['end']
        title=group['title']
        paths=list_dirs(current_path)
        if(len(paths)>0):
            month=datetime.datetime.fromtimestamp(os.path.getmtime(current_path)).strftime('%m')
            month_label = months[int(month)-1]
            new_path = os.path.join(current_path,f'{month} - {month_label} - {title}')
            for path in paths:
                belongs = start in path or end in path or (path>=start and path <= end)
                if belongs:
                    new_file_path=os.path.join(new_path,path)
                    print(new_file_path)

run()

# months = ['Enero','Febrero','Marzo','Abril','Mayo','Junio','Julio','Agosto','Septiembre','Octubre','Noviembre','Diciembre']
# [_,path,start,end,name]=sys.argv

# def print_array(array):
#     for item in array:
#         print(item)

# def list_dirs():
#     dirs=os.listdir(path)
#     return dirs

# def get_dirs_to_move(dirs):
#     dirs_to=[]
#     month = ''
#     month_label=''
#     if(len(dirs)>0):
#         current_path = os.path.join(path,dirs[0])
#         month=datetime.datetime.fromtimestamp(os.path.getmtime(current_path)).strftime('%m')
#         month_label = months[int(month)-1]
#     for dir_item in dirs:
#         current_path = os.path.join(path,dir_item)
#         if os.path.isfile(current_path):
#             modification = datetime.datetime.fromtimestamp(os.path.getmtime(current_path))
#             day = int(modification.strftime('%d'))
#             if day >= int(start) and day <= int(end):
#                 dirs_to.append(current_path)
#     return dirs_to,month,month_label

# def move(dirst_to_move,month,month_label):
#     for current_path in dirst_to_move:
#         directory=os.path.join(path,f'{month} - {month_label} - {name}')
#         try:
#             os.makedirs(directory)
#         except:
#             pass
#         shutil.move(current_path,directory)

# dirs = list_dirs()
# dirst_to_move,month,month_label = get_dirs_to_move(dirs)
# move(dirst_to_move,month,month_label)