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

# open files, folders, read them
class fileHandlers:

	def __init__(self, directory):
		self.directory = directory


	#generator that returns next record in specified folder
	def openDir(self):
		for file in os.listdir(self.directory):
	    		if (os.path.isfile(os.path.join(self.directory, file))):
	        	    yield file


	#reads data within a file
	def readItem(self, item):
		file = open((os.path.join(self.directory, item)), 'r')
		data = file.read()
		file.close()
		return data


#functions that construct the JSON array
class Components:

	def __init__(self):
		self.marcDir = fileHandlers('/data/MARC')
		self.xmlDir = fileHandlers('/home/will/MHL_download/mhl_meta_xml_files')
		self.marcNext = self.marcDir.openDir().next()
		self.xmlNext = self.xmlDir.openDir().next()

		self.marcRoot = ET.fromstring(self.marcDir.readItem(self.marcNext))
		self.xmlRoot = ET.fromstring(self.xmlDir.readItem(self.xmlNext))

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
	buildJSON = Components()
	print buildJSON.marcDir.openDir().next()

	

main()




		
