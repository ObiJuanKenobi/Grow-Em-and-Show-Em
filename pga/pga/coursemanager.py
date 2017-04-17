import os
import glob
import shutil
import zipfile
from subprocess import Popen, PIPE
from .dataAccess import DataAccess

# Directory in which to store course / lesson data.
# Should probably somewhere in /etc, /var, or /opt.
COURSE_DIR = '.'

"""
coursemanager.py
@author Andrew Dailey

The code in this file is for managing the conversion of course packages (zip files)
  into their proper directory structure and database entries.
"""

"""
From a given zip file, move its lesson data into the proper server-side directories.
Then, add the new course and lesson data into the database.

@param in_mem_file Django InMemoryUploadedFile of course zip
  https://docs.djangoproject.com/en/1.11/ref/files/uploads/
@return Tuple <Boolean, String> of success status and message
"""
def processCourseZip(in_mem_file):
    ZIP_TMP_DIR  = '/tmp/pending_course'
    ZIP_TMP_FILE = ZIP_TMP_DIR + '.zip'

    # Write file down to server in chunks (for memory reasons)
    with open(ZIP_TMP_FILE, 'wb+') as dest:
        for chunk in in_mem_file.chunks():
            dest.write(chunk)

    # Extract the zip to a temporary directory
    with zipfile.ZipFile(ZIP_TMP_FILE, 'r') as zip_ref:
        zip_ref.extractall(ZIP_TMP_DIR)

    # Ensure root dir of zip has only one course (one directory)
    if (len(os.listdir(ZIP_TMP_DIR)) != 1):
        print('[coursemanager] Number of courses is not 1')

    # Init database access
    db = DataAccess()

    # TODO Get this data from a metadata file
    # Pull out course name and create its server directory
    course_name = os.listdir(ZIP_TMP_DIR)[0]
    course_path = os.path.join(COURSE_DIR, course_name)
    course_path_tmp = os.path.join(ZIP_TMP_DIR, course_name)
    course_order = 0
    if (os.path.exists(course_path)):
        print('[coursemanager] Modifying existing course')
    else:
        os.mkdir(course_path)

    # Add course info to database
    db.addCourse(course_name, course_order, course_path)

    # Create server directories for each lesson
    course_lessons = os.listdir(os.path.join(ZIP_TMP_DIR, course_name))
    for lesson_name in course_lessons:
        lesson_path = os.path.join(course_path, lesson_name)
        if (os.path.exists(lesson_path)):
            print('[coursemanager] Modifying existing lesson')
        else:
            os.mkdir(os.path.join(course_path, lesson_name))

        # Copy all lesson content to server lesson directory
        lesson_path_tmp = os.path.join(course_path_tmp, lesson_name)
        for content in glob.glob(os.path.join(lesson_path_tmp, '*')):
            shutil.copy(content, lesson_path)

        # Add lesson info to database
        lesson_path_html = os.path.join(lesson_path, lesson_name + '.html')
        db.addLesson(course_name, lesson_name, lesson_path_html)

    return True, 'Course uploaded successfully: ' + course_name
