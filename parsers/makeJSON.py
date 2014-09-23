#!/usr/bin/python

"""This is the master parsing file. It will take a folder of raw texts, metadata, and marcXML
    and construct the necessary input.txt and jsoncatalog.txt for Presidio to compile."""

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
sys.setrecursionlimit(60000)




def parseFolder(folder, extension):
    files = []
    for item in os.listdir(folder):
        if (os.path.isfile(os.path.join(folder, item))):
            files.append(item)
    return files


#open the appropriate file, pull its contents
def readMarcFolder(count, folder, files):
    xmlItem = files[count]
    marcItem = xmlItem[:9] + "_marc.xml"
    file = open((os.path.join('/data/MARC', marcItem)), 'r')
    data = file.read()
    file.close()
    return data

def readFolder(count, folder, files):
    file = open((os.path.join(folder, files[count])), 'r')
    data = file.read()
    file.close()
    return data

#build jsoncatalog.txt
def makeMeta(count):
    print "building jsoncatalog.txt..."
    xfiles = parseFolder("/home/will/MHL_download/mhl_meta_xml_files", '_meta.xml')
    subprocess.call(['touch', 'jsoncatalog.txt'])
    meta = open('jsoncatalog.txt', 'a')

    #extract XML, MARC tags, place in jsoncatalog.txt
    def buildMeta(count):
        root = ET.fromstring(readFolder(count, "/home/will/MHL_download/mhl_meta_xml_files", xfiles))
        


        #filename
        for identifier in root.findall('identifier'):
            filename = identifier.text
            #print filename #debugging



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
                elif date.text[-2:].isdigit() and not(date.text[-3:].isdigit()) and len(date.text) < 8:
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
            for contributor in root.findall('contributor'):
                library = contributor.text

        except TypeError:
            library = ""
        #hacked error handling
        if 'library' in locals():
            pass
        else:
            library = "Other"
            

        #language
        for language in root.findall('language'):
            language = language.text

            if language=="English": #MHL database inconsistency
                language = "eng"
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
            title = filter(lambda x: x in string.printable, title)
            title = title.replace('"', '')
            title = title.replace("'", " ")
        else:
            title = filename

        #author
        for creator in root.findall('creator'):
            author = creator.text

        if 'author' in locals():
            try:
                author = author.replace('"', '')
                author = author.replace("'", "")
            except AttributeError:
                author = ""
        else:
            author = ""
        #the above XML elements could be potentially abstracted into a single function


        #searchstring
        for arlink in root.findall('identifier-access'):
            searchstring = arlink.text
            searchstring = "[" + author + "], <em>" + title + \
                        "</em> (" + year + ") <a href=" + r"\"" + \
                        searchstring + r"\"" + ">read</a>"
            searchstring = searchstring.encode('ascii','ignore')
            searchstring = searchstring.replace('"', '')
            searchstring = searchstring.replace("'", " ")

        #hacked error handling
        if 'searchstring' in locals():
           pass
        else:
           searchstring = ""

        #location
        try:
            xmlItem = xfiles[count]
            marcItem = xmlItem[:-9] + "_marc.xml"
            print marcItem
            xml = open((os.path.join('/data/MARC', marcItem)), 'r')
            xmlRead = xml.read()
            xml.close()
            rootMarc = ET.fromstring(xmlRead)
            subjectArray = []
            for child in rootMarc:
                    tag = child.get('tag')
                    if tag == "260":
                        for sub in child:
                            print sub.text[:9]
                            city = filter(lambda x: x in string.ascii_letters, sub.text)
                            if city == "Londonetc":
                            	location = "London"
                            elif city == "NewYork":
                            	location ="New York"
                            else:
                            	location = city

                            #code = child.get('c:ode')
                           # if code == "a":
                            #    print sub
            if 'location' in locals():
                pass
            else:
                location = ""

        except IOError:
            location = ""

        #subjects
        try:
            xmlItem = xfiles[count]
            marcItem = xmlItem[:-9] + "_marc.xml"
            xml = open((os.path.join('/data/MARC', marcItem)), 'r')
            xmlRead = xml.read()
            xml.close()
            rootMarc = ET.fromstring(xmlRead)
            subjectArray = []
            for child in rootMarc:
                    tag = child.get('tag')
                    if tag == "650":
                            for sub in child:

                                try:
                                    subword = sub.text
                                    subword = subword.replace(".", "")
                                    subword = subword.replace(";", "")
                                    subjectArray.append(subword)
                                except AttributeError:
                                    subjectArray.append(sub.text)
        except IOError:
 
            subjectArray = []
            for subject in root.iter('subject'):
                subject = subject.text
                if subject is not None:
                    stext = subject.replace(',', '-')
                    stext = stext.replace('"', '')
                    #stext = filter(lambda x: x in string.ascii_letters, stext)
                    subArray = subject.split("--")
                    subArray = subject.split("-")
                    subjectArray.append(stext)

                    #cleans up the words i.e. semicolons will not appear as subjects
                    for word in subArray:
                        rx = re.compile('\W+')
                       #cleanWord = rx.sub('', word).strip()
                        cleanWord = rx
                        cleanWord = cleanWord.sub('"', '')
                        if cleanWord[:4].isdigit():
                            pass
                        elif len(cleanWord) < 3:
                            pass
                        #should probably make a dictionary
                        elif cleanWord=="and":
                            pass
                        elif cleanWord=="for":
                            pass
                        elif cleanWord=="drug" or "Drug":
                            pass
                        elif cleanWord=="industry" or "Industry":
                            pass
                        elif cleanWord=="system" or "System":
                            pass
                        else:
                            cleanWord = cleanWord.lower().capitalize()
                            subjectArray.append(cleanWord)
                else:
                    subjectArray = "Miscellaneous"
                 


        #write json object to file
        jdict = {"library" : library,
                 "searchstring" : searchstring,
                 "filename" : filename,
                 "language" : language,
                 "year" : year,
                 "subject" : subjectArray,
                 "location": location,
                }

        json = str(jdict)
        json = json.replace("'", '"')
        #raw string is printing double backslashes - quick fix
        json = json.replace('\\"', '\"')

        print "writing %s metadata to jsoncatalog.txt..." % filename
        meta.write(json + '\n')

        #recursion
        if count < ((len(xfiles)) -1):
            count = count + 1
            buildMeta(count)
        else:
            print "\n jsoncatalog.txt done building! \n"

    buildMeta(count)



makeMeta(0)


        
