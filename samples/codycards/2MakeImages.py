#-------------------------------------------------------------------------------
# Name: CookingParty MakeImages
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
# PIL toolkit (http://www.pythonware.com/products/pil/)
import Image
from PIL import Image
import ImageFile
import ImageDraw
import ImageFont
#-------------------------------------------------------------------------------


#-------------------------------------------------------------------------------
# set this to change options for pdf file output for card printing
Global_flag_pdfcardprinter = False
#-------------------------------------------------------------------------------


#-------------------------------------------------------------------------------
# module globals
MainProgramTitle = "Sample Card Image Maker"
MainProgramVersion = "1.03.01"
MainProgramVersionExtra = "March 26, 2011 - by mouser@donationcoder.com"
#-------------------------------------------------------------------------------


#-------------------------------------------------------------------------------
Global_CardSize_Width = 788
Global_CardSize_Height = 1088
Global_DPI = 300
#
Global_CardFileExt = ".png"
#
Global_CardBackgroundColor = "#ffffff"
Global_SaveCardFormatConversion = "RGB"
#
if (False):
  # margin for safe printing bleed is about 0.5 inch (150pixels @ 300dpi)
  Global_CardMargin_Outer_Default = 75
  Global_CardMargin_Inner_Default = 10
  Global_BorderSize_Default = 20
else:
  # OR do we want full bleed color border
  Global_CardMargin_Outer_Default = 0
  Global_CardMargin_Inner_Default = 25
  Global_BorderSize_Default = 124
#
Global_BorderPatten_Default = "solid"
Global_BorderLineSizeInner_Default = 10
Global_BorderLineSizeOuter_Default = 1
#
Global_CategoryFontSize = 50
Global_Linespacing_Default = 0.7
#
# this changes color of border based on card category
Global_CardBorderColorDict = {"Defense":"steelblue","Bribe":"yellow","Predator":"red","Weapon":"forestgreen","Xtras":"grey","Unknown":"lime"}
#-------------------------------------------------------------------------------



#-------------------------------------------------------------------------------
if (Global_flag_pdfcardprinter):
  # special settings for pdf output? want to change borders, etc?
  Global_CardFileExt = ".pdf"
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
    BuildCardImages()
#-------------------------------------------------------------------------------














#-------------------------------------------------------------------------------
def BuildCardImages():
    pobjcp = TJrPObjCollection()

    piecepath = os.getcwd()+"/cards/pieces"
    outpath = os.getcwd()+"/cards/outimages"
    backsourcefile = os.getcwd()+"/cards/specialimages/back.png"

    # path of images RELATIVE to .pieces file
    relativeimagedir = "../srcimages"

    print "Reading data from "+piecepath

    # find all card pieces files
    fmanp = pobjcp.get_filemanager()
    fmanp.ScanDirForFiles_CreateFileEntries(piecepath,1,"*.pieces",1)

    # create collection of objects from these files
    pobjcp.LoadObjectsFromFileManager(1)

    # Create image files
    BuildCardImagesFromObjManager(outpath,pobjcp,relativeimagedir)

    # Make special back image?
    ConvertImageToCardOutputImage(outpath+"/backs",backsourcefile,"BackImage")

#-------------------------------------------------------------------------------

























#-------------------------------------------------------------------------------
def BuildCardImagesFromObjManager(root,pobjcp,relativeimagedir):
    print "Generating images for "+str(pobjcp.get_count())+" pieces:"

    # walk through objects - we only make fronts
    pobjlist = pobjcp.get_pobjList()
    for pobj in pobjlist:
        BuildCardImageFromObj(root,pobj,relativeimagedir)

    print "Done creating images."
#-------------------------------------------------------------------------------



#-------------------------------------------------------------------------------
def BuildCardImageFromObj(root,pobj,relativeimagedir):
    # create image for object

    # we only do front image -- get the filename
    fname = pobj.get_propertyval("image.front")
    if (fname==""):
        # no image to create
        return

    # add image file format extension
    fname += Global_CardFileExt

    print "Creating "+fname+"."

    # fixup filename with full path
    fullfname = root+"/"+fname

    # create image file fullfname now
    img = CreateImageFileForCard_Front(pobj,relativeimagedir)

    # optional conversion of format before saving
    if (Global_SaveCardFormatConversion!=""):
        img=img.convert(Global_SaveCardFormatConversion)


    # now write it
    TJrPFileManager.EnsureFilePathExists(fullfname)
    # encoderconfig params are &quality, &progressive, &smooth, &optimize,
    img.save(fullfname,dpi=(Global_DPI,Global_DPI),resolution=Global_DPI,forceencoderconfig=(100,))

    #using my patch to PIL PdfImagePlugin to force a desired filter to avoid jpg artefacts:
    #img.save(fullfname,dpi=(Global_DPI,Global_DPI),resolution=Global_DPI,pdffilter="/ASCIIHexDecode")
    #img.save(fullfname,dpi=(Global_DPI,Global_DPI),resolution=Global_DPI,pdffilter="/RunLengthDecode")

    #separator for next call
    #print "\n"
#-------------------------------------------------------------------------------







#-------------------------------------------------------------------------------
def CreateImageFileForCard_Front(pobj,relativeimagedir):
    # create a PIL image object of the card

    # stuff we need
    width = int(Global_CardSize_Width)
    height = int(Global_CardSize_Height)
    cardcategory=pobj.get_propertyval("category")

    # defaults		
    marginsize=Global_CardMargin_Outer_Default
    bordersize=Global_BorderSize_Default
    borderpattern=Global_BorderPatten_Default


    # create new image
    cardimg = Image.new("RGBA" , [width,height], Global_CardBackgroundColor)


    # determine border color based on category
    bordercolordict=Global_CardBorderColorDict
    if (cardcategory in bordercolordict):
        bordercolor=bordercolordict[cardcategory]
    else:
        bordercolor=bordercolordict["Unknown"]


    # lets add a border?
    totalshave=marginsize+bordersize

    # new margin for future drawing
    margin = totalshave+Global_CardMargin_Inner_Default
    drawtop = margin
    drawbottom = height - margin


    # draw border color
    JrImp_DrawThickBorder(cardimg,marginsize,bordersize,bordercolor,borderpattern,Global_BorderLineSizeInner_Default,Global_BorderLineSizeOuter_Default)


    # title of card at top (default to cardtype if not specified)
    title = pobj.get_propertyval("title","")
    title=title.upper()
    maxfontsize=72
    minfontsize=14
    flag_fontallsamesize=1
    maxheight=(drawbottom-drawtop)/4
    textheight = JrImp_DrawText(1,"center",cardimg,"ariblk.ttf",maxfontsize,minfontsize,maxheight,flag_fontallsamesize,margin,width-margin,totalshave,title,"#000000",Global_Linespacing_Default)
    drawtop += textheight

    # category text?
    if (pobj.get_propertyval("value","")!="" and cardcategory!=""):
        # first get height
        maxfontsize=Global_CategoryFontSize
        minfontsize=Global_CategoryFontSize
        maxheight=(drawbottom-drawtop)/4
        flag_fontallsamesize=0
        textheight = JrImp_DrawText_Bottom(1,"center",cardimg,"arialbi.ttf",maxfontsize,minfontsize,maxheight,flag_fontallsamesize,margin,width-margin,drawbottom,cardcategory.upper(),"#333333",Global_Linespacing_Default)
        drawbottom -= int(textheight*1.8)

    # value as big number
    itext = pobj.get_propertyval("value","")
    if (itext!=""):
        # first get height
        maxfontsize=150
        minfontsize=150
        maxheight=(drawbottom-drawtop)/4
        flag_fontallsamesize=0
        textheight = JrImp_DrawText_Bottom(1,"center",cardimg,"ariblk.ttf",maxfontsize,minfontsize,maxheight,flag_fontallsamesize,margin,width-margin,drawbottom,itext,"#000000",Global_Linespacing_Default)
        drawbottom -= textheight

    # now let's add maybe a center image?
    srcimage = pobj.get_propertyval("image.src","")

    # path to images
    sourceimagepath = pobj.get_fullfdir()
    if (relativeimagedir != ""):
        sourceimagepath += "/"+relativeimagedir
    #print "Image path is: "+sourceimagepath

    if (srcimage!=""):
        centercardimagefname = sourceimagepath + "/"+srcimage
        if (os.path.isfile(centercardimagefname)):
            JrImp_CenterImageFileInRegion(cardimg,centercardimagefname,margin,drawtop,(width-margin),drawbottom,"true","false","noborder")


    # lastly, repeat value in upperleft
    itext = pobj.get_propertyval("value","")
    if (itext!=""):
        # first get height
        maxfontsize=60
        minfontsize=20
        bordercolor="#000000"
        JrImp_DrawText_InCircle(1,cardimg,width,height,"ariblk.ttf",maxfontsize,minfontsize,"left","top",80,40,5,itext,bordercolor,"#EEEEEE","#000000",Global_Linespacing_Default)


    # return image
    return cardimg
#-------------------------------------------------------------------------------






#-------------------------------------------------------------------------------
def ConvertImageToCardOutputImage(root,sourceimagefname,destimagefnamebase):
    # convert a special image to be the proper size for card full image
    # this is most useful for back images, etc.

    # add image file format extension
    fname = destimagefnamebase + Global_CardFileExt

    print "Convert Creating "+fname+"."

    # fixup filename with full path
    fullfname = root+"/"+fname

    # load image
    img = Image.open(sourceimagefname)

    # resize it
    img = img.resize((Global_CardSize_Width,Global_CardSize_Height), Image.ANTIALIAS )

    # optional conversion of format before saving
    if (Global_SaveCardFormatConversion!=""):
        img=img.convert(Global_SaveCardFormatConversion)

    # test force dpi?
    #img.encoderinfo.set("resolution", Global_DPI)

    # now write it
    TJrPFileManager.EnsureFilePathExists(fullfname)
    img.save(fullfname,dpi=(Global_DPI,Global_DPI),resolution=Global_DPI)

    #separator for next call
    #print "\n"
#-------------------------------------------------------------------------------






















#-------------------------------------------------------------------------------
if __name__ == "__main__":
    main()
#-------------------------------------------------------------------------------
