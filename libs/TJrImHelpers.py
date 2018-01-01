#-------------------------------------------------------------------------------
# TJRImHelpers
# This file defines functions to aid working with python PIL image module
# v1.5.01 by mouser@donationcoder.com, open source for personal use, license tbd
#-------------------------------------------------------------------------------
#!/usr/bin/env python

#-------------------------------------------------------------------------------
from TJrPFileClasses import *
#-------------------------------------------------------------------------------

#-------------------------------------------------------------------------------
import os, fnmatch
import datetime
import random
#
# PIL toolkit (http://www.pythonware.com/products/pil/)
#import Image
from PIL import Image
from PIL import ImageFile
from PIL import ImageDraw
from PIL import ImageFont
from PIL import ImageEnhance
#-------------------------------------------------------------------------------







#-------------------------------------------------------------------------------
def JrImp_ConvertFSlahes(fpath):
    return fpath.replace("\\","/")
#-------------------------------------------------------------------------------










#-------------------------------------------------------------------------------
def JrImp_ConvertUnitToPixels(val,unitstr,dpi):
    # convert a value into pixels
    if (unitstr=="pixels"):
        return val
    if (unitstr=="inches"):
        return float(val)*float(dpi);
    print "INTERNAL ERROR: In JrImp_ConvertUnitToPixels() -- unknown unitstring ["+unitstr+"]"
    return val
#-------------------------------------------------------------------------------









#-------------------------------------------------------------------------------
def JrImp_LayoutImagePagesFromPath(imagepath,flag_recurse,filepatterns, outpath,outfnameprefix,outfnameext,printdetails):
    # assemble cards onto pages

    # first get list of all matching image files
    fmanp = TJrPFileManager()
    fogenerator = fmanp.ScanDirForFiles_GetFileList(imagepath,flag_recurse,filepatterns)
    flist=[]
    for fname in fogenerator:
        flist.append(fname)

    # now ask to print these images
    JrImp_LayoutImagePagesFromList(flist,outpath,outfnameprefix,outfnameext, printdetails)
#-------------------------------------------------------------------------------



#-------------------------------------------------------------------------------
def JrImp_ConvertPrintDetailsUnitsToPixels(printdetails):
    units = printdetails["Units"]
    dpi = printdetails["DPI"]
    #
    printdetails["LabelHeight"]=JrImp_ConvertUnitToPixels(printdetails["LabelHeight"],units,dpi)
    printdetails["LabelWidth"]=JrImp_ConvertUnitToPixels(printdetails["LabelWidth"],units,dpi)
    printdetails["SpacingHorizontal"]=JrImp_ConvertUnitToPixels(printdetails["SpacingHorizontal"],units,dpi)
    printdetails["SpacingVertical"]=JrImp_ConvertUnitToPixels(printdetails["SpacingVertical"],units,dpi)
    printdetails["ImageMargin"]=JrImp_ConvertUnitToPixels(printdetails["ImageMargin"],units,dpi)
    printdetails["OffsetX"]=JrImp_ConvertUnitToPixels(printdetails["OffsetX"],units,dpi)
    printdetails["OffsetY"]=JrImp_ConvertUnitToPixels(printdetails["OffsetY"],units,dpi)
    printdetails["PageWidth"]=JrImp_ConvertUnitToPixels(printdetails["PageWidth"],units,dpi)
    printdetails["PageHeight"]=JrImp_ConvertUnitToPixels(printdetails["PageHeight"],units,dpi)
    printdetails["PageCrop"]=JrImp_ConvertUnitToPixels(printdetails["PageCrop"],units,dpi)
    # all converted, so make sure we remember it is already converted
    printdetails["Units"]="pixels"
    units = printdetails["Units"]

    # handle landscape fix
    if (printdetails["PageOrientation"]=="landscape"):
        # flip properties
        printdetails["LabelHeight"],printdetails["LabelWidth"] = printdetails["LabelWidth"],printdetails["LabelHeight"]
        printdetails["SpacingHorizontal"],printdetails["SpacingVertical"]=printdetails["SpacingVertical"],printdetails["SpacingHorizontal"]
        printdetails["CountVertical"],printdetails["CountHorizontal"]=printdetails["CountHorizontal"],printdetails["CountVertical"]
        printdetails["OffsetX"],printdetails["OffsetY"]=printdetails["OffsetY"],printdetails["OffsetX"]
        printdetails["PageWidth"],printdetails["PageHeight"]=printdetails["PageHeight"],printdetails["PageWidth"]
        printdetails["PageOrientation"]="portrait"
#-------------------------------------------------------------------------------



#-------------------------------------------------------------------------------
def JrImp_LayoutImagePagesFromList(flist,outpath,outfnameprefix,outfnameext, printdetails):
    # layout image on output files

    # make output directory if it doesnt exist
    if not os.path.exists(outpath):
        os.makedirs(outpath)

    # first convert measurements to pixels
    JrImp_ConvertPrintDetailsUnitsToPixels(printdetails)

    # some details
    labelsperpage = printdetails["CountVertical"] * printdetails["CountHorizontal"]
    flistlen = len(flist)

    # now loop pages and print each one
    pageindex=0
    while (1):
        pageimagelist=[]
        findex_start=pageindex * labelsperpage
        for i in range(0,labelsperpage):
            findex = findex_start + i
            if (findex<flistlen):
                pageimagelist.append(flist[findex])
        if (len(pageimagelist)==0):
            # all done no more images
            break
        # ok we have one page of at least one image
        pagenumstr = "%03d" % (pageindex+1)
        pagefilename = outpath +"/"+outfnameprefix+pagenumstr+outfnameext
        print "Creating page "+pagenumstr
        JrImp_LayoutOneImagePageFromList(pageimagelist,pagefilename, printdetails)
        # loop to next page
        pageindex += 1
#-------------------------------------------------------------------------------









#-------------------------------------------------------------------------------
def JrImp_LayoutOneImagePageFromList(flist,outfname, printdetails):
    # layout images one a page and save that page file image
    # NOTE: You need to use a photo printing program that is willing to use the full page size of an image, and essentially crop out margins (Paint Shop Pro not irfanview)

    #print "TEST flist is "+ str(flist)

    # we will walk horizontally then vertically through labels on the page, filling them sequentially
    flistlen = len(flist)
    findex = 0
    hcount = printdetails["CountHorizontal"]
    vcount = printdetails["CountVertical"]

    # create blank image page of correct size
    xwidth = int(printdetails["PageWidth"])
    yheight = int(printdetails["PageHeight"])
    pageimg = Image.new("RGBA" , [int(xwidth),int(yheight)], printdetails["BackgroundColor"])
    #
    lwidth = int(printdetails["LabelWidth"])
    lheight = int(printdetails["LabelHeight"])
    hspace = int(printdetails["SpacingHorizontal"])
    vspace = int(printdetails["SpacingVertical"])
    xoff = int(printdetails["OffsetX"])
    yoff = int(printdetails["OffsetY"])
    dpival = int(printdetails["DPI"])
    #
    ShowCardCuts = printdetails["ShowCardCuts"]

    #print "In fopen loop."

    for ix in range(0,hcount):
        for iy in range(0,vcount):
            if (findex>=flistlen):
                # no more images, just loop and do nothing
                continue
            # image file that will display at this location
            fname = flist[findex][1]
            # calc pixel upper left of grid label location ix,iy
            x = int(xoff + ix*(hspace))
            y = int(yoff + iy*(vspace))
            # frame location (card cutting location)
            framesx = x
            framesy = y
            frameex = framesx+lwidth
            frameey = framesy+lheight
            # now display image on page
            #print "ABOUT TO OPEN IMAGE NAME: " + str(fname)
            img = Image.open(fname)

            # resize it for label frame
            # this should be done with dif options regarding aspect ratio and then adjust x and y offset based on this
            img = JrImp_SmartImgFit_PrintDetails(img,lwidth,lheight,printdetails)

            # get resized width+height
            rwidth,rheight = img.size
            # center it within area
            x+=int((lwidth-rwidth)/2)
            y+=int((lheight-rheight)/2)

            #print "Displaying at "+str(x)+","+str(y)+" ["+outfname+"]:"

            # ensure its got transparency layer for paste
            img=img.convert("RGBA")

            #print fname
            pageimg.paste(img, (x,y),img)

            # card frame
            if (ShowCardCuts):
                JrImp_DrawRect(pageimg,framesx,framesy,frameex,frameey,1,"gray","dotted")

            # move to next image
            findex+=1

    # post-crop page (for image printing to avoid full-bleed requirement)
    if ("PageCrop" in printdetails and printdetails["PageCrop"]>0):
        cropsize = int(printdetails["PageCrop"])
        pageimg = pageimg.crop((cropsize,cropsize,xwidth-cropsize,yheight-cropsize))

    # remove transparency
    pageimg=pageimg.convert("RGB")

    # ok now write output image
    pageimg.save(outfname,dpi=(dpival,dpival),resolution=dpival)

#-------------------------------------------------------------------------------


#-------------------------------------------------------------------------------
def JrImp_SmartImgFit_PrintDetails(img,lwidth,lheight,printdetails):
    # resize, autorotate, obey aspect parameter
    #printdetails["AutoRotate"]="true"
    #printdetails["PreserveAspect"]="true"

    autorotate = printdetails["AutoRotate"]
    preserveaspect = printdetails["PreserveAspect"]
    imagemargin = printdetails["ImageMargin"]

    lwidth-=imagemargin*2
    lheight-=imagemargin*2

    return JrImp_SmartImgFit(img,lwidth,lheight,preserveaspect,autorotate)
#-------------------------------------------------------------------------------




#-------------------------------------------------------------------------------
def JrImp_SmartImgFit(img,lwidth,lheight,preserveaspect,autorotate):
    # resize to fit inside a desired size
    rwidth,rheight = img.size
    imgwide = rwidth >= rheight
    framewide = lwidth >= lheight

    if (rwidth<=0 or rheight<=0):
        return img

    if (autorotate=="true"):
        # rotate if opposite aspect than frame
        if (imgwide != framewide):
            # rotate
            img = img.transpose(Image.ROTATE_90)
            rwidth,rheight = img.size

    targetwidth = int(lwidth)
    targetheight = int(lheight)
    if (preserveaspect=="true"):
        # resize and preserve aspect
        deltaxp = float(targetwidth)/float(rwidth)
        deltayp = float(targetheight)/float(rheight)
        minzoom=min(deltaxp,deltayp)
        maxzoom=max(deltaxp,deltayp)
        zoomlevel=minzoom
#        if (minzoom<=1):
#            zoomlevel=minzoom
#        else:
#            zoomlevel=maxzoom
        targetwidth=int(float(rwidth)*zoomlevel)
        targetheight=int(float(rheight)*zoomlevel)

    img = img.resize((targetwidth,targetheight), Image.ANTIALIAS )
    return img
#-------------------------------------------------------------------------------

































#-------------------------------------------------------------------------------
def JrImp_CenterImageFileInRegion(img,fname,left,top,right,bottom,preserveaspect,autorotate,bordermode):
    # load the file

    lwidth = right-left
    lheight = bottom-top
    #
    subimage = Image.open(fname)
    subimage = subimage.convert('RGBA')
    subimage = JrImp_SmartImgFit(subimage,lwidth,lheight,preserveaspect,autorotate)
    #
    rwidth,rheight = subimage.size
    xoff = int((lwidth-rwidth)/2)
    yoff = int((lheight-rheight)/2)
    #
    # now center and paste it
    # third parameter pastes with transparency effect
    img.paste(subimage, (left+xoff,top+yoff),subimage)

    if (bordermode=="single"):
        drawimg = ImageDraw.Draw(img)
        drawimg.rectangle([left+xoff,top+yoff,left+xoff+rwidth,top+yoff+rheight],outline="#000000")


    if (bordermode=="test"):
        drawimg = ImageDraw.Draw(img)
        drawimg.rectangle([left+0,top+0,right,bottom],outline="#111111")


#-------------------------------------------------------------------------------















#-------------------------------------------------------------------------------
def JrImp_DrawThickBorder(img,marginsize,bordersize,bordercolor,borderpattern,blackedgethickness_inner,blackedgethickness_outer):
    # draw a thick border
    drawimg = ImageDraw.Draw(img)
    width,height = img.size
    for i in range(marginsize,marginsize+bordersize):
        if ( (blackedgethickness_outer>0 and i<marginsize+blackedgethickness_outer) or (blackedgethickness_inner>0 and i>=marginsize+bordersize-blackedgethickness_inner) ):
            drawimg.rectangle([i,i,width-(i+1),height-(i+1)],outline="#000000")
        elif (i%2!=0 and borderpattern!="solid"):
            continue
        else:
            drawimg.rectangle([i,i,width-(i+1),height-(i+1)],outline=bordercolor)
    del drawimg



def JrImp_DrawRect(img,sx,sy,ex,ey,thickness,bordercolor,borderpattern_unused):
    # draw a thick border
    drawimg = ImageDraw.Draw(img)
    width,height = img.size
    for i in range(0,thickness):
        drawimg.rectangle([sx+i,sy+i,ex-i,ey-i],outline=bordercolor)
    del drawimg
#-------------------------------------------------------------------------------







#-------------------------------------------------------------------------------
def JrImp_DrawText(flag_doactuallydraw,halign,img,fontname,infontsize,inminfontsize,inmaxheight,flag_fontallsamesize,left,right,intop,alltextstr,textcolor,linespacing):
    # draw some text centered horizontally
    # returns new HEIGHT of the written text

    # try to fix up font path
    # the PIL font loader will search this directory anyway, but gives an annoying warning, so we try to bypass warning with a guess if its easy
    fontdir = "C:\\Windows\\Fonts\\"
    if (os.path.exists(fontdir+fontname)):
        fontname = fontdir+fontname

    imgdraw = ImageDraw.Draw(img)

    fontheightfactor = 1.25

    # we do in two parts
    # 1. first we create text lines (which may be wrapped) and font size for each line
    # 2. and then we render

    # 1. determine font sizes and lines
    loopcount = 0
    startfontsize = infontsize
    while (1):
        # try to find lines and font sizes
        # each loop is a try using a different base font size
        alltextstr = alltextstr.replace("\n","\\n")
        textlines = alltextstr.split("\\n")
        linesout = list()
        needsreloop = 0
        top=intop
        lineindex = 0
        linecount = len(textlines)

        for textstrtry in textlines:
            fontsize = startfontsize
            topstart=top
            islastline = lineindex>=linecount-1
            lineindex = lineindex + 1
            #
            while (1):
                textstr = textstrtry
                top = topstart
                textfont = ImageFont.truetype(fontname, fontsize)

                remainderstr=""
                fontimgsize = 0
                fontimgwidth = 0
                fontimgheight = 0

                didwrapline = False
                while (1):
                    fontimgsize = textfont.getsize(textstr)
                    fontimgwidth = fontimgsize[0]
                    fontimgheight = int(fontimgsize[1] / fontheightfactor)

                    if (fontimgwidth<right-left):
                        # it fits, so add it
                        lineitem = (textstr,fontsize,fontimgwidth,fontimgheight)
                        linesout.append(lineitem)
                        top += int(fontimgheight*linespacing)
                        # ok now move to remainder
                        textstr=remainderstr
                        remainderstr=""
                        #del textfont
                        #break
                    else:
                        # does not fit, try to move some of textstr to remainderstr
                        oldtextstr=textstr
                        textstr,remainderstr = JrImp_WrapText(textstr,remainderstr)
                        if (textstr==oldtextstr):
                            # couldnt wrap
                            break
                        didwrapline = True
                    if (textstr==""):
                        break

                if (didwrapline and not islastline):
                        # add separator
                        lineitem = ("",fontsize,fontimgwidth,fontimgheight)
                        linesout.append(lineitem)
                        top += int(fontimgheight*linespacing)

                if (remainderstr=="" and textstr==""):
                    # done and success
                    break

                # doesnt fit
                # should we try to word wrap?
                # ATTN: unfinished

                del textfont
                # reduce font size and try again?
                if (flag_fontallsamesize==1):
                    # we must break and start EVERYONE over at smaller font size
                    needsreloop=1
                    break
                if (fontsize<inminfontsize):
                    # font too small, so stop
                    needsreloop=1
                    break
                fontsize -= 1

            if (needsreloop==1):
                break

        # we did all lines, but is it too tall
        if (((top-intop)>inmaxheight) and startfontsize>inminfontsize):
            # lets try again with smaller font
            needsreloop=1
        if ((needsreloop==0) or (startfontsize<=inminfontsize)):
            # all done
            break
        # lets try again with smaller font
        startfontsize -= 1

    # 2. done dermining sizes, now render
    if (flag_doactuallydraw==1):
        top=intop
        for outitems in linesout:
            textstr,fontsize,fontimgwidth,fontimgheight = outitems
            #print "text="+textstr+" fontsize = "+str(fontsize)
            textfont = ImageFont.truetype(fontname, fontsize)
            if (halign=="center"):
                leftoffset = int(((right-left)-fontimgwidth)/2)
                imgdraw.text((left+leftoffset,top),textstr,font=textfont,fill=textcolor)
            elif (halign=="right"):
                leftoffset = int(((right)-fontimgwidth))
                imgdraw.text((leftoffset,top),textstr,font=textfont,fill=textcolor)
            else:
                imgdraw.text((left,top),textstr,font=textfont,fill=textcolor)
            del textfont
            top += int(fontimgheight*linespacing)


    del imgdraw

    # return height of text
    return (top-intop)
#-------------------------------------------------------------------------------




#-------------------------------------------------------------------------------
def JrImp_DrawText_Bottom(flag_doactuallydraw,halign,img,fontname,infontsize,inminfontsize,inmaxheight,flag_fontallsamesize,left,right,bottom,alltextstr,textcolor,linespacing):
    # first ask normal draw to get us height
    textheight = JrImp_DrawText(0,halign,img,fontname,infontsize,inminfontsize,inmaxheight,flag_fontallsamesize,left,right,bottom,alltextstr,textcolor,linespacing)
    JrImp_DrawText(1,halign,img,fontname,infontsize,inminfontsize,inmaxheight,flag_fontallsamesize,left,right,bottom-textheight,alltextstr,textcolor,linespacing)
    return textheight


def JrImp_DrawText_Center(flag_doactuallydraw,halign,img,fontname,infontsize,inminfontsize,inmaxheight,flag_fontallsamesize,left,right,centery,alltextstr,textcolor,linespacing):
    # first ask normal draw to get us height
    textheight = JrImp_DrawText(0,halign,img,fontname,infontsize,inminfontsize,inmaxheight,flag_fontallsamesize,left,right,centery,alltextstr,textcolor,linespacing)
    JrImp_DrawText(1,halign,img,fontname,infontsize,inminfontsize,inmaxheight,flag_fontallsamesize,left,right,centery-(textheight/1.35),alltextstr,textcolor,linespacing)
    return textheight
#-------------------------------------------------------------------------------




#-------------------------------------------------------------------------------
def JrImp_WrapText(textstr,remainderstr):
    # return 2-tuple of new values for textstr,remainderstr
    # in simplest case, take last word of textstr and add it to start of remainderstr
    # if no natural word-wrap position in textstr, trying hyphenating?
    newstr,rightword = JrImp_RemoveRightWord(textstr)
    if (remainderstr!=""):
        remainderstr = rightword + " " + remainderstr
    else:
        remainderstr = rightword

    #print "Split: "+textstr+ " into ("+newstr+","+remainderstr+")"

    return newstr,remainderstr


def JrImp_RemoveRightWord(str):
    # strip off last word at whitespace or punctuation
    # return tuple of strippped str and rightword
    endpos = len(str)-2
    splitchars = [' ',',','.',':','-','=',';']
    rightword = ""
    for i in range(endpos,0,-1):
        c = str[i]
        if (c in splitchars):
            rightword = str[i+1:]
            str = str[0:i]
            break
    if (rightword==""):
        rightword=str
        str=""
    return str,rightword
#-------------------------------------------------------------------------------


















#-------------------------------------------------------------------------------
def JrImp_DrawText_InCircle(flag_drawcircle,img,width,height,fontname,infontsize,inminfontsize,halign,valign,inmargin,radius,circlethickness,itext,bordercolor,fillcolor,textcolor,linespacing):
    # draw text in a circle somewhere around border

    # try to fix up font path
    # the PIL font loader will search this directory anyway, but gives an annoying warning, so we try to bypass warning with a guess if its easy
    fontdir = "C:\\Windows\\Fonts\\"
    if (os.path.exists(fontdir+fontname)):
        fontname = fontdir+fontname

    # determine center location of circle
    if (halign=="left"):
        xpos = 0+(inmargin+radius)
    elif (halign=="right"):
        xpos = width-(inmargin+radius)
    if (valign=="top"):
        ypos = 0+(inmargin+radius)
    elif (valign=="bottom"):
        ypos = height-(inmargin+radius)

    # draw circle
    if (flag_drawcircle==1):
        imgdraw = ImageDraw.Draw(img)
        #
        # draw circle
        if (circlethickness<=0):
            imgdraw.ellipse((xpos-radius,ypos-radius,xpos+radius,ypos+radius),fillcolor)
        elif (circlethickness==1):
            imgdraw.ellipse((xpos-radius,ypos-radius,xpos+radius,ypos+radius),fillcolor,bordercolor)
        else:
            imgdraw.ellipse((xpos-radius,ypos-radius,xpos+radius,ypos+radius),bordercolor)
            imgdraw.ellipse((xpos-(radius-circlethickness),ypos-(radius-circlethickness),xpos+(radius-circlethickness),ypos+(radius-circlethickness)),fillcolor)


    # draw text
    radiustextsizemultiplier = 0.85
    JrImp_DrawText_Center(1,"center",img,fontname,infontsize,inminfontsize,radius*2,1,xpos-(radius*radiustextsizemultiplier-circlethickness),xpos+(radius*radiustextsizemultiplier-circlethickness),ypos,itext,textcolor,linespacing)

    del imgdraw
#-------------------------------------------------------------------------------



