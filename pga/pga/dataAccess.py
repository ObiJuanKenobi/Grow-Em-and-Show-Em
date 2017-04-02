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
        exists = cursor.execute("SELECT Username FROM Users WHERE Username = %s", [username])
        if not exists:
            self._cursor.execute("INSERT into Users (Username, Password, First_Name, Last_Name) values (%s, PASSWORD(%s), %s, %s)", (username, password, firstname, lastname))
            return True
        else:
            return False

    def addCourse(self, coursename, courseorder, courseHTMLpath):
        exists = self._cursor.execute("SELECT Course_Name FROM Courses WHERE Course_Name = %s", [coursename])
        if exists:
            self._cursor.execute("UPDATE Courses SET Course_Order = %s, Course_HTML_Path = %s WHERE Course_Name = %s", (courseorder, courseHTMLpath, coursename))
        else:
            self._cursor.execute("INSERT into Courses (Course_Name, Course_Order, Course_HTML_Path) values (%s, %s, %s)", (coursename, courseorder, courseHTMLpath))

    def addLesson(self, coursename, lessonname, lessonfilepath):
        exists = self._cursor.execute("SELECT Lesson_Name FROM Lessons WHERE Lesson_Name = %s", [lessonname])
        if exists:
            self._cursor.execute("UPDATE Lessons SET Lesson_File_Path = %s WHERE Lesson_Name = %s", (lessonfilepath, lessonname))
        else:
            self._cursor.execute("INSERT into Lessons (Course_Name, Lesson_Name, Lesson_File_Path) values (%s, %s, %s)", (coursename, lessonname, lessonfilepath))

    def getLesson(self, coursename, lessonname):
        self._cursor.execute("SELECT Lesson_File_Path FROM Lessons WHERE Course_Name = %s AND Lesson_Name = %s", (coursename, lessonname))
        lesson = ""
        for(Lesson_File_Path) in self._cursor:
            lesson = Lesson_File_Path
        return lesson[0]

    def getCourseLessons(self, coursename):
        self._cursor.execute("SELECT Lesson_Name, Lesson_File_Path FROM Lessons WHERE Course_Name = %s", [coursename])
        results = self._cursor.fetchall()
        lessons = []
        for row in results:
            lessons.append({"name": row[0], "path": row[1]})
        return lessons


    def addQuiz(self, coursename, questions):
        for question in questions:
            self._cursor.execute("INSERT into Quiz_Questions (Question_Text, Course_Name) values (%s, %s)", (question._Text, coursename))
            questionID = self._cursor.lastrowid
            for answer in question._Answers:
                self._cursor.execute("INSERT into Quiz_Answers (QuestionID, Answer_Text, IsCorrect) values (%s, %s, %s)", (questionID, answer._Text, answer._IsCorrect))

    def getQuizQuestions(self, coursename):
        self._cursor.execute("SELECT q.questionID as id, q.Question_Text as question, a.Answer_Text as answer, a.Is_Correct as correct FROM Quiz_Questions q, Quiz_Answers a WHERE q.Course_Name = %s AND q.questionID = a.questionID;", [coursename])

        results = self._cursor.fetchall()
        questions = {};
        for row in results:
            id = row[0];
            question = row[1];
            answer = row[2];
            correct = row[3];

            if id in questions:
                questions[id]["answers"].append({"answer": answer, "correct": bool(int.from_bytes(correct, byteorder='big'))});
            else:
                questions[id] = {"question": question, "id": id};
                questions[id]["answers"] = [{"answer": answer, "correct": bool(int.from_bytes(correct, byteorder='big'))}];

        questionsArr = [];
        for id in questions:
            questionsArr.append(questions[id])
        return questionsArr;

    def addQuizAttempt(self, coursename, username, passed, questions):
        questionColumns = "Question1_ID, Answer1_ID, Question2_ID, Answer2_ID, Question3_ID, Answer3_ID, Question4_ID, Answer4_ID, Question5_ID, Answer5_ID"
        questionColumns = questionColumns + ", Question6_ID, Answer6_ID, Question7_ID, Answer7_ID, Question8_ID, Answer8_ID, Question_ID, Answer9_ID, Question10_ID, Answer10_ID"
        self._cursor.execute("INSERT into Quiz_Attempts (Course_Name, Username, Passed, Question1_ID, Answer1_ID, Question2_ID, Answer2_ID, Question3_ID, Answer3_ID, Question4_ID, Answer4_ID, Question5_ID, Answer5_ID, Question6_ID, Answer6_ID, Question7_ID, Answer7_ID, Question8_ID, Answer8_ID, Question9_ID, Answer9_ID, Question10_ID, Answer10_ID) values (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)", (coursename, username, passed, questions[0]["questionID"], questions[0]["answerID"], questions[1]["questionID"], questions[1]["answerID"], questions[2]["questionID"], questions[2]["answerID"], questions[3]["questionID"], questions[3]["answerID"], questions[4]["questionID"], questions[4]["answerID"], questions[5]["questionID"], questions[5]["answerID"], questions[6]["questionID"], questions[6]["answerID"], questions[7]["questionID"], questions[7]["answerID"], questions[8]["questionID"], questions[8]["answerID"], questions[9]["questionID"], questions[9]["answerID"]))
        # exists = self._cursor.execute("SELECT Attempts FROM Quiz_Attempts WHERE Course_Name = %s AND Username = %s", (coursename, username))
        # if exists:
        #     self._cursor.execute("UPDATE Quiz_Attempts SET Attempts = Attempts + 1, Passed = %s WHERE Course_Name = %s AND Username = %s", (passed, coursename, username))
        # else:
        #     self._cursor.execute("INSERT into Quiz_Attempts (Course_Name, Username, Attempts, Passed) values (%s, %s, %s, %s)", (coursename, username, 1, passed))

    #Currently, this will get every chapter completed by every user.
    def getAllUserProgress(self):
        self._cursor.execute("SELECT QA.ID as attemptID, QA.Username as user, QA.Course_Name as course, C.Course_Order as chapter FROM Quiz_Attempts QA, Courses C WHERE C.Course_Name = QA.Course_Name AND QA.Passed = 1 ORDER BY QA.Username, C.Course_Order;")
        results = self._cursor.fetchall();

        userProgress = {}
        for row in results:
            attempt = row[0];
            username = row[1];
            course = row[2];
            chapter = row[3];

            if username in userProgress:
                userProgress[username].append({"course": course, "chapter": chapter, "attempt": attempt});
            else:
                userProgress[username] = [{"course": course, "chapter": chapter, "attempt": attempt}];

    def getQuizAttempt(self, attemptID):
        self._cursor.execute("SELECT QQ.Question_Text, QAn.Answer_Text from Quiz_Questions QQ, Quiz_Attempts QA, Quiz_Answers QAn where QA.ID = %s and (QQ.QuestionID = QA.Question1_ID and QAn.AnswerID = QA.Answer1_ID or QQ.QuestionID = QA.Question2_ID and QAn.AnswerID = QA.Answer2_ID	or QQ.QuestionID = QA.Question3_ID and QAn.AnswerID = QA.Answer3_ID	or QQ.QuestionID = QA.Question4_ID and QAn.AnswerID = QA.Answer4_ID	or QQ.QuestionID = QA.Question5_ID and QAn.AnswerID = QA.Answer5_ID	or QQ.QuestionID = QA.Question6_ID and QAn.AnswerID = QA.Answer6_ID	or QQ.QuestionID = QA.Question7_ID and QAn.AnswerID = QA.Answer7_ID	or QQ.QuestionID = QA.Question8_ID and QAn.AnswerID = QA.Answer8_ID	or QQ.QuestionID = QA.Question9_ID and QAn.AnswerID = QA.Answer9_ID	or QQ.QuestionID = QA.Question10_ID and QAn.AnswerID = QA.Answer10_ID);", [attemptID])
        results = self._cursor.fetchall()
        return results
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
