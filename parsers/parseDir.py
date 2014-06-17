#!/usr/bin/python

#build core files for Presidio database

from xml.dom.minidom import parseString
import re
import os, sys
import subprocess
#from lxml import etree
#may not need some of these, preserve memory


#main function to parse a directory
def parseDir(count):
    #set a directory to parse for archive.org files
    path = '.'

    #make an array w/all folders
    dirs = os.listdir(path)
    folders = []
    for folder in dirs:
        if os.path.isdir(folder):
            folders.append(folder)

    #extract archive.org ID from folder name
    globalId = folders[count]


    #open the appropriate file, pull its contents
    def readInput(fileType, extension):
        try:
            file = open(os.path.join(globalId, globalId + extension), "r") #archive.org ID + extension
        except IOError:
            print "No match found for %s, trying other %s files" % globalId fileType
            #search for other files in directory
            for book in os.listdir(globalId):
                if book.endswith(fileType):
                     file = open(os.path.join(globalId, book), "r")
                     print book
        data = file.read()
        file.close()
        return data



    def buildInput():
        text = re.sub("[\n\r]","", readInput(".txt", "_djvu.txt"))
        subprocess.call(['touch', 'input.txt'])
        #maybe more efficient putting input.txt elsewhere, so it doesn't open w/every file?
        inp = open('input.txt', 'a')
        inp.write(globalId + "    " + text + '/n')
        inp.close()

	buildInput() #could be cause of endless recursion?
   
   


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
	if count < ((len(folders)) -1):
  		count + 1
  	  	parseDir(count)


#initialization
parseDir(0)
#progress indicator?