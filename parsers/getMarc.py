import re
import string
import os, sys
import subprocess

sys.setrecursionlimit(60000)

#open itemlist.txt
records = open('itemlist.txt', 'r')

for line in records:
	url = "https://archive.org/download/%s/%s_marc.xml" % (line, line)
	subprocess.call(['wget', url])
	print "Grabbing MARC data from https://archive.org/download/%s/%s_marc.xml" % (line, line)


#first item - assign variable
#wget
#next item in list
#repeat

subprocess.call(['touch', 'jsoncatalog.txt'])