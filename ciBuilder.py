#!/usr/bin/python 

import urllib2
import shutil
import re
import os
import string
from httplib import HTTP
from urlparse import urlparse

class ciBuilder(object):    
    #misc
    credits = 'Jason R Alexander <sunnysidesounds@gmail.com>'
    year = '2011'    
    thisScriptName = 'ciBuilder.py'
    #file urls
    ciUrl = 'http://codeigniter.com/download.php'
    jqueryUrl = 'http://code.jquery.com/jquery-latest.js'    
    validationUrl = 'http://livevalidation.com/javascripts/src/1.3/livevalidation_standalone.compressed.js'
    #folders
    userGuidePath = 'user_guide'
    javascriptFolder = 'js'
    cssFolder = 'css'
    imageFolder = 'img'
    #files
    jqueryFile = 'jquery.js'
    validationFile = 'validation.js'
    defaultJs = 'jscript.js'
    defaultCss = 'styles.css'
    
        
    def __init__(self):    
        print ''
        print '-------------------------------------------'
        print 'CI BUILD SCRIPT'  
        print '(c) 2011 Jason R Alexander <sunnysidesounds@gmail.com>'
        print 'Version 1.0.0'
        print '-------------------------------------------' 
        print ''
                
        continueScript = raw_input('Continue with the setup? (Y/N): ') 
        
        if(continueScript == 'Y' or continueScript == 'y'):
            #Install ci
            self.buildCi(self.ciUrl)
            
            #Delete user_guide
            print "Removng the [ " + self.userGuidePath + " ] folder"
            shutil.rmtree(self.userGuidePath)
            
            #Create javascript folder
            setJsFolder = self.makeFolder(self.javascriptFolder)
            
            #Create css folder
            setCssFolder = self.makeFolder(self.cssFolder)
           
           #Create image folder
            setImgFolder = self.makeFolder(self.imageFolder)
            
            #Create default js file
            jsDefault = self.javascriptFolder + '/' + self.defaultJs
            self.makeFile(jsDefault)

            #Create default css file
            cssDefault = self.cssFolder + '/' + self.defaultCss
            self.makeFile(cssDefault)
                       
           #Get and create jQuery
            self.getRemoteFile(self.jqueryUrl, self.javascriptFolder + '/', self.jqueryFile)
           
           #Get and create liveValidation
            self.getRemoteFile(self.validationUrl, self.javascriptFolder + '/', self.validationFile)
        
        else:
            print 'Invalid Selection, Try Again'
            self.restartScript()


    def buildCi(self, ciUrl):
        #get current directory
        currentDirectory = os.getcwd()
        print "Installing CI in current directory: " +currentDirectory    
        #TODO: Check to see if the files already exists, if so, don't install or move folders    
        #wget ci
        os.system("wget " + ciUrl + "")
    
        print "Unzipping... "
        #unzip ci
        os.system("unzip \*.zip")
    
        ciZipFolder = self.getFilesMatchingPattern(currentDirectory, '.zip') 
        
        #Delete ci zip
        if(ciZipFolder):        
            convertToString = "".join(ciZipFolder)
            zipToDelete = currentDirectory + "/" + convertToString
            os.remove(zipToDelete) 
    
        #Find the ci folder
        ciFolder = self.getFilesMatchingPattern(currentDirectory, 'CodeIgniter')
        ciConvertToString = "".join(ciFolder)
        ciDirectory = currentDirectory + "/" + ciConvertToString
        #List ci folder content    
        srcFiles = os.listdir(ciDirectory)
        for fileName in srcFiles:        
            print "Moving [" + fileName + "] into place..."
            sourceCi = ciDirectory + "/" +fileName
            moveFilesInToPlace = shutil.move(sourceCi, currentDirectory)
            
        if(ciFolder): 
            convertToString = "".join(ciFolder)
            fileToDelete = currentDirectory + "/" + convertToString
            shutil.rmtree(fileToDelete)
    
        print "ci is installed in" + currentDirectory
        

    def getFilesMatchingPattern(self, directory, nonWildCardPattern):
      fileList=os.listdir(directory)
      return [f for f in fileList if f.find(nonWildCardPattern) > -1]
      
    def fileHeader(self, path):
        header = """
        /***************************************************************
        *  Copyright notice
        *
        *  (c) """+ self.year +""" """+ self.credits +"""
        *  All rights reserved
        *
        * """+ path + """
        ***************************************************************/
        """
        return header
            
    def getRemoteFile(self, remoteUrl, localPath, file):
        print "Creating " + file
        getRemoteUrl = urllib2.urlopen(remoteUrl)
        output = open(localPath + file,'wb')
        output.write(getRemoteUrl.read())
        output.close() 
    
    def makeFolder(self, folder):
        print "Creating [ " + folder + " ] folder"
        os.mkdir(folder) 
    
    def makeFile(self, path):
        print "Creating [ " + path + " ] file"
        #Create file
        FILE = open(path,"w")
        #Write header
        #TODO: Redo the fileHeader function
        FILE.writelines(self.fileHeader(path))

    def restartScript(self):
        returnToTop =  os.system("python " + self.thisScriptName)
        return returnToTop


#ciBuilder Object creation
obj = ciBuilder()
    