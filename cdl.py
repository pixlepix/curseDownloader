#!/usr/bin/env python

import argparse
import json
import os
import requests
import shutil
from pathlib import Path
from threading import Thread
from tkinter import *
from tkinter import ttk, filedialog
import urllib


minecraftPath=""

parser = argparse.ArgumentParser(description="Download Curse modpack mods")
#parser.add_argument("--manifest", help="manifest.json file from unzipped pack")
#parser.add_argument("--nogui", dest="gui", action="store_false", help="Do not use gui to to select manifest")

parser.add_argument('id', metavar='id', type=int,
                   help='id of mod to be downloaded')
parser.add_argument('fileId', metavar='fid', type=int,
                   help='id of file to be downloaded')
args, unknown = parser.parse_known_args()


def doDownload(id, fileId):
    sess = requests.session()
    projectResponse = sess.get("http://minecraft.curseforge.com/mc-mods/%s" % (id), stream=True)
    print(projectResponse)
    fileResponse = sess.get("%s/files/%s/download" % (projectResponse.url, fileId), stream=True)
    while fileResponse.is_redirect:
        source = fileResponse
        fileResponse = sess.get(source, stream=True)
    filePath = Path(fileResponse.url)
    fileName = filePath.name.replace("%20", " ")
    with open(str(minecraftPath + "mods/" + fileName), "wb+") as mod:
        mod.write(fileResponse.content)

doDownload(args.id, args.fileId)