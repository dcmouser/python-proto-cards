#-------------------------------------------------------------------------------
# TJrPFileClasses
# This file defines some classes for working with a simple kind of data
#  files, reading and writing them.
# v1.03.01 by mouser@donationcoder.com, open source for personal use, license tbd
#-------------------------------------------------------------------------------
#!/usr/bin/env python


#-------------------------------------------------------------------------------
import os, fnmatch
import datetime
import random
import subprocess
import copy
import re
import json
#-------------------------------------------------------------------------------

#-------------------------------------------------------------------------------
from titlecase import titlecase
#-------------------------------------------------------------------------------



#---------------------------------------------------------------------------
# TJrPFileEntry represents a file object which is normally simply used to read or write file contents
class TJrPFileEntry(object):

    def __init__(self):
        self.fname = ""
        self.froot = ""
        self.fcontents = []
        self.filep = 0
        self.fcontents_loaded = 0

    def GetFileContents(self):
        if (self.fcontents_loaded==0):
            self.ReadFileContents()
        return self.fcontents
    def SetFileContents(self,str):
        self.fcontents = str
    def AddLineToFileContents(self,str):
        self.fcontents.append(str)
    def AddLineListToFileContents(self,slist):
        for oneline in slist:
            self.fcontents.append(oneline)
    def AddSeparatorLineToFileContents(self):
        self.fcontents.append("--\n")
    def get_fname(self):
        return self.fname
    def set_fname(self,in_fname):
        self.fname=in_fname
    def get_froot(self):
        return self.froot
    def set_froot(self,in_froot):
        self.froot=in_froot

    def ReadFileContents(self):
        self.OpenFile("r")
        if (self.filep!=0):
            try:
                self.fcontents = self.filep.readlines()
            finally:
                self.CloseFile()
            self.fcontents_loaded = 1

    def WriteFileContents(self,in_froot):
        self.froot=in_froot
        self.OpenFile("w")
        try:
            self.filep.writelines(self.fcontents)
        finally:
            self.CloseFile()
    def OpenFile(self,modestr):
        self.CloseFile()
        if (self.froot!=""):
            fullfname=self.froot+"/"+self.fname
        else:
            fullfname=self.fname
        if (modestr=="w" or modestr=="a" or os.path.isfile(fullfname)):
            TJrPFileManager.EnsureFilePathExists(fullfname)
            self.filep = open(fullfname,modestr)
        else:
            self.filep = 0
    def CloseFile(self):
        if (self.filep!=0):
            self.filep.close()
        self.filep=0
    def ClearFileContents(self):
        # delete all lines in file following initial comments
        self.GetFileContents()
        self.CloseFile()
        newcontents = []
        for oneline in self.fcontents:
            if (oneline != "" and oneline[0]!='/' and oneline!="\n"):
                break;
            newcontents.append(oneline)
        self.fcontents = newcontents

#---------------------------------------------------------------------------



#---------------------------------------------------------------------------

# TJrMultiFileManager manages a collection of files, either for reading from many files or for writing to many of them
class TJrPFileManager(object):

    def __init__(self):
        self.pFileList = []

    def get_pFileList(self):
        return self.pFileList

    # call this to get a list of matching files (root is base directory, filepatterns are ; separated file masks
    def ScanDirForFiles_GetFileList(self,rootstr,flagrecurse,filepatterns):
        patterns = filepatterns.split(';')
        roots = rootstr.split(';')
        for root in roots:
            for path, subdirs, files in os.walk(root):
                files.sort()
                for name in files:
                    for pattern in patterns:
                        if fnmatch.fnmatch(name, pattern):
                            yield root , os.path.join(path, name)
                            break
                if (flagrecurse==0):
                    break

    def ScanDirForFiles_CreateFileEntries(self,root,flagrecurse,filepatterns, clearfirst):
        if (clearfirst==1):
            self.pFileList = []
        fogenerator = self.ScanDirForFiles_GetFileList(root,flagrecurse,filepatterns)
        for froot,fname in fogenerator:
            newfobj = TJrPFileEntry()
            newfobj.set_fname(JrP_RemoveRootFromFilename(fname,froot))
            newfobj.set_froot(froot)
            self.pFileList.append(newfobj)
        return self.pFileList

    def CloseAndClearFiles(self):
        for fobj in self.pFileList:
            fobj.CloseFile()
   	    self.pFileList = []
    def WriteAllFiles(self,root):
        for fobj in self.pFileList:
            fobj.WriteFileContents(root)

    def FindFileByName(self,fname,flag_createifmissing):
        for fobj in self.pFileList:
            if (fobj.get_fname()==fname):
                #print "FOUND "+fname
                return fobj
        # not found, create it
        if (flag_createifmissing==1):
            newfobj = TJrPFileEntry()
            newfobj.set_fname(fname)
            self.pFileList.append(newfobj)
            #print "CREATING "+fname
            return newfobj
        # not found, return 0
        return 0

    def SplitFilename(fname):
        # return 3-tuple with path, basename, extension
        path = ""
        basename = ""
        extension = ""
        slen = len(fname)
        extensionpos=len
        lastslashpos=-1
        for i in range(slen-1,0,-1):
            c = fname[i]
            if (c=='.'):
                extensionpos=i;
            if (c=='/' or c=='\\'):
                lastslashpos=i
                break
        if (extensionpos<len):
            extension=fname[extensionpos+1:]
            fname = fname[0:extensionpos]
        if (lastslashpos>0):
            path = fname[0:lastslashpos]
            basename = fname[lastslashpos+1:]
        return path,basename,extension
    SplitFilename = staticmethod(SplitFilename)

    def EnsureFilePathExists(filepath):
        # create the directory tree if it doesnt exist
        d = os.path.dirname(filepath)
        if not os.path.exists(d):
            os.makedirs(d)
    EnsureFilePathExists = staticmethod(EnsureFilePathExists)



    def AddStringToFilenameBeforeExtension(fullfname, addstr):
        # split filename into basename and extension
        (path, basename, extension) = TJrPFileManager.SplitFilename(fullfname)
        outfname = path + "/" + basename + addstr + "." + extension
        return outfname
    AddStringToFilenameBeforeExtension = staticmethod(AddStringToFilenameBeforeExtension)
#---------------------------------------------------------------------------





#---------------------------------------------------------------------------

# TJrPObj stores information for one object, typically an associative array of [property,value] tuples
class TJrPObj(object):

    def __init__(self,dict_in={}):
        self.propertyDict = {"__file":"","__dir":""}
        self.propertyDict.update(dict_in)

    def add_propertyval(self,propertyname,propertyval):
        self.propertyDict[propertyname]=propertyval

    def addto_propertyval(self,propertyname,propertyval,separator="\n"):
        # add it with separator
        if propertyname in self.propertyDict:
            str = self.get_propertyval(propertyname)+separator+propertyval
        else:
            str = propertyval
        self.propertyDict[propertyname]=str

    def get_propertyval(self,propertyname,defaultval=""):
        if (not propertyname in self.propertyDict):
            return defaultval
        return self.propertyDict[propertyname]


    def get_propertyval_asint(self,propertyname,defaultval=""):
        if (not propertyname in self.propertyDict):
            return defaultval
        return int(self.propertyDict[propertyname])

    def get_propertyvaldict(self,propertyname):
        retdict={}
        for key in self.propertyDict:
            if (key.find(propertyname+".")!=0):
                continue
            propsubname=key[len(propertyname)+1:len(key)+1]
            retdict[propsubname]=self.propertyDict[key]
        return retdict

    def get_propertyvaldict_astext(self,propertyname,keyseparator=" = ",lineseparator="\n",flag_sorted=1):
        retdict = self.get_propertyvaldict(propertyname)
        if (len(retdict)==0):
            return ""
        retlines = []
        rettext = ""
        for key,val in retdict.iteritems():
            if (val==''):
                str = key
            else:
                str = key+keyseparator+val
            retlines.append(str)
        if (flag_sorted==1):
            retlines.sort()
        for aline in retlines:
            if (rettext!=""):
                rettext+=lineseparator
            rettext += aline
        return rettext

    def set_dictcontents(self,dict_in):
        # note that this is a SHALLOW copy (references)
        self.propertyDict=dict_in

    def GetDictAsContentsList(self):
        slist = list()
        for key in self.propertyDict:
            if ( len(key)>2 and key[0]=='_' and key[1]=='_'):
                continue
            astr = "@"+str(key)+"="+str(self.propertyDict[key])+"\n"
            slist.append(astr)
        # sort before returning
        slist.sort()
        return slist

    def DoesDictItemExist(self,propertyname):
        if (propertyname in self.propertyDict):
            return 1
        return 0

    def get_fullfdir(self):
        # return full path to the directory of the piece file containing this
        return self.get_propertyval("__dir","")

    def CopyFrom(self,otherobj):
        # copy dictionary from another
        #self.set_dictcontents(otherobj.propertyDict)
        self.set_dictcontents(copy.deepcopy(otherobj.propertyDict))

    def DebugObject(self):
        print "\nDumping object:"
        for key in self.propertyDict:
            print key + " = " + self.propertyDict[key]
#---------------------------------------------------------------------------



#---------------------------------------------------------------------------

# TJrPObjCollection is a collection of TJrPObj objects and some helper functions for working with them
class TJrPObjCollection(object):

    def __init__(self):
        self.pobjList = []
        self.pfilemanager = TJrPFileManager()
        self.counterdict = {}

    def AddObject(self,pobj):
        self.pobjList.append(pobj)

    def WriteObjectOutputFiles(self,rootpath,flag_clearfilecontents):
        flist = list()
        for pobj in self.pobjList:
            fname = pobj.get_propertyval("__file")
            #print "OBJECT TO FILE "+fname
            if (fname==""):
                continue
            fullfname = rootpath + "/"+fname
            pcontentslist = pobj.GetDictAsContentsList()
            fobj = self.pfilemanager.FindFileByName(fname,1)
            if (flag_clearfilecontents==1 and flist.count(fname)==0):
                # not yet used so clear it and add to our used filelist
                fobj.ClearFileContents();
                flist.append(fname)
            fobj.AddLineListToFileContents(pcontentslist)
            fobj.AddSeparatorLineToFileContents()
        self.pfilemanager.WriteAllFiles(rootpath)
        self.pfilemanager.CloseAndClearFiles()

    def LoadObjectsFromFileManager(self,clearfirst):
        # use the filemanager to load in all objects
        if (clearfirst):
            self.pobjList = []
        for fobj in self.pfilemanager.get_pFileList():
            self.AddLoadObjectsFromFileObj(fobj)

    def AddLoadObjectsFromFileObj(self,fobj):
        # add all objects found in a file
        self.AddLoadObjectsFromContentsList(fobj.GetFileContents(),fobj.get_fname(),fobj.get_froot())

    def AddLoadObjectsFromContentsList(self,fcontents,fname,froot):
        # add all objects found in a file
        lastpropname = ""
        lastobj = 0
        fcontents.append("---")
        lineindex = 0
        #print fname
        #print froot
        for aline in fcontents:
            #print aline
            lineindex = lineindex+1
            aline = aline.strip()
            if (len(aline)==0):
                continue
            elif (aline[0]=='/'):
                continue
            elif (aline[0]=='-'):
                # ok a separator, so maybe add last object we were working on
                if (lastpropname==""):
                    continue
                # non-empty object, add filename
                if (fname!=""):
                    lastobj.add_propertyval("__file",fname)
                    odir = os.path.dirname(fname)
                    if (odir!=""):
                        odir=froot+"/"+odir
                    else:
                        odir=froot
                    lastobj.add_propertyval("__dir",odir)
                # add it and clear it
                self.AddObject(lastobj)
                lastpropname = ""
            elif (aline[0]=='@'):
                # a new property, create an object if we arent already working on one
                propname,propval = self.ParsePropLine(aline)
                if (propname==""):
                    continue
                if (lastpropname==""):
                    lastobj = TJrPObj()
                lastpropname=propname
                lastobj.add_propertyval(propname,propval)
            else:
                # ok its something else, so we treat it as continuation of last property with \n separator, OR error
                if (lastpropname==""):
                    # error
                    print "ERROR: Line ["+str(lineindex)+"] of file ("+fname+"), reading into object data and got line that was not understood."
                lastobj.addto_propertyval(lastpropname,aline)

    def ParsePropLine(self,aline):
        # return tuple of line parsed into @PROP=VAL
        if (aline[0]=='@'):
            aline = aline[1:len(aline)].strip()
        epos = aline.find("=")
        if (epos==-1):
            return (aline,"")
        propname = aline[0:epos].strip()
        propval = aline[epos+1:len(aline)].strip()
        return (propname,propval)

    def get_objectcount(self):
        return len(self.pobjList)
    def get_pobjList(self):
        return self.pobjList
    def get_filemanager(self):
        return self.pfilemanager

    def AddFileComment(self,fname,commentstr):
        commentstr = "// "+commentstr+"\n";
        fobj = self.pfilemanager.FindFileByName(fname,1)
        fobj.AddLineListToFileContents(commentstr)

    def AddFileComment_WithDate(self,fname,commentstr):
        commentstr = "// "+commentstr;
        commentstr += " ["+(datetime.datetime.now()).strftime('%Y-%m-%d')+"]"+"\n\n"
        fobj = self.pfilemanager.FindFileByName(fname,1)
        fobj.AddLineListToFileContents(commentstr)

    def GetCounter(self,tagstr,includetag):
        # keep unique counters indexed by tag, useful for nicefilenames
        if tagstr in self.counterdict:
            curvalue=self.counterdict[tagstr]+1
        else:
            curvalue=1
        self.counterdict[tagstr]=curvalue
        if (includetag==0):
            return curvalue
        curvalstr = "%03d" % curvalue
        return tagstr+"_"+curvalstr

    def get_count(self):
        return len(self.pobjList)

    def DebugDump(self):
        print "# of objects: "+str(len(self.pobjList))

    def FindObjectByFields(self,fdict):
        # return object (pointer) if one matches all dict items
        for pobj in self.pobjList:
            failedmatch = 0
            for dkey in fdict:
                if (pobj.DoesDictItemExist(dkey)==0 or pobj.propertyDict[dkey]!=fdict[dkey]):
                    failedmatch = 1
#                    if (pobj.DoesDictItemExist(dkey)==0):
#                        print "Existing object has no val for "+dkey+"."
#                    else:
#                        print "Existing object value for field is "+pobj.propertyDict[dkey]+"."
                    break

            if (failedmatch==0):
                # got a match, return it
                return pobj
        # no match
        return None


    def ExportToJson(self,outfname):
        # write all objects to a json file
        filep = open(outfname,"w")
        flist = list()
        outcount = 0
        filep.writelines('[\n')
        for pobj in self.pobjList:
            #objectfname = pobj.get_propertyval("__file")
            #pcontentslist = pobj.GetDictAsContentsList()
            odict = pobj.propertyDict
            #
            # ATTN: test, modify some stuff
            for k in odict.keys():
                if k.startswith('__'):
                    odict.pop(k)
            #
            del odict['image.src'];
            odict['image.front']='outimages/' + odict['image.front']+'.png';
            odict['image.back']='outimages/backs/BackImage.png';
            imagedict = {'front':odict['image.front'],'back':odict['image.back']};
            del odict['image.front'];
            del odict['image.back'];
            odict['image']=imagedict;

            #
            if outcount>0:
                filep.writelines('')
                filep.writelines('\n,\n')
                filep.writelines('')
            #
            outcount = outcount + 1
            json.dump(odict,filep,indent=4)
            #filep.writelines(pcontentslist)

        filep.writelines('\n]\n')
        filep.close()
#---------------------------------------------------------------------------





















#---------------------------------------------------------------------------
# Choose an item from a list using weighted info, either randomly or proportionately sequentially
def JrP_ChooseWeighted(probdict,index,minindex,maxindex,flagsequentially):
    if (flagsequentially==0):
        return JrP_ChooseWeightedProbability(probdict)
    return JrP_ChooseWeightedSequence(probdict,index,minindex,maxindex)


# Choose an item from a weighted probability list
def JrP_ChooseWeightedProbability(probdict):
    # first normalize to cumulative values
    ctotal = 0.0
    indexcount = 0
    for key, pvalue in probdict.iteritems():
        indexcount+=1
        ctotal+=pvalue
    if (ctotal<=0.0):
        return ""
    # now choose uniform random number from 0 to 1
    rval = random.uniform(0,1)
    # normalize it
    rvalnorm = rval * ctotal
    # now find it via roulette wheel
    rtotal = 0.0
    for key, pvalue in probdict.iteritems():
        indexcount-=1
        rtotal+=pvalue
        if (rtotal>=rvalnorm or indexcount==0):
            return key
    # we should never get to here
    return ""


# Choose an item from a list proportionately based on index
def JrP_ChooseWeightedSequence(probdict,index,minindex,maxindex):
    # first normalize to cumulative values
    ctotal = 0.0
    indexcount = 0
    for key, pvalue in probdict.iteritems():
        indexcount+=1
        ctotal+=pvalue
    if (ctotal<=0.0):
        return ""

    # now map index range into it
    indextounit = (float(index)-float(minindex)) / (float((maxindex-minindex)+1))
    rvalnorm = indextounit * ctotal

    # now find it via roulette wheel
    rtotal = 0.0
    for key, pvalue in probdict.iteritems():
        indexcount-=1
        rtotal+=pvalue
        if (rtotal>=rvalnorm or indexcount==0):
            return key
    # we should never get to here
    return ""


# Choose an item from a list
def JrP_ChooseOneFromListRandomly(rlist):
    listlen = len(rlist)
    index = random.randrange(0,listlen)
    return rlist[index]

# Choose an item from a list
def JrP_ChooseOneFromRangeStringRandomly(rangestring):
    if (rangestring==''):
        return ''
    stringsplits = rangestring.split('-')
    if (len(stringsplits)==1):
        return int(rangestring)
    min = int(stringsplits[0])
    max = int(stringsplits[1])
    index = random.randrange(min,max+1)
    return index

# Choose N items from a listwithout replacement
def JrP_ChooseNFromListRandomlyNoReplacement(rlist,numtochoose):
    results = random.sample(rlist, numtochoose)
    return results


def JrP_Intrangeify(valuein,acceptablevalues):
    for val in acceptablevalues:
        lastval=val
        if (val>valuein):
            break
    return int(lastval)


# normalize to 0-1 values
def JrP_NormalizeToFloats(probdict):
   ctotal = 0.0
   for key, pvalue in probdict.iteritems():
        ctotal+=pvalue
   if (ctotal==0):
        return
   for key, pvalue in probdict.iteritems():
        probdict[key]=float(probdict[key])/ctotal

# normalize to 0-100 values
def JrP_NormalizeToInts(probdict):
   ctotal = 0.0
   for key, pvalue in probdict.iteritems():
        ctotal+=pvalue
   if (ctotal==0):
        return
   for key, pvalue in probdict.iteritems():
        probdict[key]=int((100.0*float(probdict[key]))/ctotal)

#---------------------------------------------------------------------------




#---------------------------------------------------------------------------
def JrP_ReturnItemsFromListANotInListB(lista,listb):
    if (len(listb)==0):
        return lista
    # convert dict to list
    if isinstance(listb, dict):
         exlist = listb.keys()
    else:
         exlist = listb
    newlist = []
    for itema in lista:
        if not itema in exlist:
            newlist.append(itema)
    return newlist
#---------------------------------------------------------------------------














#-------------------------------------------------------------------------------
def JrP_RemoveRootFromFilename(fname,root):
    # remove the root part from fname
    rlen = len(root)
    if (rlen==0):
        return fname
    if (fname.lower().find(root.lower())!=0):
        # not found
        return fname
    str = fname[rlen+1:len(fname)]
    #print "from "+fname+" and "+root+" extracted to "+str
    return str
#-------------------------------------------------------------------------------



#-------------------------------------------------------------------------------
def JrP_GoUpDirectory(path,uplevels):
    # go up a few directories from passed path
    while (uplevels>0 and len(path)>0):
        rpos1 = path.rfind("/")
        rpos2 = path.rfind("\\")
        if (rpos1>rpos2):
            rpos=rpos1
        else:
            rpos=rpos2
        if (rpos==-1):
            break
        if (rpos<len(path)-1):
            uplevels=uplevels-1
        path=path[0:rpos]
    return path
#-------------------------------------------------------------------------------


#---------------------------------------------------------------------------
def JrP_CurrentImageFilenameToCardLabelAndCategory(sourceimagepath,imgfname):
    # given an image filename we want to generate a category name and card name/label

    fpath,fbasename,fext = TJrPFileManager.SplitFilename(imgfname);

    if (fpath!=""):
        fcategory=fpath
    else:
        fcategory="base"

    flabel = fbasename

    # replace _ with spaces in label
    flabel = flabel.replace("_"," ")

    # extract initial number if present
    fvalue = ""
    m = re.search(r"^(\d[\w\-]*)\s+(.*)$",flabel)
    if (m):
        fvalue = m.group(1)
        flabel = m.group(2)

    # titlecase it
    flabel = titlecase(flabel)

    return flabel,fvalue,fcategory
#---------------------------------------------------------------------------













































#-------------------------------------------------------------------------------
def TJrP_Test_DirWalk():
    rootpath = os.getcwd()
    fmanp = TJrPFileManager()

    print "Running directory walk test #1"
    fmanp.CloseAndClearFiles()
    fogenerator = fmanp.ScanDirForFiles_GetFileList(rootpath,0,"*.*")
    for fname in fogenerator:
        print fname
    print "DONE running test."


    print "Running directory walk test #2"
    fmanp.ScanDirForFiles_CreateFileEntries(rootpath,0,"*.*",1)
    fentrylist = fmanp.pFileList
    #get_pFileList()
    for fentry in fentrylist:
        print fentry.get_fname()
    print "DONE running test."
#-------------------------------------------------------------------------------



#-------------------------------------------------------------------------------
def TJrP_Test_ObjWriteTest():
    rootpath = os.getcwd()

    print "Running pobject creation test - stage 1"

    pobjcp = TJrPObjCollection()

    pobj1 = TJrPObj()
    pobj1.add_propertyval("__file","ofile1.txt")
    pobj1.add_propertyval("val1","1a")
    pobj1.add_propertyval("val2","hello world A")
    pobjcp.AddObject(pobj1)
    #
    pobj2 = TJrPObj()
    pobj2.add_propertyval("__file","ofile2.txt")
    pobj2.add_propertyval("val1","1b")
    pobj2.add_propertyval("val2","hello world B")
    pobjcp.AddObject(pobj2)
    #
    pobj3 = TJrPObj()
    pobj3.add_propertyval("__file","ofile1.txt")
    pobj3.add_propertyval("val1","1a")
    pobj3.add_propertyval("val2","hello world A")
    pobjcp.AddObject(pobj3)
    pobj4 = TJrPObj()
    pobj4.add_propertyval("__file","ofile2.txt")
    pobj4.add_propertyval("val1","1b")
    pobj4.add_propertyval("val2","hello world B")
    pobjcp.AddObject(pobj4)

    print " writing files for pobject test creations - stage 2"
    pobjcp.WriteObjectOutputFiles(rootpath)

    print "DONE running test."
#-------------------------------------------------------------------------------









