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

parser.add_argument('id', metavar='id',
                   help='id of mod to be downloaded')
args, unknown = parser.parse_known_args()

def doDownloadByName(name):
	
    sess = requests.session()
    searchResponse = sess.get("http://minecraft.curseforge.com/search?search="+name)
    reg = re.compile("<a class=\"results-image e-avatar64 \" href=\"/mc-mods/.{1,50}\">")
    links = reg.findall(str(searchResponse.content))
    for i in range(len(links)):
    	links[i] = links[i].replace("<a class=\"results-image e-avatar64 \" href=\"", "")
    	links[i] = links[i].replace("\">", "")
    	
    
    dlCountMax = -1
    dlCountProj = ""
    for link in links:
    
    	#Messy regex to get download counts
    	projectResponse = sess.get("http://minecraft.curseforge.com/" + link, stream=True)
    	page = projectResponse.content
    	reg = re.compile("<div class=\"info-label\">Total Downloads</div>.{1,30}<div class=\"info-data\">.{1,16}</div>")
    	dl = reg.findall(str(projectResponse.content))[0]
    	reg = re.compile("<div class=\"info-data\">.{1,16}</div>")
    	dl = reg.findall(dl)[0]
    	dl = dl.replace("<div class=\"info-data\">", "")
    	dl = dl.replace("</div>", "")
    	dl = dl.replace(",", "")
    	dlcount = int(dl)
    	if dlcount > dlCountMax:
    		dlCountMax = dlcount
    		dlCountProj = link
    link = dlCountProj
    	
    sess = requests.session()
    projectResponse = sess.get("http://minecraft.curseforge.com/" + link, stream=True)
    fileResponse = sess.get("%s/files/latest" % (projectResponse.url), stream=True)
    while fileResponse.is_redirect:
        source = fileResponse
        fileResponse = sess.get(source, stream=True)
    filePath = Path(fileResponse.url)
    fileName = filePath.name.replace("%20", " ")
    with open(str(minecraftPath + "mods/" + fileName), "wb+") as mod:
        mod.write(fileResponse.content)
    
def doDownload(id):
    sess = requests.session()
    projectResponse = sess.get("http://minecraft.curseforge.com/mc-mods/%s" % (id), stream=True)
    fileResponse = sess.get("%s/files/latest" % (projectResponse.url), stream=True)
    while fileResponse.is_redirect:
        source = fileResponse
        fileResponse = sess.get(source, stream=True)
    filePath = Path(fileResponse.url)
    fileName = filePath.name.replace("%20", " ")
    with open(str(minecraftPath + "mods/" + fileName), "wb+") as mod:
        mod.write(fileResponse.content)

doDownloadByName(args.id)