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
			print filename  #debugging purposes
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

		try:

			jdict = {"library" : library, 
					 "searchstring" : searchstring,
					 "filename" : filename,
					 "language" : language,
					 "year" : year,
					}


		except UnboundLocalError as e:
			#finds which variable is not defined, makes that variable an empty string
			varErr = str(e)
			varErr = re.findall(r"'(.*?)'", varErr, re.DOTALL)
			print varErr

			# this is a temporary solution. need to talk to ben about this one
			# what would happen if bookworm had missing data
			# tried to have it skip cases w/o data, but still got unbound error
			jdict = {"library" : ("" if varErr == "['library']" else ""),
					 "searchstring" : ("" if varErr == "['searchstring']" else ""),
					 "filename" : filename,
					 "language" : ("" if varErr == "['language']" else ""),
					 "year" : ("" if varErr == "['year']" else ""),
					}
					#might run into trouble if a file is missing TWO things
					

		json = str(jdict)

		#may do if except:
		#jdict = {"searchstring: searchstring, "filename" : filename}

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

		