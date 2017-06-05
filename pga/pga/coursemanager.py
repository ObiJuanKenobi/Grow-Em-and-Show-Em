import glob
import openpyxl
import os
import re
import shutil
import zipfile
from .dataAccess import DataAccess, QuizQuestion, QuizAnswer


"""
coursemanager.py
@author Andrew Dailey

The code in this file is for managing the conversion of course packages (zip files)
  into their proper directory structure and database entries.
"""

# Directory in which to store course / lesson data.
COURSE_DIR = './static/courses'

"""
Get a list of paths to the extra materials for a given course.

@param course_name Name of course to get materials from
@return List of materials associated with given course
"""
def getMaterialPaths(course_name):
    course_dir = os.path.join(COURSE_DIR, course_name)
    materials_dir = os.path.join(course_dir, 'materials')

    return [os.path.join(materials_dir, f) for f in os.listdir(materials_dir)]

"""
Given a directory, return the first file with given extension.

@param base_path Directory to search
@param extension Desired extension of file
@return First file found with this extension
"""
def getFirstPathWithExtension(base_path, extension):
    valid_files = [f for f in os.listdir(base_path) if f.endswith(extension)]
    if len(valid_files) == 0:
        return None
    return os.path.join(base_path, valid_files[0])

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
    course_path = os.path.join(COURSE_DIR, course_name)
    course_tmp_path = os.path.join(ZIP_TMP_DIR, course_dir_name)
    if (os.path.exists(course_path)):
        print('[coursemanager] Modifying existing course')
    else:
        os.makedirs(course_path)

    # Check if this course has a quiz
    has_quiz = 1 if 'quiz' in os.listdir(course_tmp_path) else 0

    # Add course info to database
    db.addCourse(course_name, course_order, course_path, has_quiz)

    # Create server directories for each lesson
    course_lessons = os.listdir(os.path.join(ZIP_TMP_DIR, course_dir_name))
    for lesson_name in course_lessons:

        # Create lesson directory if not already present
        lesson_path = os.path.join(course_path, lesson_name)
        if (os.path.exists(lesson_path)):
            print('[coursemanager] Modifying existing lesson')
        else:
            os.makedirs(os.path.join(course_path, lesson_name))

        # Copy all lesson content to server lesson directory
        lesson_tmp_path = os.path.join(course_tmp_path, lesson_name)
        for content in glob.glob(os.path.join(lesson_tmp_path, '*')):
            shutil.copy(content, lesson_path)

        # Skip lesson processing for quizzes and materials
        if lesson_name == 'quiz' or lesson_name == 'materials':
            continue

        # Add lesson info to database
        lesson_path_html = getFirstPathWithExtension(lesson_path, '.html')
        if lesson_path_html is not None:
            db.addLesson(course_name, lesson_name, lesson_path_html)

        # Read file
        with open(lesson_path_html, 'r') as html_file:
            html_text = html_file.read()

        # Replace links
        content_pattern = r'<!--\s*LINK:\s*"(.*)",\s*type:\s*"(.*)",\s*text:\s*"(.*)"\s*-->'
        content_replace = r'<a href="/static/courses/' + course_name + r'/materials/\1">\3</a>'
        section_pattern = r'<!--\s*LINK:\s*"(.*)",\s*type:\s*"subsection",\s*name:\s*"(.*)"\s*-->'
        section_replace = r'<a href="#\1">\2</a>'
        image_pattern = r'<img.*src=".*\/(.*)".*alt="(.*)".*\/>'
        image_replace = r'<img src="/static/courses/' + course_name + r'/materials/\1" alt="\2"/>'

        html_text = re.sub(content_pattern, content_replace, html_text)
        html_text = re.sub(section_pattern, section_replace, html_text)
        html_text = re.sub(image_pattern, image_replace, html_text)

        # Write file
        with open(lesson_path_html, 'w') as html_file:
           html_file.write(html_text)

    # Import quiz data
    if has_quiz == 1:
        processQuiz(course_name, course_path)

    # Cleanup temp dirs
    shutil.rmtree(ZIP_TMP_DIR)

    return True, 'Course uploaded successfully: ' + course_name


def add_new_quiz(course_name, quiz_file):
    course_dir = os.path.join(COURSE_DIR, course_name)
    quiz_path = os.path.join(course_dir, 'quiz')

    if os.path.exists(quiz_path):
        quiz = getFirstPathWithExtension(quiz_path, '.xlsx')

        # Delete an existing quiz:
        if quiz is not None:
            os.remove(quiz)

    else:
        os.makedirs(quiz_path)

    f = open(os.path.join(quiz_path, "quiz.xlsx"), 'w')
    f.write(quiz_file.read())

    processQuiz(course_name, course_dir)


"""
Process the contents of a given quiz spreadsheet by adding its
  questions and answers to the database.

@param course_dir Directory of course containing quiz to be processed
"""
def processQuiz(course_name, course_dir):
    quiz_path = getFirstPathWithExtension(os.path.join(course_dir, 'quiz'), '.xlsx')
    wb = openpyxl.load_workbook(filename = quiz_path, read_only = True, data_only = True)

    questions = []

    # Will probably only ever be 1 sheet
    for sheet in wb:
        
        # Accumulate questions and their answers
        #
        # Spreadsheet cols:
        # [0] = Question itself
        # [1] = Correct answer
        # [2] = Other answer 1
        # [3] = Other answer 2
        # [4] = Other answer 3
        for row in sheet.iter_rows(row_offset = 1):
            if type(row[0].value) != unicode:
                continue

            # Create a QuizAnswer object for each answer
            correct = QuizAnswer()
            correct._Text = row[1].value
            correct._IsCorrect = True

            other1 = QuizAnswer()
            other1._Text = row[2].value

            other2 = QuizAnswer()
            other2._Text = row[3].value

            other3 = QuizAnswer()
            other3._Text = row[4].value

            # Create a QuizQuestion object and add its answers
            question = QuizQuestion()
            question._Text = row[0].value
            question._Answers.append(correct)
            question._Answers.append(other1)
            question._Answers.append(other2)
            question._Answers.append(other3)

            # Add QuizQuestion to list of questions
            questions.append(question)

        db = DataAccess()
        db.deleteQuiz(course_name)
        db.add_quiz(course_name, questions)

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
