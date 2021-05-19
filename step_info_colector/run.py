#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import sys
import os
from pathlib import Path

path_file = Path(os.path.abspath(__file__)).parent
path_group = path_file.parent
path_root = path_group.parent
sys.path.append(str(path_root))

from rpa_robot.rpa_web import *

try:
    for file in listdir(str(path_group)+"/general_output/"):
        if "keep" not in file:
            os.remove(str(path_group)+"/general_output/"+str(file))

    print("ROBOT RPA")
    print("Ejecución:", datetime.datetime.now())
    print("")
    print("Ingresar la URL de la web a capturar:")

    url = input("")

    web = Web(url)

    path_file = Path(os.path.abspath(__file__)).parent

    counter = 0
    while True:
        counter = counter + 1
        if counter == 1:
            web.minimize_all_windows()
        val = input("[ENTER = conseguir html + png] / [F = fin del proceso]")
        if web.open_windows() > 1:
            web.change_window(web.open_windows()-1)
        else:
            web.change_window(0)

        if not val: web.latch_web_status("/general_output/step"+str(counter))
        elif "f" in val.lower(): break
        else: print("No existe la opcion: "+str(val)+". REINTENTAR!."); counter = counter - 1;continue

    # Email(config["EMAIL"]["SENDER"], config["EMAIL"]["PASSWORD"], config["EMAIL"]["RECEIVER"], "Archivos recuperados de Step_Information_Collector.","archivos png y html adjuntos.", str(path_group)+"/general_output/")
except Exception as e:
    print_stack_error()

finally:
    web.driver.close()
