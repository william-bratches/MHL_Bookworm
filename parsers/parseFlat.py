#!/usr/bin/python

"""This is the master parsing file. It will take a folder of raw texts, metadata, and marcXML
	and construct the necessary input.txt and jsoncatalog.txt for Presidio to compile."""

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

#make input.txt, set the directory to be parsed
def makeInput(count):
	print "building input.txt..."
	files = parseFolder("/data/MHL/MHL_download/mhl_djvu_txt_files", '_djvu.txt')
	subprocess.call(['touch', 'input.txt'])
	inp = open('input.txt', 'a')

	#put file contents into input.txt, recur through entire folder
	def buildInput(count):
		text = re.sub("[\n\r]","", readFolder(count, "/data/MHL/MHL_download/mhl_djvu_txt_files", files))
		print "writing %s to input.txt..." % files[count]
		inp.write(files[count][:-9] + "\t" + text + '\n') #chops off _djvu.txt to get ID

		#recursion
		if count < 5:
			count = count + 1
			buildInput(count)
		else:
			print "\n input.txt done building! \n"	

	buildInput(count)
	inp.close()


#build jsoncatalog.txt
def makeMeta(count):
	print "building jsoncatalog.txt..."
	xfiles = parseFolder("/data/MHL/MHL_download/mhl_meta_xml_files", '_meta.xml')
	subprocess.call(['touch', 'jsoncatalog.txt'])
	meta = open('jsoncatalog.txt', 'a')

	#extract XML, MARC tags, place in jsoncatalog.txt
	def buildMeta(count):
		root = ET.fromstring(readFolder(count, "/data/MHL/MHL_download/mhl_meta_xml_files", xfiles))


		#required tags
		for identifier in root.findall('identifier'):
			filename = identifier.text
			#print filename #debugging
		for arlink in root.findall('identifier-access'):
			searchstring = arlink.text
		#hacked error handling
		if 'searchstring' in locals():
			pass
		else:
			searchstring = ""



		#optional tags to extract
			"""note: I have hacked in some robust error handling, there were scope issues with
			   more elegant solutions, and it would require dynamically named variables,
			   so for now it is reliable brute force. Apologies for the mess,
			   I am aware that this is bad coding, and hope to clean it up later"""
			   
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
		#hacked error handling
		if 'year' in locals():
			pass
		else:
			year = ""


		
		#contributing library
		try:
			for contributor in root.find('contributor'):
				library = library.text

		except TypeError:
			library = ""
		#hacked error handling
		if 'library' in locals():
			pass
		else:
			library = ""
			


		#language
		for language in root.findall('language'):
			language = language.text
		#hacked error handling
		if 'language' in locals():
			pass
		else:
			language = ""



		#title
		for title in root.findall('title'):
			title = title.text
		#sets title to filename if it does not exist
		if 'title' in locals():
			pass
		else:
			title = filename

		#author
		for creator in root.findall('creator'):
			author = creator.text
		if 'author' in locals():
			pass
		else:
			author = ""
	


		"""
		def buildMarc()
		#build marc files here
		"""

		#write json object to file
		jdict = {"library" : library, 
				 "searchstring" : "[" + author + "], <em>" + title +
				 "</em> (" + year + ") <a href=" + r"\"" + 
				 searchstring + r"\"" + ">read</a>",
				 "filename" : filename,
				 "language" : language,
				 "year" : year,
				}

		json = str(jdict)
		json = json.replace("'", '"')
		#raw string is printing double backslashes - quick fix
		json = json.replace('\\"', '\"')

		print "writing %s metadata to jsoncatalog.txt..." % filename
		meta.write(json + '\n')

		#recursion
		if count < 5:
			count = count + 1
			buildMeta(count)
		else:
			print "\n jsoncatalog.txt done building! \n"

	buildMeta(count)



makeMeta(0)
makeInput(0)

		
