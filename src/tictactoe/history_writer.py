from os import path, mkdir, getcwd
from json import load, dump, dumps
from datetime import datetime


def jsonNamer(folder_name='ai_history'):
    now = datetime.now()
    timestamp = now.strftime("%m_%d_%Y_%H_%M_%S")
    name = folder_name+"/simulation_history_"+timestamp+".json"
    return name


def jsonDirectory(folder_name='ai_history'):
    cur_directory = getcwd()
    folder_path = path.join(cur_directory, folder_name)
    return folder_path


def jsonWriter(folder_path, json_name):
    if path.exists(folder_path) != True:
        mkdir(folder_path)
    json_object = dumps([])  # create list
    with open(json_name, "w") as outfile:
        outfile.write(json_object)


def jsonDump(simulation_history, json_name):
    with open(json_name) as openjson:
        dictObj = load(openjson)
        dictObj.append(simulation_history)

    with open(json_name, "w") as outfile:
        dump(dictObj, outfile, indent=4)

def jsonActionConverter(folder_name,action_list):
    action_filename = "allActions.json"
    newActionList = {}
    for i in action_list:
        actionName = i.get('action') + ' ' + i.get('action_details')
        newActionList[actionName] = None
    json_object = dumps(actionName)  # create list
    folder_path = jsonDirectory(folder_name)
    if path.exists(folder_path) != True:
        mkdir(folder_path)
    json_object = dumps(newActionList,indent=4)  # create list
    with open(folder_name+'/'+action_filename, "w") as outfile:
        outfile.write(json_object)
   
    

