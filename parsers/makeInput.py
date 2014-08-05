import subprocess
import os, sys
import re

sys.setrecursionlimit(60000)

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
def makeInput(count, end):
	print "building input.txt..."
	files = parseFolder("/data/MHL/MHL_download/mhl_djvu_txt_files", '_djvu.txt')
	subprocess.call(['touch', 'input.txt'])
	inp = open('input.txt', 'a')

	#put file contents into input.txt, recur through entire folder
	def buildInput(count, end):
		text = re.sub("[\n\r]","", readFolder(count, "/data/MHL/MHL_download/mhl_djvu_txt_files", files))
		print "writing %s to input.txt..." % files[count]
		print count
		inp.write(files[count][:-9] + "\t" + text + '\n') #chops off _djvu.txt to get ID

		#recursion
		if count < ((len(files)) -1):
			count = count + 1
			buildInput(count, end)

		elif count < end:
			"Chunk at %i finished, building next..." % count
			del text #free memory

		else:
			print "\n input.txt done building! \n"	

	buildInput(count, end)
	inp.close()

makeInput(0, 20000)
del files
makeInput(20000, 40000)
del files
makeInput(40000, 60000)

