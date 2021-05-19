# -*- coding: utf-8 -*-
# $Autor: Nicolás Lista $
# $Revision: 1 $
# $Fecha de Creación: 27/05/2020 $
# Fecha de Modificación: 19/05/2021 $
import sys
import os
from sys import argv
from os import system
from pathlib import Path
from decimal import *

import time
import datetime
import csv
import socket
import re
import configparser
import platform

# Bring routes from config.ini.
from typing import List

from selenium.webdriver.remote.webelement import WebElement
from rpa_robot.rpa_email import *

sistema = platform.system().lower()
config = configparser.ConfigParser()
config.readfp(open(os.path.dirname(os.path.abspath(__file__))+"/../config/config.ini"))



local_data_filename = os.path.dirname(os.path.abspath(__file__))+"/../local_data.ini"
try:
    local_data = configparser.ConfigParser()
    local_data.read_file(open(local_data_filename))
except:
    open(local_data_filename,"+a").write("#COMPLETAR CREDENCIALES")

sep = config["PATHS"]["SEPARATOR"]

# Test start time
starting_point = time.time()
start_time = datetime.datetime.now()
step_time = ""
steps = []
steps_time = []

# Results format
output = {
    "--stdout": False,
    "--csv": False,
    "--steps": False,
    "--headless": False
}

# Create a dictionary with a parameter format string
def crear_dict(string_params):
    string_params += " "
    keys = re.findall('--(.+?)=', string_params)
    dict = {}
    for key in keys:
        dict[key] = re.findall('--'+key+'=([^--]*)', string_params)[0].rstrip()
    return dict

# Run script
def run_script(script, show=False):
    if show: return os.system(script)
    else: return os.system(script+" > /dev/null 2>&1")

# Return the exception details.
def case_exception(e):
    if len(e.args) == 2: finish_test(False, str(e.args[0]).split("\n")[0])
    else: finish_test(False, "TECHNICAL ERROR: " + str(e).split("\n")[0])
    sys.exit()

def current_case():
    matches = re.finditer(r".*\/(.*\/.*\.py)", argv[0], re.MULTILINE)
    for match in matches:
        for groupNum in range(0, len(match.groups())):
            groupNum = groupNum + 1
            return "{group}".format(group = match.group(groupNum)).replace("/", ".")

def print_stack_error(email=True, log_text = ""):
    import traceback
    print("Automatismo procesado con ERROR")




    msg = log_text
    msg += traceback.format_exc()+"\nFecha y hora de ejecucion: "+str(start_time)

    if email:


        files_path = os.path.dirname(os.path.abspath(__file__))+"/../rpa_robot/general_output/"

        Email(
            sender=config["EMAIL"]["SENDER"],
            password=config["EMAIL"]["PASSWORD"],
            to=config["EMAIL"]["RECEIVER"],
            subject="ROBOT RPA: OGS - Error Hospital",
            message=msg,
            files_path=files_path
        )

    else:
        print("Por favor envíe el mensaje de error al área de sistemas")


    traceback.print_exc()


def log(msg):

    print(msg)

    from pathlib import Path
    path_file = Path(os.path.abspath(__file__)).parent

    final_msg = "## Log: " + str(datetime.datetime.now()) + "\n"
    final_msg += msg + "\n"
    final_msg += "#################################" + "\n"

    try:
        file = open(str(path_file) + "/general_output/log.txt",'a')
    except:
        file = open(str(path_file) + "/general_output/log.txt",'w+')

    file.write(final_msg)

    return final_msg



def read_file(filename):
    with open(filename, 'rb') as f:
        file = f.read()
    return file


def str_to_bool(string):
    if string.lower() == 'true':
         return True
    elif string.lower() == 'false':
         return False
    else:
         raise ValueError



def newest_file(path, end=""):
    files = os.listdir(path)
    paths = [os.path.join(path, basename) for basename in files if basename.endswith(end)]
    return max(paths, key=os.path.getctime)

files_csv = {}
def init_csv(filename, con_cabecera = True):

    files_csv[filename] = {
        'con_cabecera': con_cabecera
    }

    try:
        os.remove(filename)
    except:
        None



def make_io_dir(path_file, dir=""):

    if dir == "":
        dir = "output"

    path_dir = str(path_file) + "/" + dir + "/"
    if(os.path.isdir(path_dir) == False):
        os.makedirs(path_dir, exist_ok=True)

    return path_dir



def make_io_dirs(path_file):

    return make_io_dir(path_file, "input"), make_io_dir(path_file, "output")



def write_raw(filename, dict, end="\n"):
    with open(filename,"+a") as file:
        for key, value in dict.items():
            file.write("%s" %(value))
        file.write(end)

def write_csv(filename, dict, begin=False):
    ##### EJEMPLO DE USO
    # operaciones = [
    #     {'clavel1':'valori1', 'claveliDue': 'valurenzo chesccoli'},
    #     {'clavel1':'valori2222', 'claveliDue': 'valurenzo vereneslao'},
    # ]
    #
    # filename = "pepiri.csv"
    # write_csv(filename, operaciones[0], begin = True)
    # write_csv(filename, operaciones[1])
    # write_csv(filename, operaciones[2])
    #
    #######################

    auto_begin = False
    if(os.path.isfile(filename) == False):
        auto_begin = True
        path = "/".join(filename.split("/")[:-1])
        os.makedirs(path, exist_ok=True)


    #DEPRECATED?
    if begin:
        try:
            os.remove(filename)
        except:
            None


    if sistema == "windows": output_file = open(filename, 'a+', newline='')
    else: output_file = open(filename, 'a+')

    output_csv = csv.writer(output_file, delimiter=';')


    def write_keys_dict():
        values = []
        for key, value in dict.items():
            values.append(key)
        output_csv.writerow(values)

    def write_values_dict():
        values = []
        for attr, value in dict.items():
            values.append(value)
        output_csv.writerow(values)



    if auto_begin and files_csv[filename]['con_cabecera']:
        write_keys_dict()

    if not begin:
        write_values_dict()


# def get_index_by_text(driver, texto_buscado:str, lista_elementos:List[WebElement])->int:
#     for element in lista_elementos:
#         if (element.text==texto_buscado):
#             return lista_elementos.index(element)
#     return -1

class Step:
  def __init__(self, description):
    self.description = description
    self.start_time = time.time()
    self.end_time = ""
    self.elapsed_time = ""

  def end(self):
    self.end_time = time.time()
    self.elapsed_time = (self.end_time - self.start_time)
    print(self.description)
    print(" ")

def step(description):
    step = Step(description)
    steps.append(step)
    return step

def step_end():
    steps[-1].end()
    step_time = steps[-1].elapsed_time
    steps_time.append(step_time)


def read_args(defaults={}, sys_args=[]):
    args = defaults
    i=3
    while i < len(sys_args):
        if sys_args[i].startswith("--"):
             args[sys_args[i].replace("--", "")] = sys_args[i+1]
             i+=2
        i+=1
    return args




def update_stats_from_item(stats, item):
    # EJEMPLO DE USO:
    # stats = {
    #     'FECHA ASIGNACIÓN'    : {},
    #     'FECHA PRODUCTIVO'    : {}
    # }



    for key in stats.keys():

        if item[key] == "":
            continue

        if not 'min' in stats[key].keys():
            stats[key]['min'] = item[key]

        if not 'max' in stats[key].keys():
            stats[key]['max'] = item[key]


        stats[key]['min'] = min(item[key], stats[key]['min'])
        stats[key]['max'] = max(item[key], stats[key]['max'])


    return stats


def get_items_from_result(results, must_exists_attr=""):
    items = []

    row = 1
    for item in results:
        row += 1
        item['row'] = row


        try:
            attr = item[must_exists_attr]
            if attr != "":
                items.append(item)
        except:
            if must_exists_attr == "":
                items.append(item)
    return items
