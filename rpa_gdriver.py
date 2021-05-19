#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# $Autor: Nicolás Lista $
# $Revision: 1 $
# $Fecha de Creación: 27/05/2020 $
# Fecha de Modificación: 19/05/2021 $

import sys
import os
import traceback
from pathlib import Path
import os.path as path




from rpa_robot.rpa_tools import *
import gspread
from oauth2client.service_account import ServiceAccountCredentials

output.update({"--gspread": False})

def open_sheet(sheetName):
    scope = ['https://spreadsheets.google.com/feeds', 'https://www.googleapis.com/auth/drive']
    credentials = ServiceAccountCredentials.from_json_keyfile_name(config["PATHS"]["QUICKSTART"],scope)
    gc = gspread.authorize(credentials)
    wks = gc.open_by_url(config["URLS"]["SHEET"])
    ws = wks.worksheet(sheetName)
    return(ws)

def getInfo(cell, ws):
    cellContent = ws.acell(cell).value
    return(cellContent)

def next_available_row(ws):
    str_list = list(filter(None, ws.col_values(1)))
    return str(len(str_list)+1)


class Gsheet:
    def __init__(self, url, sheetName=""):

        path_rpa_robot = Path(os.path.abspath(__file__)).parent
        path_rpa = path_rpa_robot.parent
        sys.path.append(str(path_rpa))


        scope = ['https://spreadsheets.google.com/feeds', 'https://www.googleapis.com/auth/drive']
        credentials = ServiceAccountCredentials.from_json_keyfile_name(str(path_rpa) + '/' + config["PATHS"]["QUICKSTART"],scope)
        gc = gspread.authorize(credentials)
        self.planilla = gc.open_by_url(url)

        if sheetName=="":
            self.sheet = self.planilla.worksheets()[0]
        else:
            self.set_default_worksheet(sheetName)
    def getColumnName(self, n):

        # initialize output String as empty
        res = ""

        while n > 0:

            # find index of next letter and concatenate the letter
            # to the solution

            # Here index 0 corresponds to 'A' and 25 corresponds to 'Z'
            index = (n - 1) % 26
            res += chr(index + ord('A'))
            n = (n - 1) // 26

        return res[::-1]


    def set_default_worksheet(self, sheetName):

        self.sheet = self.planilla.worksheet(sheetName)
        return self.sheet

    def get_worksheet(self, sheetName):
        #No la retilizo por ahora porque me parece que se deprecaría
        return self.planilla.worksheet(sheetName)


    def get_results(self):
        return self.sheet.get_all_records()


    def get_cell_info(self, cell):
        cellContent = self.sheet.acell(cell).value
        return(cellContent)

    def next_available_row(self):
        str_list = list(filter(None, self.sheet.col_values(1)))
        return str(len(str_list)+1)
