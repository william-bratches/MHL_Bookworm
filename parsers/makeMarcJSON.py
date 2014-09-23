

#build core files for Presidio database

import re
import string
import os, sys
import subprocess
import xml.etree.ElementTree as ET
from xml.dom.minidom import parseString
import inspect
from pymarc import MARCReader
#may not need some of these, preserve memory
sys.setrecursionlimit(70000)

# open files, folders, read them
class fileHandlers:

	def __init__(self, directory, directoryAlt):
		self.directory = directory
		self.directoryAlt = directoryAlt #may be redundant

	'''
	#generator that returns next record in specified folder
	#turned out to be extremely buggy when abstracted
	def openDir(self, dir):
			for file in os.listdir(self.directory):
	    			if (os.path.isfile(os.path.join(self.directory, file))):
	        			yield file
	'''
	# older, slow, terrible method for iterating over file directory
	# on the wishlist to improve but for now it gets the job done
	def openDir(self, dir):
		files = []
		for item in os.listdir(dir):
        		if (os.path.isfile(os.path.join(dir, item))):
            			files.append(item)
    				return files


	#reads data within a file
	def readItem(self, count):
		file = open((os.path.join(self.directory, self.openDir
			(self.directory)[count])), 'r')
		data = file.read()
		file.close()
		return data


	#MARC data will be used as a base. If it can't find relevant data in MARC,
	#open file in XML directory instead.
	def readAlternate(self, count, extension):
		#chop off the filetype, replace it
		#note: only possible due to archive.org's impressive uniformity
		item = self.openDir(self.directory)[count]
		item = item[:-9]
		item = item + extension
		file = open((os.path.join(self.directoryAlt, self.openDir
			(self.directoryAlt)[count])), 'r')
		data = file.read()
		file.close()
		return data



#functions that construct the JSON array
class Components:

	def __init__(self, count):
		self.count = count #is an integer
		#how and I going to pass this along in recursion?

		self.files = fileHandlers('/data/MARC', 
			'/home/will/MHL_download/mhl_meta_xml_files')
		self.marcNext = self.files.openDir(self.files.directory)
		self.xmlNext = self.files.openDir(self.files.directoryAlt)

		self.readMarc = self.files.readItem(count)
		self.readXml = self.files.readAlternate(count, "_meta.xml")

		self.marcRoot = ET.fromstring(self.readMarc)
		self.xmlRoot = ET.fromstring(self.readXml)

#problem: how to align, synchornize two different filetypes
	def getDate(self):
		if True or False: #leaving flexibility in, currently always true
			root = self.marcRoot
			for child in root:
				tag = child.get('tag')
				if tag == "260":
						for sub in child:
							code = sub.get('code')
							if code == "c":
								return code
		else:
			# can put alternate XML method here
			print "failed"
		pass
              

	def getLibrary(self):
		try:
			for contributor in xmlRoot.findall('contributor'):
				library = contributor.text
		except TypeError:
			library = ""

		# validation
		if 'library' in locals():
			pass
		else:
			library = "Other"


	def getLanguage(self):
		for language in xmlRoot.findall('language'):
			language = language.text

			if language=="English": #MHL database inconsistency
				language = "eng"

		# validation
		if 'language' in locals():
			pass
		else:
			language = ""

	def getTitle(self):
		for title in root.findall('title'):
			title = title.text
		#sets title to filename if it does not exist
		if 'title' in locals():
			title = filter(lambda x: x in string.printable, title)
			title = title.replace('"', '')
			title = title.replace("'", " ")
		else:
			title = filename

	def getSearchstring(self):
		for arlink in xmlRoot.findall('identifier-access'):
			searchstring = arlink.text
			if searchstring in locals():
				searchstring = "[" + author + "], <em>" + title + \
					 			"</em> (" + year + ") <a href=" + r"\"" + \
								 searchstring + r"\"" + ">read</a>"
				searchstring = searchstring.encode('ascii','ignore')
			else:
				searchstring = ""

	def getSubject(self):
		pass

	def getLocation(self):
		pass


def main():
	buildJSON = Components(0)
	print buildJSON.readMarc
	print buildJSON.getDate()




main()

