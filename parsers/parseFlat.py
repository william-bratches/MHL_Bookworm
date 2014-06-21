#!/usr/bin/python

"""this parser is designed to specifically grab a test database of 3000 books"""

#build core files for Presidio database

from xml.dom.minidom import parseString
import inspect
import re
import os, sys
import subprocess
import xml.etree.ElementTree as ET
#may not need some of these, preserve memory
sys.setrecursionlimit(3500)


#navigate a folder, create array with all files and file globalId
def parseFolder(folder, extension):
    files = []
    for item in os.listdir(folder):
        if (os.path.isfile(os.path.join(folder, item))):
            files.append(item)
    return files


#open the appropriate file, pull its contents
def readFolder(count, folder, files):
	file = open((os.path.join(folder, files[count])), 'r')
	data = file.read()
	file.close()
	return data

#put file contents into input.txt, recur through entire folder
def makeInput(count):
	print "building input.txt..."
	files = parseFolder("/data/MHL/MHL_download/mhl_djvu_txt_files", '_djvu.txt')
	subprocess.call(['touch', 'input.txt'])
	inp = open('input.txt', 'a')

	def buildInput(count):
		text = re.sub("[\n\r]","", readFolder(count, "/data/MHL/MHL_download/mhl_djvu_txt_files", files))
		print "writing %s to input.txt..." % files[count]
		inp.write(files[count][:-9] + "    " + text + '\n') #chops off _djvu.txt to get ID

		#recursion
		if count < 3000:
			count = count + 1
			buildInput(count)
		else:
			print "input.txt done building!"	

	buildInput(count)
	inp.close()


#build jsoncatalog.txt
#first pass: year, library, language
def makeMeta(count):
	print "building jsoncatalog.txt..."
	xfiles = parseFolder("/data/MHL/MHL_download/mhl_meta_xml_files", '_meta.xml')
	subprocess.call(['touch', 'jsoncatalog.txt'])
	meta = open('jsoncatalog.txt', 'a')

	def buildMeta(count):
		root = ET.fromstring(readFolder(count, "/data/MHL/MHL_download/mhl_meta_xml_files", xfiles))
		

		#required tags
		for identifier in root.findall('identifier'):
			filename = identifier.text
			print filename
		for arlink in root.findall('identifier-access'):
			searchstring = arlink.text
		#hacked-in error handling/debugging; elegant nested solutions did not work
		if 'searchstring' in locals():
			print "searchstring exists"
		else:
			searchstring = ""

		#optional tags to extract
		"""note: I have hacked in some robust error handling, normal nested solutions like 'if x is None' 
			failed to work. I will improve the elegance  of this after I compile a working database."""
		#date: handles inconsistent formatting
		for date in root.findall('date'):
			
			try:
				#if (i.e. 1822-1946), take last four digits
				if date.text[-4:].isdigit():
					year = date.text[-4:]

				#i.e. 1922-26 -> 1926
				elif date.text[-2:].isdigit() and not(date.text[-3:].isdigit()):
					year = date.text[:2] + date.text[-2:]

				else:
					#take first four characters for any other inconsistency
					year = date.text[:4]
			except TypeError:
				year = ""
		#hacked-in error handling/debugging
		if 'year' in locals():
			print "year exists"
		else:
			year = ""


		
		#contributing library: occasionally does not exist
		try:
			for contributor in root.find('contributor'):
				library = library.text

		except TypeError:
			library = ""
		#hacked-in error handling/debugging
		if 'library' in locals():
			print "library exists"
		else:
			library = ""


		#language
		for language in root.findall('language'):
			if language.text == "eng":
				language = "english"
			elif language.text == "ger":
				language = "german"
			elif language.text == "fre":
				langauge = "french"
			else:
				language = language.text
		#hacked-in error handling/debugging
		if 'language' in locals():
			print "language exists"
		else:
			language = ""

		#write json object to file
		jdict = {"library" : library, 
				 "searchstring" : searchstring,
				 "filename" : filename,
				 "language" : language,
				 "year" : year,
				}

		json = str(jdict)

		print "writing %s metadata to jsoncatalog.txt..." % filename
		meta.write(json + '\n')

		#recursion
		if count < 3000:
			count = count + 1
			buildMeta(count)
		else:
			print "jsoncatalog.txt done building!"

	buildMeta(count)



makeMeta(0)
makeInput(0)

		