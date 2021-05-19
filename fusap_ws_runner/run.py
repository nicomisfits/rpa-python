#!/usr/bin/env python3
# -*- coding: utf-8 -*-


import sys
import datetime


from os.path import basename
import os
from pathlib import Path


path_file = Path(os.path.abspath(__file__)).parent
path_group = path_file.parent


path = Path(os.path.abspath(__file__)).parent.parent.parent
sys.path.append(str(path))

path = Path(os.path.abspath('fusap_rpa_test_fwk')).parent.parent
sys.path.append(str(path))



from fusap_rpa_test_fwk.fusap_tools import *
from fusap_rpa_test_fwk.fusap_db import *


from flask import Flask, json, request

import simplejson as json
import requests

api = Flask(__name__)



@api.route('/run', methods=['GET'])
def run_script():
    script = "/".join(request.args.get('script').split("-"))


    args = ""
    for key in request.args.keys():
        args += "--" + key + " " + request.args[key] + " "


    import subprocess


    result = ""
    try:
        result = str(subprocess.check_output(
            script + "/run.py " + args,
            stderr=subprocess.STDOUT,
            shell=True
        ))

    except:
        result = str(read_file(str(path_group) + "/general_output/log.txt"))


    result = result.replace("b'", "")
    result = result.replace('b"', '')
    result = result.replace("\\n'", "")
    result = result.replace('\\n"', '')
    result = result.replace("\\n", "<br/>")
    result = result.replace("\\xc3\\xb3", "ó")
    result = result.replace("\\xc3\\xa1", "á")
    result += "<img scr='" + str(path_group) + "/general_output/error.png" + "' />"


    filename = str(path_file)+"/res/base.html"
    file = open(filename, mode='r')
    content = file.read()

    html = content
    html = html.replace('{% OUTPUT %}', result)


    return html



if __name__ == '__main__':

    from waitress import serve
    serve(api, host="0.0.0.0", port=8090)
