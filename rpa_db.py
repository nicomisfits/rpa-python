# -*- coding: utf-8 -*-
# $Autor: Nicolas Lista $
# $Fecha de Creación: 27/05/2020 $
# Fecha de Modificación: 19/05/2021 $

from rpa_robot.rpa_tools import *
import MySQLdb
import pyodbc


def get_db(clave_ambiente, motor=""):

    #if("ETS_DB" in clave_ambiente):
    def connect_pyodbc():
        return pyodbc.connect(
            DRIVER='{ODBC Driver 17 for SQL Server}',
            SERVER=config[clave_ambiente]["HOST"],
            DATABASE=config[clave_ambiente]["DATABASE"],
            UID=config[clave_ambiente]["USER"],
            PWD=config[clave_ambiente]["PASS"]
        )
    def connect_mysqldb():
        return MySQLdb.connect(
            host=config[clave_ambiente]["HOST"],
            user=config[clave_ambiente]["USER"],
            passwd=config[clave_ambiente]["PASS"],
            db=config[clave_ambiente]["DATABASE"]
        )

    if motor == "":#####################################

        try:
            db = connect_pyodbc()
        except:
            db = connect_mysqldb()

    elif motor == "SQLSERVER":###########################

        db = connect_pyodbc()

    elif motor == "MYSQL":###############################

        db = connect_mysqldb()

    return db


def get_columns(clave_ambiente, table, motor=""):


    if motor == "":
        if("ETS_DB" in clave_ambiente):
            motor = "SQLSERVER"
        elif("PLUS_DB" in clave_ambiente):
            motor = "MYSQL"


    sql=""
    if motor == "SQLSERVER":
        sql="SELECT TOP 1 * FROM " + table
    elif motor == "MYSQL":
        sql="SELECT * FROM " + table + " LIMIT 1"



    db = get_db(clave_ambiente, motor)

    cursor = db.cursor()

    cursor.execute(sql)

    columns = cursor.description

    db.close()
    return columns

def print_columns(clave_ambiente, table, motor=""):
    print(clave_ambiente, table)
    print("================================================")
    columns = get_columns(clave_ambiente, table, motor)

    for column in columns:
        print(column)

def print_result(result):

    for row in result:
        print(row)

def query(clave_ambiente, sql, motor="", cursor=""):


    if cursor=="":
        # TODO: deprecar cuando en todo el proyecto se aclare el motor
        if motor=="":
            if("ETS_DB" in clave_ambiente):
                motor = "SQLSERVER"
            elif("PLUS_DB" in clave_ambiente):
                motor = "MYSQL"

        db = get_db(clave_ambiente, motor)
        cursor = db.cursor()


    cursor.execute(sql)
    
    if not "SELECT" in sql:
        db.commit()

    values = [dict(zip([column[0] for column in cursor.description], row))
             for row in cursor.fetchall()]

    try:
        db.close()
    except:
        None


    return values
