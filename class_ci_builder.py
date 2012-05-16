#!/usr/bin/python 

import urllib2
import shutil
import re
import os
import string
from httplib import HTTP
from urlparse import urlparse



class ciBuilder(object):
    
    
    credits = 'Jason R Alexander <sunnysidesounds@gmail.com>'
    year = '2011'
    
    thisScriptName = 'class_ci_builder.py'
    
    #userGuidePath = 'user_guide'
    
    #javascriptFolder = 'js/'
    #javascriptDefault = 'jscript.js'
    
    #cssFolder = 'css'
   # cssDefault = 'styles.css'
    
    #imageFolder = 'img';
    
    #ciUrl = 'http://codeigniter.com/download.php'
    
    #jqueryUrl = 'http://code.jquery.com/jquery-latest.js'
   # jqueryFileName = 'jquery.js'
    
    #validationUrl = 'http://livevalidation.com/javascripts/src/1.3/livevalidation_standalone.compressed.js'
    #validationFileName = 'validation.js'
    
    viewsPath = 'application/views/'
    viewsFolder = 'template/'
    viewsUrl = 'views_template/'
    viewsHeader = 'header.txt'
    viewsFooter = 'footer.txt'
    viewsTemplate = 'template.txt'
    
    #apiUrl = 'http://api.snippetboxx.com/ci/'
    apiUrl = 'http://localhost:8888/Python_Projects/ci_build/ci/'
    #apiUrl = 'ci'
    
    
    urlList = {'ci':'http://codeigniter.com/download.php', 
        'validate':'http://livevalidation.com/javascripts/src/1.3/livevalidation_standalone.compressed.js', 
        'jquery':'http://code.jquery.com/jquery-latest.js'}
        
    fileList = {'jsF':'jscript.js', 
        'cssF':'styles.css', 
        'jqueryF':'jquery.js',
        'validationF':'validation.js'}
        
    folderList = {'userFo':'user_guide', 
        'jsFo':'js', 
        'cssFo':'css',
        'image': 'img'}    
    

    def __init__(self):    
        print ''
        print '-------------------------------------------'
        print 'CI Build Script'
        print '-------------------------------------------'    
        print ''
        print 'Current packages setup to install: '
        for url in self.urlList:
            print '[' + url + '] : ' + self.urlList[url]        
        print ''
        print 'Current file setup to install: '
        for file in self.fileList:
            # print value
            print '[' + file + '] : ' + self.fileList[file]    
        print ''
        print 'Current folder setup to install: '
        for folder in self.folderList:
            # print value
            print '[' + folder + '] : ' + self.folderList[folder]  
        print ''
        enterKeys = raw_input('Enter the key(s) you would like to install ') 
        
        valuesToInstall = enterKeys.split(', ')

        for installValues in valuesToInstall:           
           #install codeigniter
            if(self.urlList.has_key(installValues) == True):            
                print self.urlList
                #TODO: Make this dymanic 'ciUrl'
                if(installValues == 'ci'):
                    libraryUrl = self.urlList[installValues]
                    installCI = self.buildCi(libraryUrl)                        
            #install folders
            elif(self.folderList.has_key(installValues) == True):                    
                    jsExists = os.path.exists(self.folderList[installValues])
                    if(jsExists == False):                    
                        folder = self.folderList[installValues]
                        mk = self.makeFolder(folder)
                        self.restartScript()
                    else:
                        print " -The folder [ " + self.folderList[installValues] + " ] has already been created"   
                        self.restartScript()
            #install remote files
            elif(self.fileList.has_key(installValues) == True):
                    #self.getRemoteFile(jqueryUrl, javascriptFolder, jqueryFileName)
                    print 'value in file list'                                  


            else:
                print '[' + enterKeys + '] was not found, Please try again.'
                self.restartScript()
                #TODO: make so user can try again without restarting the script
                
        
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
      
    def fileHeader(self, folder, file):
        header = """
        /***************************************************************
        *  Copyright notice
        *
        *  (c) """+ year +""" """+ credits +"""
        *  All rights reserved
        *
        * """+ folder + """/"""+ file +"""
        ***************************************************************/
        """
        return header
            
    def getRemoteFile(self, remoteUrl, localPath, file):
        print " --Creating " + file
        getRemoteUrl = urllib2.urlopen(remoteUrl)
        output = open(localPath + file,'wb')
        output.write(getRemoteUrl.read())
        output.close() 
    
    def makeFolder(self, folder):
        print " --Making [ " + folder + " ] folder"
        os.mkdir(folder) 

    def restartScript(self):
        returnToTop =  os.system("python " + self.thisScriptName)
        return returnToTop

obj = ciBuilder()
    