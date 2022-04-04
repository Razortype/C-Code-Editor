import os
import subprocess
from datetime import datetime
import pyperclip
from tkinter import filedialog

all_folder_directories = []
all_file_directories = []

def get_data(req=None,filedir=r"DATA\settings.txt"):
    with open(filedir,"r") as set_file:
        data = set_file.read()
    
    data_dict = {}
    for row in data.split("\n"):
        key,val = row.split('$:=')
        if "items" in key:
            data_dict[key] = val.split("#")
        else:
            data_dict[key] = val

    if req=="IP":
        if data_dict.get("init_path"):
            return data_dict.get("init_path")
        else:
            init_dir = filedialog.askdirectory()
            save_data(init_dir, *list(data_dict.values())[1:])
            return init_dir
    elif req=="PI":
        return data_dict.get("prop_items")
    elif req=="RI":
        return data_dict.get("refill_items")
    elif req=="LV":
        return data_dict.get("log_val")
    elif req=="LP":
        return data_dict.get("log_path")
    else:
        return data_dict

def save_data(init_path,prop_items,refill_items,log_val,log_path,filedir="DATA/settings.txt"):
    prop_items = "#".join(prop_items)
    refill_items = "#".join(refill_items)
    data = []
    data.append(f"init_path$:={init_path}")
    data.append(f"prop_items$:={prop_items}")
    data.append(f"refill_items$:={refill_items}")
    data.append(f"log_val$:={log_val}")
    data.append(f"log_path$:={log_path}")
    with open(filedir,"w") as datafile:
        datafile.write("\n".join(data))


def get_init_path():
    init_path = get_data("IP")
    return init_path

def get_log_path():
    currently = r'C:\Users\RAZORTYPE\Desktop\cLessonFolder\LOG'
    return currently

def get_folders(thedir):
    folder_lst = [folder for folder in os.listdir(thedir) if os.path.isdir(os.path.join(thedir, folder))]
    return folder_lst

def get_files(thedir):
    file_lst = [file for file in os.listdir(thedir) if os.path.isfile(os.path.join(thedir, file))]
    return file_lst

def get_all_folder_directory(thedir):
    folder_lst = get_folders(thedir)
    for folder in folder_lst:
        new_directory = thedir + "\\" + folder
        all_folder_directories.append(new_directory)
        get_all_folder_directory(new_directory)

def get_all_file_directory(dir_lst):
    for dirr in dir_lst:
        files = get_files(dirr)
        for file in files:
            if file != os.path.basename(__file__):
                new_directory = dirr + "\\" + file
                all_file_directories.append(new_directory)

def search_files(path):
    global all_file_directories, all_folder_directories
    
    all_folder_directories.append(path)

    get_all_folder_directory(path)
    get_all_file_directory(all_folder_directories)

    files = all_file_directories

    all_file_directories = []
    all_folder_directories = []

    return files

def check_exists(path):
    return os.path.isdir(path)

def get_file_data(thedir):
    folder_name = os.path.basename(os.path.dirname(thedir))
    file_name = os.path.basename(thedir)
    file_modified_time = datetime.fromtimestamp(os.path.getmtime(thedir)).strftime('%H:%M - %d/%m/%Y')
    comp_before = file_name.replace(".c",".exe") in os.listdir(os.path.dirname(thedir))
    try:
        last_compiled_time = datetime.fromtimestamp(os.path.getmtime(thedir.replace(".c",".exe"))).strftime('%H:%M - %d/%m/%Y')
    except Exception:
        last_compiled_time = None

    return [folder_name, file_name, file_modified_time, comp_before, last_compiled_time]

def compile_handle(command):
    result = subprocess.Popen(command, shell = True,stdout=subprocess.PIPE,stderr=subprocess.PIPE)
    _,output=result.communicate()
    output = output.decode("utf-8").split("error: ")[-1]
    return output

def run_compile_both(thedir, state):
    pfile = thedir.split(".")[0]
    exedir = pfile+".exe"

    run_command = f"cmd /k {exedir}"
    compile_command = f"gcc {thedir} -o {exedir}"

    if state == "RUN":
        os.system(run_command)
    elif state == "COMPILE":
        output = compile_handle(compile_command)
        return output
    elif state == "BOTH":
        output = compile_handle(compile_command)
        if output:
            return output
        else:
            os.system(run_command)

def compile_file(cdir):
    exedir = cdir.replace(".c",".exe")
    os.system(f"gcc {cdir} -o {exedir}")

def save_source_code(filepath, data):
    with open(filepath, "w") as source:
        source.write(data)

def copy_text(text):
    pyperclip.copy(text)

def check_run_suit(cdir):
    exedir = cdir.replace(".c",".exe")
    return os.path.getmtime(cdir) <= os.path.getmtime(exedir)

def open_folder_dir(path):
    abspath = os.path.dirname(os.path.abspath(path))
    clean_folder(abspath)
    os.system("start "+abspath)

def clean_folder(abspath):
    cfiles = []
    exefiles = []
    for i in os.listdir(abspath):
        if i.endswith(".c"):
            cfiles.append(i.split(".")[0])
        if i.endswith(".exe"):
            exefiles.append(i.split(".")[0])

    not_match = list(set(exefiles).difference(cfiles))
    if not_match:
        for exe in not_match:
            os.remove(abspath+"//"+exe+".exe")