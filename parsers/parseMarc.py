#!/usr/bin/python

"""this parser is designed to specifically grab a test database of 3000 books"""

#build core files for Presidio database

from xml.dom.minidom import parseString
import inspect
import re
import os, sys
import subprocess
import xml.etree.ElementTree as ET
from pymarc import MARCReader


def buildMarc():
	xml = open("marctest.xml", "r")
	xml = xml.read()
	root = ET.fromstring(xml)
	for child in root:
		tag = child.get('tag')
		if tag == "650":
			for sub in child:
				print sub.text
		

#write json object to file
jdict = {"library" : "test", 
		 "searchstring" : "[No author], <em>" + "testname" +
				 "</em> (undated) <a href=" + r"\"" + 
				 "http://www.test.com" + r"\"" + ">read</a>",
				 #TODO: expand searchsring to include proper author and title
				 "filename" : "testname",
				 "language" : "eng",
				 "year" : "2014",
				}

json = str(jdict)
json = json.replace("'", '"')
#raw string is printing double backslashes - quick fix
json = json.replace('\\"', '\"')

#print "writing %s metadata to jsoncatalog.txt..." % "test"
buildMarc()
#print jdict

		
