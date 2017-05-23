import MySQLdb
import smtplib
from email.mime.text import MIMEText
from decimal import Decimal

class DataAccess:
    _connection = None
    _cursor = None

    #Establish DB connection on instantiation of a new DataAccess object
    def __init__(self):
        self._connection = MySQLdb.Connection(host = "sddb.ece.iastate.edu", port = 3306, user = "may1713", passwd="gawrA75Nac!&", db="may1713_PrisonGardenApp")


    #Close the connection when this object is deleted or falls out of scope
    def __del__(self):
        # self._cursor = self._connection.cursor()
        # self._cursor.execute("COMMIT")
        self._connection.close()

    def isUser(self, username, password):
        self._cursor = self._connection.cursor()
        exists = self._cursor.execute("SELECT Username FROM Users WHERE Username = %s and PASSWORD(%s) = password", (username, password))
        if not exists:
            return True
        else:
            return False

    def addUser(self, username, password, firstname, lastname):
        self._cursor = self._connection.cursor()
        exists = self._cursor.execute("SELECT Username FROM Users WHERE Username = %s", [username])
        if not exists:
            self._cursor.execute("INSERT into Users (Username, Password, First_Name, Last_Name) values (%s, PASSWORD(%s), %s, %s)", (username, password, firstname, lastname))
            self._cursor.execute("COMMIT")
            return True
        else:
            return False

    def addCourse(self, coursename, courseorder, courseHTMLpath, has_quiz):
        self._cursor = self._connection.cursor()
        exists = self._cursor.execute("SELECT Course_Name FROM Courses WHERE Course_Name = %s", [coursename])
        if exists:
            self._cursor.execute("UPDATE Courses SET Course_Order = %s, Course_HTML_Path = %s, Has_Quiz = %s WHERE Course_Name = %s", (courseorder, courseHTMLpath, coursename, has_quiz))
        else:
            self._cursor.execute("INSERT into Courses (Course_Name, Course_Order, Course_HTML_Path, Has_Quiz) values (%s, %s, %s, %s)", (coursename, courseorder, courseHTMLpath, has_quiz))
        self._cursor.execute("COMMIT")

    def getAllUnits(self):
        self._cursor = self._connection.cursor()
        self._cursor.execute("SELECT Course_Name FROM Courses Order By Course_Order")
        results = self._cursor.fetchall()
        courses = []
        for row in results:
            courses.append(row[0])

        return courses
        
    def getCompletedCoursesForUser(self, user):
        self._cursor = self._connection.cursor()
        self._cursor.execute("Select distinct Course_Name from Quiz_Attempts WHERE Username=%s and Passed=1;", [user])
        results = self._cursor.fetchall()
        courses = []
        for row in results:
            courses.append(row[0])
            
        return courses

    def addLesson(self, coursename, lessonname, lessonfilepath):
        self._cursor = self._connection.cursor()
        exists = self._cursor.execute("SELECT Lesson_Name FROM Lessons WHERE Lesson_Name = %s", [lessonname])
        if exists:
            self._cursor.execute("UPDATE Lessons SET Lesson_File_Path = %s WHERE Lesson_Name = %s", (lessonfilepath, lessonname))
        else:
            self._cursor.execute("INSERT into Lessons (Course_Name, Lesson_Name, Lesson_File_Path) values (%s, %s, %s)", (coursename, lessonname, lessonfilepath))
        self._cursor.execute("COMMIT")

    def editLessonName(self, oldName, newName):
        self._cursor = self._connection.cursor()
        self._cursor.execute("UPDATE Lessons SET Lesson_Name = %s WHERE Lesson_Name = %s", (newName, oldName))

    def getLesson(self, coursename, lessonname):
        self._cursor = self._connection.cursor()
        self._cursor.execute("SELECT Lesson_File_Path FROM Lessons WHERE Course_Name = %s AND Lesson_Name = %s", (coursename, lessonname))
        lesson = ""
        for(Lesson_File_Path) in self._cursor:
            lesson = Lesson_File_Path
        return lesson[0]

    def deleteLesson(self, lessonname):
        #This will get rid of the lesson from the table, but don't have supplemental content set up so not sure how to handle just yet
        self._cursor = self._connection.cursor()
        self._cursor.execute("DELETE FROM Lessons WHERE Lesson_Name = %s", [lessonname])
        self._cursor.execute("COMMIT")

    def deleteUnit(self, unitName):
        self._cursor = self._connection.cursor()
        self._cursor.execute("DELETE FROM Courses WHERE Course_Name = %s", [unitName])
        self._cursor.execute("COMMIT")

    def editUnitName(self, oldName, newName):
        self._cursor = self._connection.cursor()
        self._cursor.execute("UPDATE Courses SET Course_Name = %s WHERE Course_Name = %s", (newName, oldName))
        self._cursor.execute("COMMIT")

    def getCourses(self):
        self._cursor = self._connection.cursor()
        self._cursor.execute("Select CourseID, Course_Name, Course_Color from Courses ORDER BY Course_Order;")
        courses = []
        results = self._cursor.fetchall()
        for row in results:
            courses.append({"CourseID": row[0], "Course_Name": row[1], "Course_Color": row[2]})
        return courses

    def getCourseColor(self, course_name):
        self._cursor = self._connection.cursor()
        self._cursor.execute("Select Course_Color from Courses WHERE Course_Name = %s;", [course_name])
        result = self._cursor.fetchone()

        color = "000000"
        if result is not None:
            color = result[0]
        return color
        
    def get_gardens(self):
        self._cursor = self._connection.cursor()
        self._cursor.execute("Select garden_name from gardens ORDER BY garden_name ASC;")
        gardens = []
        results = self._cursor.fetchall()
        for row in results:
            gardens.append(row[0])
        return gardens
        
    def doesCourseHaveQuiz(self, course_name):
        self._cursor = self._connection.cursor()
        self._cursor.execute("Select Has_Quiz from Courses WHERE Course_Name = %s;", [course_name])
        result = self._cursor.fetchone()

        has_quiz = False
        if result is not None:
            has_quiz = result[0]
        return has_quiz
        
    def setCourseColor(self, course_name, color):
        self._cursor = self._connection.cursor()
        self._cursor.execute("UPDATE Courses SET Course_Color = %s WHERE Course_Name = %s;", [color, course_name])
        self._cursor.execute("COMMIT")

    def getCourseLessons(self, coursename):
        self._cursor = self._connection.cursor()
        self._cursor.execute("SELECT Lesson_Name, Lesson_File_Path FROM Lessons WHERE Course_Name = %s", [coursename])
        results = self._cursor.fetchall()
        lessons = []
        for row in results:
            lessons.append({"name": row[0], "path": row[1]})
        return lessons

    def deleteQuiz(self, coursename):
        self._cursor = self._connection.cursor()
        self._cursor.execute("DELETE FROM Quiz_Questions WHERE Course_Name = %s;", [coursename])
        self._cursor.execute("COMMIT")

    def addQuiz(self, coursename, questions):
        self._cursor = self._connection.cursor()
        for question in questions:
            self._cursor.execute("INSERT into Quiz_Questions (Question_Text, Course_Name) values (%s, %s)", (question._Text, coursename))
            questionID = self._cursor.lastrowid
            for answer in question._Answers:
                self._cursor.execute("INSERT into Quiz_Answers (QuestionID, Answer_Text, Is_Correct) values (%s, %s, %s)", (questionID, answer._Text, answer._IsCorrect))

        self._cursor.execute("COMMIT")

    def getQuizQuestions(self, coursename):
        self._cursor = self._connection.cursor()
        self._cursor.execute("SELECT q.questionID as id, q.Question_Text as question, a.AnswerID as answerID, a.Answer_Text as answer, a.Is_Correct as correct FROM Quiz_Questions q, Quiz_Answers a WHERE q.Course_Name = %s AND q.questionID = a.questionID;", [coursename])

        results = self._cursor.fetchall()
        questions = {};
        for row in results:
            id = row[0];
            question = row[1];
            answerID = row[2];
            answer = row[3];
            correct = True if bytearray(row[4])[0] == 1 else False

            if answer is not None:
                answer = unicode(answer, errors='ignore')
                if id in questions:
                    questions[id]["answers"].append({"id": answerID, "answer": answer, "correct": correct});
                else:
                    questions[id] = {"question": question, "id": id};
                    questions[id]["answers"] = [{"id": answerID, "answer": answer, "correct": correct}];

        questionsArr = [];
        for id in questions:
            print(questions[id])
            questionsArr.append(questions[id])
        return questionsArr;

    def editQuestionTitle(self, questionID, questionText):
        self._cursor = self._connection.cursor()
        self._cursor.execute("UPDATE Quiz_Questions SET Question_Text = %s WHERE QuestionID = %s", (questionText, questionID))
        self._cursor.execute("COMMIT")

    def editAnswer(self, answerID, answerText, isCorrect):
        self._cursor = self._conneciton.cursor()
        self._cursor.execute("UPDATE Quiz_Answers SET Answer_Text = %s, Is_Correct = %s WHERE AnswerID = %s", (answerText, isCorrect, answerID))
        self._cursor.execute("COMMIT")

    def addQuizAttempt(self, coursename, username, passed, questions):
        self._cursor = self._connection.cursor()
        self._cursor.execute("INSERT into Quiz_Attempts (Course_Name, Username, Passed, Question1_ID, Answer1_ID, Question2_ID, Answer2_ID, Question3_ID, Answer3_ID, Question4_ID, Answer4_ID, Question5_ID, Answer5_ID, Question6_ID, Answer6_ID, Question7_ID, Answer7_ID, Question8_ID, Answer8_ID, Question9_ID, Answer9_ID, Question10_ID, Answer10_ID) values (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)", (coursename, username, passed, questions[0]["questionID"], questions[0]["answerID"], questions[1]["questionID"], questions[1]["answerID"], questions[2]["questionID"], questions[2]["answerID"], questions[3]["questionID"], questions[3]["answerID"], questions[4]["questionID"], questions[4]["answerID"], questions[5]["questionID"], questions[5]["answerID"], questions[6]["questionID"], questions[6]["answerID"], questions[7]["questionID"], questions[7]["answerID"], questions[8]["questionID"], questions[8]["answerID"], questions[9]["questionID"], questions[9]["answerID"]))
        self._cursor.execute("COMMIT")

    #Currently, this will get every chapter completed by every user.
    def getAllUserProgress(self):
        self._cursor = self._connection.cursor()
        self._cursor.execute("SELECT QA.ID, QA.Username as user, QA.Course_Name as course, C.Course_Order as chapter, QA.Passed FROM Quiz_Attempts QA, Courses C WHERE C.Course_Name = QA.Course_Name AND QA.ID in (SELECT MAX(ID) FROM Quiz_Attempts where Username = QA.Username and Course_Name = QA.Course_Name) ORDER BY QA.Username, C.Course_Order;")
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

        return userProgress;

    def getQuizAttempt(self, attemptID):
        self._cursor = self._connection.cursor()
        self._cursor.execute("SELECT QA.Course_Name, QQ.Question_Text, QAn.Answer_Text from Quiz_Questions QQ, Quiz_Attempts QA, Quiz_Answers QAn where QA.ID = %s and (QQ.QuestionID = QA.Question1_ID and QAn.AnswerID = QA.Answer1_ID or QQ.QuestionID = QA.Question2_ID and QAn.AnswerID = QA.Answer2_ID or QQ.QuestionID = QA.Question3_ID and QAn.AnswerID = QA.Answer3_ID    or QQ.QuestionID = QA.Question4_ID and QAn.AnswerID = QA.Answer4_ID    or QQ.QuestionID = QA.Question5_ID and QAn.AnswerID = QA.Answer5_ID    or QQ.QuestionID = QA.Question6_ID and QAn.AnswerID = QA.Answer6_ID    or QQ.QuestionID = QA.Question7_ID and QAn.AnswerID = QA.Answer7_ID    or QQ.QuestionID = QA.Question8_ID and QAn.AnswerID = QA.Answer8_ID    or QQ.QuestionID = QA.Question9_ID and QAn.AnswerID = QA.Answer9_ID    or QQ.QuestionID = QA.Question10_ID and QAn.AnswerID = QA.Answer10_ID);", [attemptID])
        results = self._cursor.fetchall()
        course = results[0][0]
        question = ""
        answer = ""
        response = []
        i = 1
        row = {"unit": course, "attempt":[{"question": results[0][i], "answer": results[0][i+1]}]}
        for i in range(1, len(results)):
            row["attempt"].append({"question": results[0][i], "answer": results[0][i+1]})
        return results

    def getPercentPassed(self, unit):
        self._cursor = self._connection.cursor()
        self._cursor.execute("SELECT (SELECT COUNT(QA1.Passed) FROM Quiz_Attempts QA1 WHERE QA1.Passed = 1 AND QA1.Course_Name = %s) / COUNT(QA2.Passed) FROM Quiz_Attempts QA2 WHERE QA2.Course_Name = %s;", (unit, unit))
        results = self._cursor.fetchall()
        return round(Decimal(results[0][0]) * 100, 2)

    def sendAlertEmail(self):
        self._cursor = self._connection.cursor()
        server = smtplib.SMTP_SSL('smtp.gmail.com', 465)
        fromaddr = "prisongardenapp@gmail.com"
        toaddr = "mattkoenig50@gmail.com"
        subject = "Test Email"
        content = "Just testing"

        msg = MIMEText(content)
        msg['From'] = fromaddr
        msg['To'] = toaddr
        msg['Subject'] = subject

        server.login('prisongardenapp@gmail.com', 'prisongardenapp2017')
        server.sendmail(fromaddr, toaddr, msg.as_string())
        server.close()

    def saveBedPlan(self, bedName, bedPlan, canvasData):
        self._cursor = self._connection.cursor()
        self._cursor.execute("INSERT into Bed_Plans (Bed_Name, Bed_Plan, Bed_Canvas) values (%s, %s, %s)", (bedName, bedPlan, canvasData))
        self._cursor.execute("COMMIT")

    def getBedPlans(self, bedName):
        self._cursor = self._connection.cursor()
        self._cursor.execute("SELECT PlanID, Bed_Plan, Updated_At, Created_At FROM Bed_Plans WHERE Bed_Name = %s", [bedName])
        return self._cursor.fetchall()

    def getBedCanvas(self, planID):
        self._cursor = self._connection.cursor()
        self._cursor.execute("SELECT Bed_Canvas FROM Bed_Plans WHERE PlanID = %s",[planID])
        return self._cursor.fetchone()

    def deleteBedPlan(self, planID):
        self._cursor = self._connection.cursor()
        self._cursor.execute("DELETE FROM Bed_Plans WHERE PlanID = %s", [planID])
        self._cursor.execute("COMMIT")

    def getDailyLogs(self):
        self._cursor = self._connection.cursor()
        self._cursor.execute("SELECT Username, Plant, Location, Quantity, DATE_FORMAT(Record_Date, '%m/%d/%Y') AS RecDate, Notes FROM Daily_Records ORDER BY Record_Date DESC")
        results = self._cursor.fetchall()
        logs = []
        for row in results:
            user = row[0]
            plant = row[1]
            location = row[2]
            quantity = row[3]
            logdate = row[4]
            notes = row[5]
            logs.append({"username": user, "plant": plant, "location": location, "quantity": quantity, "logdate": logdate, "notes": notes})
        return logs

    def addDailyLog(self, user, plant, location, quantity, date, notes):
        self._cursor = self._connection.cursor()
        self._cursor.execute("INSERT INTO Daily_Records (Username, Plant, Location, Quantity, Record_Date, Notes) VALUES (%s, %s, %s, %s, %s, %s)", (user, plant, location, quantity, date, notes))
        self._cursor.execute("COMMIT")
        
    def get_current_crops(self):
        self._cursor = self._connection.cursor()
        self._cursor.execute("SELECT crop FROM Current_Crops WHERE is_current = 1 ORDER BY crop ASC;")
        results = self._cursor.fetchall()
        crops = []
        for row in results:
            crops.append(row[0])
        return crops

    def get_all_crops(self):
        self._cursor = self._connection.cursor()
        self._cursor.execute("SELECT crop, is_current FROM Current_Crops ORDER BY crop ASC;")
        results = self._cursor.fetchall()
        crops = []
        for row in results:
            crops.append({'name': row[0], 'is_current': row[1]})
        return crops

    def add_crop(self, new_crop):
        self._cursor = self._connection.cursor()
        self._cursor.execute(
            "INSERT INTO Current_Crops (crop) VALUES (%s);", [new_crop])
        self._cursor.execute("COMMIT")

    def toggle_current_for_crop(self, crop, is_current):
        self._cursor = self._connection.cursor()
        self._cursor.execute(
            "UPDATE Current_Crops SET is_current = %s WHERE crop = %s;", [is_current, crop])
        self._cursor.execute("COMMIT")

    def mark_task_complete(self, task_id, username):
        self._cursor = self._connection.cursor()
        self._cursor.execute("UPDATE Tasks SET IsComplete = 1, CompletedBy = %s, CompletedDate = now() WHERE TaskId = %s;", (username, task_id))
        self._cursor.execute("COMMIT")
        
    def get_current_schedule(self):
        # First find current schedule Id
        self._cursor = self._connection.cursor()
        self._cursor.execute("SELECT ScheduleId FROM Schedules WHERE IsCurrent = 1;")
        cur_schedule_id = self._cursor.fetchone()
        
        # Now find tasks with that schedule Id:
        self._cursor.execute("SELECT Description, Day, IsComplete, TaskId FROM Tasks WHERE ScheduleId = %s ORDER BY Day;", [cur_schedule_id])
        task_rows = self._cursor.fetchall()
        
        # Python is neat - inits a list of 7 elements, each element is empty list:
        tasks_by_day = [[] for _ in range(7)]
        
        for task_row in task_rows:
            task = {'task': task_row[0], 'complete': task_row[2], 'id': task_row[3]}
            day_num = task_row[1]
            tasks_by_day[day_num].append(task)
            
        # Easier to work with on Frontend if
        # I give it the day name instead of number,
        # and each element is a tuple of day_str and 
        # the tasks list for that day
        # The array created above is already
        # sorted by day, since sunday is 0, sat is 6
        to_return = []
        for index, day_tasks_list in enumerate(tasks_by_day):
            if len(day_tasks_list) > 0:
                day_str = self.switch_day_num_to_string(index)
                tuple_to_append = (day_str, day_tasks_list)
                to_return.append( tuple_to_append )
                
        return to_return

    def create_schedule(self, username, day_tasks_dict):
        self._cursor = self._connection.cursor()
        
        # First thing to do is set the current schedule to non-current
        self._cursor.execute("UPDATE Schedules SET IsCurrent = 0 WHERE IsCurrent = 1")
        self._cursor.execute("COMMIT")
        
        # Next create a new current schedule:
        self._cursor.execute("INSERT INTO Schedules (IsCurrent, CreatedBy) VALUES (1, %s)", [username])
        
        # Get ID of the new schedule to use for inserting tasks:
        schedule_id = self._cursor.lastrowid
        
        self._cursor.execute("COMMIT") #for some reason returns 0 if commit call is before lastrowid...

        for day, tasks_list in day_tasks_dict.items():
            for task in tasks_list:
                self._cursor.execute("INSERT INTO Tasks (ScheduleId, Day, IsComplete, Description) VALUES (%s, %s, 0, %s)", (schedule_id, day, task))
                self._cursor.execute("COMMIT")
       
    day_dict = {
        0: 'Sunday',
        1: 'Monday',
        2: 'Tuesday',
        3: 'Wednesday',
        4: 'Thursday',
        5: 'Friday',
        6: 'Saturday'
    }
    
    def switch_day_num_to_string(self, day_num):
        return self.day_dict.get(day_num, 'Unknown Day')


# Class for passing quiz questions to the DB in a convenient object
class QuizQuestion:
    def __init__(self):
        self._Text = ""
        self._Answers = []


# Class for passing quiz answers to the DB in a convenient object
class QuizAnswer:
    def __init__(self):
        self._Text = ""
        self._IsCorrect = False
