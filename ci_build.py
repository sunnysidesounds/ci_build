#!/usr/bin/python 

import urllib2
import shutil
import re
import os

print ''
print '-------------------------------------------'
print 'CI Build Script'
print '-------------------------------------------'


credits = 'Jason R Alexander <sunnysidesounds@gmail.com>'
year = '2011'

thisScriptName = 'ci_build.py'

userGuidePath = 'user_guide'

javascriptFolder = 'js/'
javascriptDefault = 'jscript.js'

cssFolder = 'css'
cssDefault = 'styles.css'

imageFolder = 'img';

ciUrl = 'http://codeigniter.com/download.php'

jqueryUrl = 'http://code.jquery.com/jquery-latest.js'
jqueryFileName = 'jquery.js'

validationUrl = 'http://livevalidation.com/javascripts/src/1.3/livevalidation_standalone.compressed.js'
validationFileName = 'validation.js'

viewsPath = 'application/views/'
viewsFolder = 'template/'
viewsUrl = 'views_template/'
viewsHeader = 'header.txt'
viewsFooter = 'footer.txt'
viewsTemplate = 'template.txt'

#apiUrl = 'http://api.snippetboxx.com/ci/'
apiUrl = 'http://localhost:8888/Python_Projects/ci_build/ci/'

#FUNCTIONS

def fileHeader(folder, file):
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
        
def getRemoteFile(remoteUrl, localPath, file):
    print " --Creating " + file
    getRemoteUrl = urllib2.urlopen(remoteUrl)
    output = open(localPath + file,'wb')
    output.write(getRemoteUrl.read())
    output.close() 

def makeFolder(folder):
    print " --Making [ " + folder + " ] folder"
    os.mkdir(folder)    

def getFilesMatchingPattern(directory, nonWildCardPattern):
  fileList=os.listdir(directory)
  return [f for f in fileList if f.find(nonWildCardPattern) > -1]


#LOGIC   


#User prompt
print "[1] Install CI"
print "[2] Install Custom Folders (CSS and JS Structure)"
print "[3] Install CI Custom Configuration"
ciSetup = raw_input('What would you like to install? ')
print 'Processing...'

#Install CI
if(ciSetup == '1'):    
    #get current directory
    currentDirectory = os.getcwd()
    print "Installing CI in current directory: " +currentDirectory    
    #TODO: Check to see if the files already exists, if so, don't install or move folders    
    #wget ci
    os.system("wget " + ciUrl + "")

    print "Unzipping... "
    #unzip ci
    os.system("unzip \*.zip")

    ciZipFolder = getFilesMatchingPattern(currentDirectory, '.zip') 
    
    #Delete ci zip
    if(ciZipFolder):        
        convertToString = "".join(ciZipFolder)
        zipToDelete = currentDirectory + "/" + convertToString
        os.remove(zipToDelete) 

    #Find the ci folder
    ciFolder = getFilesMatchingPattern(currentDirectory, 'CodeIgniter')
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
    
    returnToTop =  os.system("python " +thisScriptName)

#Install Custom Folders
elif(ciSetup == '2'):    
    print '\n'
    #CREATE CUSTOM JAVASCRIPT
    #Setup path
    javascriptFile = javascriptFolder + "/" + javascriptDefault
    #Get path
    print " Checking for [ " + javascriptFolder + " ] folder"
    javascriptExists = os.path.exists(javascriptFile)
    
    if(javascriptExists != True):
        #make js
        makeFolder(javascriptFolder)
        
        print " --Creating default [ " + javascriptDefault + " ] file"
        #Create js file
        FILE = open(javascriptFile,"w")
        #Write header to js file
        FILE.writelines(fileHeader(javascriptFolder, javascriptDefault))
    
        #User prompt
        installJquery = raw_input(' Do you want to install jQuery (Y/N) ')
        
        #JQUERY INSTALL
        if(installJquery == 'Y' or installJquery == 'y'):
            print " --Getting latest version of jQuery from  [ " + jqueryUrl + " ] and building [ " + jqueryFileName + " ] file"
            getRemoteFile(jqueryUrl, javascriptFolder, jqueryFileName)
        else:
            print " --jQuery was not installed"
            
        #User prompt
        installValidation = raw_input(' Do you want to install LiveValidation (Y/N) ')
        
        #LIVEVALIDATION INSTALL
        if(installValidation == 'Y' or installValidation == 'y'):
            print " --Getting liveValidation from  [ " + validationUrl + " ]"
            getRemoteFile(validationUrl, javascriptFolder, validationFileName)
        else:
            print "--Live Validation was not installed"    
            
        #Add More JS Libraries here
            
    else:
        print " -The folder [ " + javascriptFolder + " ] has already been created"
    
    print '\n'
    #CREATE CUSTOM CSS
    #Setup path
    cssFile = cssFolder + "/" + cssDefault
    print " Checking for [ " + cssFolder + " ] folder"
    #Get path
    cssExists = os.path.exists(cssFile)
    
    if(cssExists != True):    
        makeFolder(cssFolder)
        
        print " --Creating default [ " + cssDefault + " ] file"
        #Create css file
        FILE = open(cssFile,"w")
        #Write header to css file
        FILE.writelines(fileHeader(cssFolder, cssDefault))
    else:
        print " -The folder [ " + cssFolder + " ] has already been created"
    
    print '\n'
    #DELETE USERGUIDE
    print " Checking for [ " + userGuidePath + " ] folder"
    userGuideExists = os.path.exists(userGuidePath)
    if(userGuideExists == True):
        print " --Removng the [ " + userGuidePath + " ] folder"
        shutil.rmtree(userGuidePath)
    else:
        print " -No need to remove the [ " + userGuidePath + " ] folder"

    print '\n'
    #CREATE IMAGE DIRECTORY
    print " Checking for [ " + imageFolder + " ] folder"
    imageFolderExists = os.path.exists(imageFolder)
    if(imageFolderExists != True):
        makeFolder(imageFolder)
    else:
        print " -The folder [ " + imageFolder + " ] has already been created"
    
    #installTemplateViews = raw_input(' Do you want to install your template view files (Y/N) ')
    
    print '\n'

#CI Custom Configuration    
elif(ciSetup == '3'):
    #CREATE VIEWS TEMPLATE
    viewFullPath = viewsPath + viewsFolder
    print " Checking for [ " + viewsFolder + " ] folder in [ " + viewsPath + " ]"
    viewsExists = os.path.exists(viewFullPath)
    if(viewsExists != True):    
        makeFolder(viewFullPath)
                
        #TO DO MAKE THIS MORE DYNAMIC
        #Reads all the files from the folder "template"
        print " --Getting template files from  [ " + apiUrl + " ]"
        #header    
        headerUrl = apiUrl + viewsUrl + viewsHeader
        headerPath = viewsPath + viewsFolder
        getHeader = getRemoteFile(headerUrl, headerPath, 'header.php')        
        #footer
        footerUrl = apiUrl + viewsUrl + viewsFooter
        footerPath = viewsPath + viewsFolder
        getFooter = getRemoteFile(footerUrl, footerPath, 'footer.php')            
        #template
        templateUrl = apiUrl + viewsUrl + viewsTemplate
        templatePath = viewsPath + viewsFolder
        getTemplate = getRemoteFile(templateUrl, templatePath, 'template.php')  
    else:
        print " -The folder [ " + viewsFolder + " ] has already been created"
    print '\n'    
    
    
    
else:
    print "Please choose a value."
    
    
#DEV
#print "-add user_guide back in for dev testin"
#os.mkdir(userGuidePath)

