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
def parseFolder(folder, extension):
    files = []
    for item in os.listdir(folder):
        if (os.path.isfile(os.path.join(folder, item))):
            files.append(item)
    return files


#open the appropriate file, pull its contents
def readInput(count, folder, files):
	file = open((os.path.join(folder, files[count])), 'r')
	data = file.read()
	file.close()
	return data


#put file contents into input.txt, recur through entire folder
def buildInput(count):
	files = parseFolder("/data/MHL/MHL_Bookworm/samples/texts", '_djvu.txt')
	subprocess.call(['touch', 'input.txt'])
	inp = open('input.txt', 'a')

	def buildData(count):
		text = re.sub("[\n\r]","", readInput(count, "/data/MHL/MHL_Bookworm/samples/texts", files))
		print "writing %s to input.txt" % files[count]
		inp.write(files[count][:-9] + "    " + text + '\n') #chops off _djvu.txt for global identification
		if count < ((len(files)) -1):
			count = count + 1
			buildData(count)
		else:
			print "files done building!"	
	buildData(count)
	inp.close()



buildInput(0)

"""
#might need a system of extracting global IDs, matching them against jsoncatalog.txt

#build metadata entries

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


#recursion --> next folder in array
#def recur(count):
	
		


#initialization
#progress indicator?
"""