#!/usr/bin/python

"""this is a parser designed to build the input.txt and jsoncatalog.txt for the MHL bookworm in a flat
directory tree where individual items do NOT have their own directories. parseDir handles the other case.

A note on efficiency: right now the parser assumes that all files are perfectly set up, i.e. every
input.txt has a corresponding meta.xml. This allows the parser to efficiently build data in bulk,
parsing the entire text folder at once, for example. It may be modified later to build the database
piecemeal, checking to see if every input.txt has a corresponding metadata file and then building a
new line in both input.txt and jsoncatalog.txt for that single library item. We'll see how the final
Presidio build goes."""

#build core files for Presidio database

from xml.dom.minidom import parseString
import re
import os, sys
import subprocess
import xml.etree.ElementTree as ET
#may not need some of these, preserve memory


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
	files = parseFolder("/data/MHL/MHL_Bookworm/samples/texts", '_djvu.txt')
	subprocess.call(['touch', 'input.txt'])
	inp = open('input.txt', 'a')

	def buildInput(count):
		text = re.sub("[\n\r]","", readFolder(count, "/data/MHL/MHL_Bookworm/samples/texts", files))
		print "writing %s to input.txt..." % files[count]
		inp.write(files[count][:-9] + "    " + text + '\n') #chops off _djvu.txt to get ID
		if count < ((len(files)) -1):
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
	xfiles = parseFolder("/data/MHL/MHL_Bookworm/samples/meta", '_meta.xml')
	subprocess.call(['touch', 'jsoncatalog.txt'])
	meta = open('jsoncatalog.txt', 'a')

	def buildMeta(count):
		root = ET.fromstring(readFolder(count, "/data/MHL/MHL_Bookworm/samples/meta", xfiles))
		

		#required tags
		for identifier in root.findall('identifier'):
			filename = identifier.text
			print filename
		for arlink in root.findall('identifier-access'):
			searchstring = arlink.text

		#optional tags to extract
		for date in root.findall('date'):
			#if (i.e. 1822-1946), take last four digits
			if date.text[-4:].isdigit():
				year = date.text[-4:]

			#i.e. 1922-26 -> 1926
			elif date.text[-2:].isdigit() and not(date.text[-3:].isdigit()):
				year = date.text[:2] + date.text[-2:]

			else:
				#take first four characters for any other inconsistency
				year = date.text[:4]

		for contributor in root.findall('contributor'):
			library = contributor.text

		for language in root.findall('language'):
			if language.text == "eng":
				language = "english"
			else:
				language = language.text

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
		if count < ((len(xfiles)) -1):
			count = count + 1
			buildMeta(count)
		else:
			print "jsoncatalog.txt done building!"

	buildMeta(count)


makeMeta(0)

#makeInput(0)

		