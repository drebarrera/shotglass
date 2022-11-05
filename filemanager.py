import sys
import os
import shutil
import json

def delete_dir(path):
    return shutil.rmtree(path)

def delete_file(path):
    return os.remove(path)

def isdir(path):
    return os.path.isdir(path)

def listdir(path):
    return os.listdir(path)

def pathexists(path):
    return os.path.exists(path)

def getcwd():
    return os.getcwd()

def read_file(path):
    f = open(path, "r")
    read_data = f.read()
    f.close()
    return read_data

def write_to_file(path, data):
    f = open(path,"w")
    f.write(data)
    f.close()

def read_json(path):
    f = open(path)
    data = json.load(f)
    f.close()
    return data

def makedir(path):
    return os.mkdir(path)

def startfile(path):
    return os.startfile(path)

def realpath(path):
    return os.path.realpath(path)