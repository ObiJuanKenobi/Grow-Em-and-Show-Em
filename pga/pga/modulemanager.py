import os
from subprocess import Popen, PIPE
from dataAccess import DataAccess

'''
modulemanager.py
@author Andrew Dailey
'''

'''
Helper method for opening the lowriter subprocess for converting docx to HTML.
'''
def docxToHTML(inputFile, outputPath):
    process = Popen(['lowriter', '--convert-to', 'html', '--outdir', outputPath, inputFile], stdout=PIPE, stderr=PIPE)
    stdout, stderr = process.communicate()

'''
Convert all docx files found in contentDir to html files in htmlDir.
'''
def convertLessonsToHTML(contentDir, htmlDir):
    # Ensure content path is absolute
    if contentDir[0] != '/':
        print('Content path should be absolute: ' + contentDir)
        return

    print('Converting lessons from: ' + contentDir)
    lessons = []

    # Iterate over lessons, converting each to HTML
    for root, dirs, files in os.walk(contentDir):
        for file in files:
            path = os.path.join(root, file)

            # Skip non-docx files
            if 'docx' not in file:
                print('Skipping:\t' + file)
                continue

            # Convert docx files to HTML
            print('Converting:\t' + file)
            docxToHTML(path, htmlDir + path)

            # Keep track of all created lessons
            lessons.append(htmlDir + path  + '/' + file[:-4] + 'html')

    return lessons

'''
After converting docx files to HTML, sync them with the Courses table.
'''
def syncLessonsToDatabase(contentDir):
    lessons = convertLessonsToHTML(contentDir, '/tmp')
    if not lessons:
        return
    
    db = DataAccess()
    for lesson in lessons:
        name = lesson.split('/')[-1]
        print('Adding lesson: ' + name)

        db.addCourse(name, 0, lesson)

syncLessonsToDatabase('tmp/sd_data')
