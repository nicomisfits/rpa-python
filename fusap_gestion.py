# -*- coding: utf-8 -*-
# © FUSAP SRL
# $Autor: Nicolás Lista $
# $Revision: 1 $
# $Fecha de Creación: 20/08/2020 $
# Fecha de Modificación: 24/09/2020 $
import sys
import os
from os import listdir
from os.path import isfile, isdir
from fusap_rpa_test_fwk.fusap_tools import *




def get_week(fecha = "", fecha_inicio = "2020-03-01"):


    if fecha == "":
        fecha_datetime = datetime.datetime.now()
    else:
        fecha_datetime = datetime.datetime(
            int(fecha.split("-")[0]),
            int(fecha.split("-")[1]),
            int(fecha.split("-")[2])
        )

    fecha_inicio_datetime = datetime.datetime(
        int(fecha_inicio.split("-")[0]),
        int(fecha_inicio.split("-")[1]),
        int(fecha_inicio.split("-")[2])
    )



    # week = ((fecha_datetime.year - 2020) * 53) + fecha_datetime.isocalendar()[1]
    #
    # #le resto las semanas que tardamos en arrancar del año 2020
    # week -= 10

    return int((fecha_datetime - fecha_inicio_datetime).days / 7)


def get_sprint(fecha = ""):


    week = get_week(fecha)

    import math

    sprint = math.ceil(week / 2)

    return sprint
