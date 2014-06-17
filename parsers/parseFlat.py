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
#from lxml import etree
#may not need some of these, preserve memory

#navigate a folder, create array with all files and file globalId
def parseFolder(count, folder, extension):
    files = []
    for item in dirs:
        if os.path.isfile(item):
            files.append(item)

    #extract archive.org ID from file name, disabled - see note at top
    #globalId = files[count]
    #return globalId[:-len(extension)]
    return files

#open the appropriate file, pull its contents
def readInput(fileType, extension):
	try:
   	 	file = open(os.path.join(globalId, globalId + extension), "r") #archive.org ID + extension
	except IOError:
   	 	print "No match found for %s, trying partial match for %s files" % globalId fileType
    #search for other files in directory
   		for book in os.listdir(globalId):
       	 	if book.endswith(fileType):
            	file = open(os.path.join(globalId, book), "r")
            	print book
	data = file.read()
	file.close()
	return data


#put file contents into input.txt, recur through entire folder
def buildInput():
	text = re.sub("[\n\r]","", readInput(".txt", "_djvu.txt"))
	subprocess.call(['touch', 'input.txt'])
	#maybe more efficient putting input.txt elsewhere, so it doesn't open w/every file?
	inp = open('input.txt', 'a')
	inp.write(globalId + "    " + text + '/n')
	inp.close()

buildInput() #could be cause of endless recursion?


#might need a system of extracting global IDs, matching them against jsoncatalog.txt

#build metadata entries
"""
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
"""

#recursion --> next folder in array
def recur:
	if count < ((len(files)) -1):
		count + 1
		return count


#initialization
parseFolder(0, './mhl_djvu_txt_files/', "_djvu.txt")
#progress indicator?