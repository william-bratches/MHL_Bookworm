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
    
    dirs = os.listdir(path)
    folders = []
    for folder in dirs:
        if os.path.isdir(folder):
            folders.append(folder)
    
    

    globalId = folders[count]
    #archive.org uses a uniform naming system, files similar name to folder
    print globalId   #debugging


    def readInput():
         #this can probably be abstracted into one function for both files
        try:
            file = open(os.path.join(globalId, globalId + "_djvu.txt"), "r") #archive.org extension
        except IOError:
            print "No match found for %s, trying other .txt files" % globalId
            for book in os.listdir(globalId):
                if book.endswith(".txt"):
                     file = open(os.path.join(globalId, book), "r")
                     print book
                     """unsure if this will be effective, I have to see what the larger data looks like
                        in my samples only .txt files are the ones I want, are there > 1 per directory in main database?
                        if not specific enough, search for the first four letters"""
     #else:
     #     print "directory %s contains no .txt files, skipping" % globalId
     #     parseDir() #skip it"""
        data = file.read()
        file.close()



        def buildInput():
            text = re.sub("[\n\r]","",data)
            subprocess.call(['touch', 'input.txt'])
            #maybe more efficient putting input.txt elsewhere, so it doesn't open w/every file?
            inp = open('input.txt', 'a')
            inp.write(globalId + "    " + text + '/n')
            inp.close()
        buildInput()
    readInput()
    
    #recursion
    if count < ((len(folders)) -1):
        count + 1
        parseDir(count)
#initialization
parseDir(0)


#progress indicator?


#build metadata entries
"""
def readJSON():
    jsonfile = open(globalId + '_dc.xml')
    jdata = jsonfile.read()
    file.close()
    dom = parseString(data)
    metaData = dom.getElementsByTagName("div")


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

