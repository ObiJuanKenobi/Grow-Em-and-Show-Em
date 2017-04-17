import os
import glob
import shutil
import zipfile
from subprocess import Popen, PIPE
from .dataAccess import DataAccess

# Directory in which to store course / lesson data.
COURSE_DIR = './static/courses'

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

    # Pull out course name and create its server directory
    # Ex. 1_Course_Name
    course_dir_name = os.listdir(ZIP_TMP_DIR)[0]
    course_order, course_name = splitCourseDirectoryName(course_dir_name)
    course_path = os.path.join(COURSE_DIR, course_dir_name)
    course_tmp_path = os.path.join(ZIP_TMP_DIR, course_dir_name)
    if (os.path.exists(course_path)):
        print('[coursemanager] Modifying existing course')
    else:
        os.mkdir(course_path)

    # Add course info to database
    db.addCourse(course_name, course_order, course_path)

    # Create server directories for each lesson
    course_lessons = os.listdir(os.path.join(ZIP_TMP_DIR, course_dir_name))
    for lesson_name in course_lessons:
        lesson_path = os.path.join(course_path, lesson_name)
        if (os.path.exists(lesson_path)):
            print('[coursemanager] Modifying existing lesson')
        else:
            os.mkdir(os.path.join(course_path, lesson_name))

        # Copy all lesson content to server lesson directory
        lesson_tmp_path = os.path.join(course_tmp_path, lesson_name)
        for content in glob.glob(os.path.join(lesson_tmp_path, '*')):
            print(content)
            if 'quiz' in content or 'materials' in content:
                continue
            shutil.copy(content, lesson_path)

        # Add lesson info to database
        lesson_path_html = os.path.join(lesson_path, 'lesson.html')
        db.addLesson(course_name, lesson_name, lesson_path_html)

    return True, 'Course uploaded successfully: ' + course_name

"""
Split a course directory into its order and name.
Ex. 1_Course_Name becomes (1, 'Course Name')

@param course_dir_name Name of directory to split
@return Tuple<Int, String> of course order and course name
"""
def splitCourseDirectoryName(course_dir_name):
    course_order = int(course_dir_name.split('_')[0])
    course_name = ' '.join(course_dir_name.split('_')[1:])
    return course_order, course_name
