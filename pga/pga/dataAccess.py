import MySQLdb

class DataAccess:
    _connection = None
    _cursor = None

    #Establish DB connection on instantiation of a new DataAccess object
    def __init__(self):
        self._connection = MySQLdb.Connection(host = "sddb.ece.iastate.edu", port = 3306, user = "may1713", passwd="gawrA75Nac!&", db="may1713_PrisonGardenApp")
        self._cursor = self._connection.cursor()

    #Close the connection when this object is deleted or falls out of scope
    def __del__(self):
        self._cursor.execute("COMMIT")
        self._connection.close()

    def addUser(self, username, password, firstname, lastname):
        self._cursor.execute("INSERT into Users (Username, Password, First_Name, Last_Name) values (%s, PASSWORD(%s), %s, %s)", (username, password, firstname, lastname))

    def addCourse(self, coursename, courseorder):
        self._cursor.execute("INSERT into Courses (Course_Name, Course_Order) values (%s, %s)", (coursename, courseorder))

    def addLesson(self, coursename, lessonname, lessonfilepath):
        self._cursor.execute("INSERT into Lessons (Course_Name, Lesson_Name, Lesson_File_Path) values (%s, %s, %s)", (coursename, lessonname, lessonfilepath))

    def getLesson(self, coursename, lessonname):
        self._cursor.execute("SELECT Lesson_File_Path FROM Lessons WHERE Course_Name = %s AND Lesson_Name = %s", (coursename, lessonname))
        lesson = ""
        for(Lesson_File_Path) in self._cursor:
            lesson = Lesson_File_Path
        return lesson[0]

    def addQuiz(self, coursename, questions):
        for question in questions:
            self._cursor.execute("INSERT into Quiz_Questions (Question_Text, Course_Name) values (%s, %s)", (question._Text, coursename))
            questionID = self._cursor.lastrowid
            for answer in question._Answers:
                self._cursor.execute("INSERT into Quiz_Answers (QuestionID, Answer_Text, IsCorrect) values (%s, %s, %s)", (questionID, answer._Text, answer._IsCorrect))

    def addQuizAttempt(self, coursename, username, passed):
        #First, check to see if the user has taken the course before
        data = self._cursor.execute("SELECT Attempts FROM Quiz_Attempts WHERE Course_Name = %s AND Username = %s", (coursename, username))
        #If data is empty, this condition evaluates to True
        if not data:
            self._cursor.execute("INSERT into Quiz_Attempts (Course_Name, Username, Attempts, Passed) values (%s, %s, %s, %s)", (coursename, username, 1, passed))
        else:
            self._cursor.execute("UPDATE Quiz_Attempts SET Attempts = Attempts + 1, Passed = %s WHERE Course_Name = %s AND Username = %s", (passed, coursename, username))

#Class for passing quiz questions to the DB in a convenient object
class QuizQuestion:
    _Text = None
    _Answers = None

    def __init__(self):
        _Text = ""
        _Answers = ["", "", "", ""]

#Class for passing quiz answers to the DB in a convenient object
class QuizAnswer:
    _Text = None
    _IsCorrect = None

    def __init__(self):
        _Text = ""
        _IsCorrect = False
