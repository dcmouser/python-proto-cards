#-------------------------------------------------------------------------------
# Name: CtContracts MakePages
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
from libs.TJrImHelpers import *
#-------------------------------------------------------------------------------

#-------------------------------------------------------------------------------
import os
import random
import math
import string
#-------------------------------------------------------------------------------


#-------------------------------------------------------------------------------
# globals
MainProgramTitle = "Sample Page Composer"
MainProgramVersion = "1.01.01"
MainProgramVersionExtra = "March 12, 2011 - by mouser@donationcoder.com"
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
    ComposeImages()
#-------------------------------------------------------------------------------




























#-------------------------------------------------------------------------------
def ComposeImages():
    # assemble cards onto pages

    imagepath = os.getcwd()+"/cards/outimages"
    print "Assembling pages from "+imagepath

    filepatterns="*.png"
    flag_recurse=0
    outpath = imagepath+"/pages"
    outfnameprefix = "cardpage"
    outfnameext = ".pdf"

    # print details
    printdetails = {}
	
    if (True):
        # not sure where this came from
        printdetails["LabelHeight"]=2.625
        printdetails["LabelWidth"]=3.725
        printdetails["SpacingHorizontal"]=3.90
        printdetails["SpacingVertical"]=2.62
        printdetails["ImageMargin"]=0.0
        printdetails["CountVertical"]=4
        printdetails["CountHorizontal"]=2
        printdetails["OffsetX"]=0.40
        printdetails["OffsetY"]=0.20
        printdetails["PageWidth"]=8.50
        printdetails["PageHeight"]=11.00
        printdetails["PageOrientation"]="landscape"
        printdetails["PageCrop"]=0
        printdetails["Units"]="inches"
        printdetails["DPI"]=300
        printdetails["AutoRotate"]="true"
        printdetails["PreserveAspect"]="false"
        printdetails["BackgroundColor"]="#ffffff"
        printdetails["ShowCardCuts"]=False
    else:
        # plaincards
        printdetails["LabelHeight"]=2.30
        printdetails["LabelWidth"]=3.30
        printdetails["SpacingHorizontal"]=3.92
        printdetails["SpacingVertical"]=2.62
        printdetails["ImageMargin"]=0.05
        printdetails["CountVertical"]=4
        printdetails["CountHorizontal"]=2
        printdetails["OffsetX"]=0.62
        printdetails["OffsetY"]=0.45
        printdetails["PageWidth"]=8.50
        printdetails["PageHeight"]=11.00
        printdetails["PageOrientation"]="landscape"
        printdetails["PageCrop"]=0
        printdetails["Units"]="inches"
        printdetails["DPI"]=150
        printdetails["AutoRotate"]="true"
        printdetails["PreserveAspect"]="true"
        printdetails["BackgroundColor"]="#ffffff"
        printdetails["ShowCardCuts"]=False

    JrImp_LayoutImagePagesFromPath(imagepath,flag_recurse,filepatterns, outpath,outfnameprefix,outfnameext,printdetails)
#-------------------------------------------------------------------------------

























#-------------------------------------------------------------------------------
if __name__ == "__main__":
    main()
#-------------------------------------------------------------------------------
