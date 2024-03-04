#!/usr/bin/env python3

# @todo: make it use a specific python version, do not run if not installed
# perhaps poetry already does that? which python (inside the venv) gives:
# /home/souto/.cache/pypoetry/virtualenvs/py-update-tmx-h7xCdFbW-py3.11/bin/python

import inspect
import sys, os
import yaml
import shutil
import fileinput
from datetime import datetime
import argparse
from lxml import etree
import pandas as pd
import numpy as np
from rich import print
from dataclasses import dataclass
from html import escape, unescape

# args

# output = "edit"
output = "copy"
keep_unedited = "yes"

# functions

def indent_nodes(entries):
    return [etree.indent(entry, space='    ', level=3) for entry in entries]


def convert_dicts_to_dataclasses(data):
    """ Convert dictionary to dataclass for easy manipulation in dot notation """

    @dataclass
    class Request:
        file:   str
        key:    str
        source: str
        target: str
        update: str

    return [Request(**entry_dict) for entry_dict in data]


def extract_requests(xls_fpath):
    """ Extract update requests from Excel config """

    df = pd.read_excel(xls_fpath, sheet_name="updates").replace(np.nan, None)
    entries = df.to_dict('records') # entires is a list of dicts
    return convert_dicts_to_dataclasses(entries)


def update_change_props():
    pass


def remove_all_tus(tmx_fpath):
    # make template for output
    doc = etree.parse(tmx_fpath, parser)
    for tu in doc.xpath("//tu"):
        tu.getparent().remove(tu)

    doc.write(tmx_fpath, encoding='UTF-8', pretty_print=True, standalone=True)
    return True


def add_edited_entries(entries, tmx_fpath):
    doc = etree.parse(tmx_fpath, parser)
    body = doc.xpath("//body")[0]
    for entry in entries:
        tu = etree.Element("tu")
        tu = entry
        body.append(tu)
    
    doc.write(tmx_fpath, encoding='UTF-8', pretty_print=True, standalone=True)
        

def convert_conditions_to_xpath_output(update_request):
        filters = []
        print(filters)
        if update_request.key:
            filters.append(f"[prop[@type='id'][text()='{update_request.key}']]")
        if update_request.file:
            filters.append(f"[prop[@type='file'][text()='{update_request.file}']]")
        if update_request.source:
            filters.append(f"[tuv[@lang='{source_lang}'][seg[text()='{update_request.source}']]]")
        if update_request.target:
            filters.append(f"[tuv[@lang='{target_lang}'][seg[.='{update_request.target}']]]")
        expr = ''.join(filters)
        entries = doc.xpath(f"//tu{expr}/tuv[@lang='{target_lang}']/seg")
        tus = doc.xpath(f"//tu{expr}")
        return [entries, tus]


# input must be a file path
tmx_fpath="/home/souto/Sync/Dev/py-update-tmx/files/project_save.tmx"
xls_fpath="/home/souto/Sync/Dev/py-update-tmx/data/change-requests.xlsx"
tmx_fpath2="/home/souto/Sync/Dev/py-update-tmx/files/project_save2.tmx"
tmx_fpath3="/home/souto/Sync/Dev/py-update-tmx/files/project_save3.tmx"

print(f"{xls_fpath=}")
print(f"{tmx_fpath=}")



# <repository type="git" url="&DOMAIN;/pisa_2025ft_translation_common.git">
#   <mapping local="omegat/filters.xml" repository="config/filters.xml"/>

init_dpath = os.getcwd()

if not os.path.exists(tmx_fpath) or not os.path.exists(xls_fpath):
    # some exit message here
    sys.exit()

requests = extract_requests(xls_fpath)
# for request in requests:
#     print(request)

parser = etree.XMLParser(resolve_entities=False)
doc = etree.parse(tmx_fpath, parser)


for request in requests:
    # key_prop =  request.key
    # file_prop =  request.file
    # source_text = request.source
    # orig_target_text = request.target
    edit_target_text = request.update

    conditions = [request.key, request.file, request.source, request.target]

    print(request)

    source_lang = "en"
    target_lang = "de-DE"

    if edit_target_text == None:
        # some exit message
        sys.exit()

    entries, tus = convert_conditions_to_xpath_output(request)
    # entries = doc.xpath(f"//tu{filters}/tuv[@lang='{target_lang}']/seg")
    # tus = doc.xpath(f"//tu{filters}")

    for entry in entries:
        print(f"{entry.text=}")
        entry.text = edit_target_text # update!
        print(f"{entry.text=}")


# updated_tus, updated_entries = edits*

doc.write(tmx_fpath2, encoding='UTF-8', pretty_print=True, standalone=True)


# entries = indent_nodes(entries)

for tu in tus:
    print(f"{tu=}")
    for tuv in tu:
        print(f"{tuv=}")

remove_all_tus(tmx_fpath3)
add_edited_entries(tus, tmx_fpath3)


# @todo: check that expected worksheets are found in the excel
# @todo: check that expected headers are found in the excel
# @todo: check that source_text is provided if key and/or file props are provided
# @todo: check if ods or xlsx, and use library accordingly
# @todo: validate TMX ?
# @todo: get target_lang from config sheet with common data