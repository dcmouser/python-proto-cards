#-------------------------------------------------------------------------------
# Name: Export .pieces files
# This script creates a set of text pieces files that define cards
#-------------------------------------------------------------------------------
#!/usr/bin/env python

#-------------------------------------------------------------------------------
# include top level TJrPythonProtoCards directory
import sys
sys.path.append("../../") 
#-------------------------------------------------------------------------------

#-------------------------------------------------------------------------------
# import the helper classes
from libs.TJrPFileClasses import *
#-------------------------------------------------------------------------------

#-------------------------------------------------------------------------------
import os
import random
import math
import string
#-------------------------------------------------------------------------------





#-------------------------------------------------------------------------------
# module globals
MainProgramTitle = "Pieces Json Export"
MainProgramVersion = "1.01.01"
MainProgramVersionExtra = "July 10, 2011 - by mouser@donationcoder.com"
#-------------------------------------------------------------------------------





#-------------------------------------------------------------------------------
def ShowUsage():
    AnnounceVersionInfo()

def AnnounceVersionInfo():
	print MainProgramTitle+" v"+MainProgramVersion+" ("+MainProgramVersionExtra+")"
#-------------------------------------------------------------------------------




#-------------------------------------------------------------------------------
def main():
    print "\n\n\n\n"
    AnnounceVersionInfo()
    ExportJsonFile()
#-------------------------------------------------------------------------------














#-------------------------------------------------------------------------------
def ExportJsonFile():
    pobjcp = TJrPObjCollection()

    piecepath = os.getcwd()+"/cards/pieces"
    outpath = os.getcwd()+"/cards"

    print "Reading data from "+piecepath

    # find all card pieces files
    fmanp = pobjcp.get_filemanager()
    fmanp.ScanDirForFiles_CreateFileEntries(piecepath,1,"*.pieces",1)

    # create collection of objects from these files
    pobjcp.LoadObjectsFromFileManager(1)

    # write out json
    pobjcp.ExportToJson(outpath+"/cards.json")
#-------------------------------------------------------------------------------



















#-------------------------------------------------------------------------------
if __name__ == "__main__":
    main()
#-------------------------------------------------------------------------------
