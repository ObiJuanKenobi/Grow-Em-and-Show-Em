import os
from subprocess import Popen, PIPE

'''
modulemanager.py
@author Andrew Dailey
'''

'''
Helper method for opening the lowriter subprocess for converting docx to HTML.
'''
def __docxToHTML(inputFile, outputPath):
    process = Popen(['lowriter', '--convert-to', 'html', '--outdir', outputPath, inputFile], stdout=PIPE, stderr=PIPE)
    stdout, stderr = process.communicate()

'''
Convert all docx files found in moduleDir to html files in dataDir.
'''
def convertModulesToHTML(moduleDir, dataDir):
    # Ensure module path is absolute
    if moduleDir[0] != '/':
        print('Module path should be absolute: ' + moduleDir)
        return

    print('Converting modules from: ' + moduleDir)

    # Iterate over modules, converting each to HTML
    for root, dirs, files in os.walk(moduleDir):
        for file in files:
            path = os.path.join(root, file)

            # Skip non-docx files
            if 'docx' not in file:
                print('Skipping:\t' + file)
                continue

            # Convert docx files to HTML
            print('Converting:\t' + file)
            __docxToHTML(path, dataDir + path)

'''
After converting docx files to HTML, sync them with the Courses table.
'''
def syncModulesToDatabase(moduleRoot):
    pass

convertModulesToHTML('dataPath', '/tmp')
