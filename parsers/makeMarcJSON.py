#!/usr/bin/python

"""This is the master parsing file. It will take a folder of raw texts, metadata, and marcXML
	and construct the necessary input.txt and jsoncatalog.txt for Presidio to compile."""

#build core files for Presidio database

import re
import string
import os, sys
import subprocess
import xml.etree.ElementTree as ET
#may not need some of these, preserve memory
sys.setrecursionlimit(60000)

#generator that returns next record in specified folder

class folderWalk:
	def __init__(self, folder, extension):
		self.folder = folder
		self.extension = extension

	def __iter__(self):
        	return self

	def openDir(folder, extension):
		for item in os.listdir(folder):
	    		if (os.path.isfile(os.path.join(folder, item))):
	        	    return item
	        	    #combine readItem here



def readItem(item):
	file = open(item, 'r')
	data = file.read()
	file.close()
	return data

class Components:

	def __init__(self):
		#self.marcDir = openDir('/data/MARC', '_marc.xml')
		#self.xmlDir = openDir('MHL_download/mhl_meta_xml_files', '_meta.xml')
		#self.marcRoot = ET.fromstring(readItem(self.marcDir))
		#self.xmlRoot = ET.fromstring(readItem(self.xmlDir))

		def getDate(self):
			pass

		def getLibrary(self):
			pass

		def getLanguage(self):
			pass

		def getTitle(self):
			pass

		def getSearchstring(self):
			pass

		def getSubject(self):
			pass

		def getLocation(self):
			pass


def main():
	x = folderWalk()
	print x.openDir('/data/MARC', '_marc.xml')
	#buildJSON = Components()
	#print buildJSON.marcDir

main()




		
