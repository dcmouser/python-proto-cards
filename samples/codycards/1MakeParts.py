#-------------------------------------------------------------------------------
# Sample script showing how to use library to make .pieces files from a bunch of images
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
# globals
MainProgramTitle = "Sample Piece Maker"
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
    AnnounceVersionInfo()
    BuildCards()
#-------------------------------------------------------------------------------















#-------------------------------------------------------------------------------
def BuildCards():
    BuildCards_Main()
#-------------------------------------------------------------------------------











#-------------------------------------------------------------------------------
def BuildCards_Main():
    # create collection of objects
    pobjcp = TJrPObjCollection()

    # now write the card files
    piecepath = os.getcwd()+"/cards/pieces"
    sourceimagepath = os.getcwd()+"/cards/srcimages"

    # leave existing data in files?
    flag_leaveexistingdata=0

    if (flag_leaveexistingdata):
      # read existing data
      print "Reading data from "+piecepath
      # find all card pieces files
      fmanp = pobjcp.get_filemanager()
      fmanp.ScanDirForFiles_CreateFileEntries(piecepath,0,"*.pieces",1)
      # create collection of objects from these files
      pobjcp.LoadObjectsFromFileManager(1)

    # build cards from ingredient images
    BuildCards_FromFoundImages(pobjcp,sourceimagepath)

		# report
    print "\nTotal Cards Found: "+str(pobjcp.get_objectcount())

    print "Writing card pieces to: "+piecepath
    pobjcp.WriteObjectOutputFiles(piecepath,1)
#-------------------------------------------------------------------------------





#---------------------------------------------------------------------------
def BuildCards_FromFoundImages(pobjcp,sourceimagepath):
    # discover all image files and create piece files (or modify existing ones)

    # discover all image files
    imagefmanp = TJrPFileManager()
    imgflist = imagefmanp.ScanDirForFiles_CreateFileEntries(sourceimagepath,1,"*.jpg;*.png;*.gif;*.tiff;*.tif",1)

    # ok now walk them
    for fobj in imgflist:
        # fields for this image file
        imgfname = fobj.get_fname()
        flabel,fvalue,fcategory = JrP_CurrentImageFilenameToCardLabelAndCategory(sourceimagepath,imgfname)
        fname = fcategory+".pieces"
        print "Found image file ("+flabel+") , ("+imgfname+") , ("+fname+") ("+fvalue+"), "+"("+fcategory+")"
        # does this card already exist?
        fdict = dict()
        fdict["__file"]=fname
        fdict["label"]=flabel
        fdict["value"]=fvalue
        pobj = pobjcp.FindObjectByFields(fdict)
        if (pobj==None):
            # it doesn't exist, so create it
            pobj = TJrPObj()
            pobj.add_propertyval("__file",fname)
            pobj.add_propertyval("title",flabel)
            pobj.add_propertyval("value",fvalue)
            pobj.add_propertyval("category",fcategory)
            imagefilename = fcategory+"_"+fvalue+"_"+flabel
            pobj.add_propertyval("image.front",imagefilename)
            pobj.add_propertyval("image.src","../srcimages/"+imgfname)
            pobjcp.AddObject(pobj)
#---------------------------------------------------------------------------

































#-------------------------------------------------------------------------------
if __name__ == "__main__":
    main()
#-------------------------------------------------------------------------------
