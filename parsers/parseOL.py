#!/usr/bin/python

#build core files for Presidio database

from xml.dom.minidom import parseString
import re
import subprocess
from lxml import etree
#may not need some of these, preserve memory


globalId = "abdominalsurgery00smit"
#TO DO: have the parser automatically swap IDs from folder

def readInput():
	file = open(globalId + "_djvu.txt") #archive.org extension
	data = file.read()
	file.close()
	#this can probably be abstracted into one function for both files
	#or maybe separated into two different parsing scripts


	def buildInput():
		text = re.sub("[\n\r]","",data)
		subprocess.call(['touch', 'input.txt'])                       #will probably need to break into two functions
		inp = open('input.txt', 'w')                                      #so input.txt is not opened with every single file (improve speed)
		inp.write(globalId + "    " + text + '/n')
		inp.close()
	buildInput()
readInput()




#build metadata entries

def readJSON():
	jsonfile = open(globalId + '_dc.xml')
	jdata = jsonfile.read()
	file.close()
	dom = parseString(data)
	metaData = dom.getElementsByTagName("div")


	def parseMetadata(info, dataNum):
    		root = etree.fromstring(jdata)
	 	 subprocess.call(['touch', 'jsoncatalog.txt'])
	 	 jtxt = open('jsoncatalog.txt', 'w')
	 	 	#tags to search go here
	 	 	for element in root.iter("date")
	 	 		jtxt.write("{ date: ") + '"' element.items()) #tag needs to be stripped
				+ '", "filename:" ' + globalId + "searchstring:" + url + "}"    #better way to do this?
	 	 	for element in root.iter("contributor")
                                            #same code for contributor tag tag
                       jtxt.close()

	
	 	 parseMetadata()
readJSON()
