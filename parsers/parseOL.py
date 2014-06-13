#!/usr/bin/python

#build core files for Presidio database

from xml.dom.minidom import parseString
import re
import json
import subprocess
#may not need some of these, preserve memory


globalId = "abdominalsurgery00smit"
#TO DO: have the parser automatically swap IDs from folder

file = open(globalId + "_djvu.txt")
#standardized archive.org extension
data = file.read()
file.close()
#this can probably be abstracted into one function for both files
#or maybe separated into two different parsing scripts

def buildInput():
	text = re.sub("[\n\r]","",data)
	subprocess.call(['touch', 'input.txt'])                       #will probably need to break into two functions
	inp = open('input.txt', 'w')                                      #so input.txt is not opened with every single file (improve speed)
	inp.write(globalId + "    " + text)

	


buildInput()
#output = open("input.txt", "w")
#build metadata entries


"""
file = open(globalId + '_dc.xml')
#standardized archive.org extension
data = file.read()
file.close()
dom = parseString(data)

metaData = dom.getElementsByTagName("div")


def parseMetadata(info, dataNum):
    out = dict()
    for metadataField in ["date"]:
	    out[metadataField] = info.getElementsByTagName(metadataField)[0].childNodes[0].data


	template:
	   define tags to be parsed 
	   loop through document to locate tags
	   output content/child of variable
	   format variable in JSON as parseString
	   write JSON to output
	"""



