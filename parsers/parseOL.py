#!/usr/bin/python

#build core files for Presidio database

from xml.dom.minidom import parseString
import re
import json


globalId = "abdominalsurgery00smit"
#TO DO: have the parser automatically swap IDs from folder

#build input.txt

file = open(globalId + "_djvu.txt")
#standardized archive.org extension
text = file.read()
file.close()
domtxt = parseString(text)
#this can probably be abstracted into one function for both files
#or maybe separated into two different parsing scripts

def buildInput():

	"""template:
	   store title in variable
	   filter text (i.e. newlines)
	   store filtered text in variable
	   append end of input.txt with {title text}
	"""

#build metadata entries

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


	"""template:
	   define tags to be parsed 
	   loop through document to locate tags
	   output content/child of variable
	   format variable in JSON as parseString
	   write JSON to output
	"""



