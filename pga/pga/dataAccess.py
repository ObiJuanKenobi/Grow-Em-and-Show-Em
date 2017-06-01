import MySQLdb
import smtplib
from email.mime.text import MIMEText
from decimal import Decimal

class DataAccess:
    _connection = None
    _cursor = None

    # Establish DB connection on instantiation of a new DataAccess object
    def __init__(self):
        # "sddb.ece.iastate.edu"
        self._connection = MySQLdb.Connection(host="sddb.ece.iastate.edu", port = 3306, user = "may1713", passwd="gawrA75Nac!&", db="may1713_PrisonGardenApp")

    # Close the connection when this object is deleted or falls out of scope
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
        lesson_row = self._cursor.fetchone()
        return lesson_row[0]

    def deleteLesson(self, lessonname):
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

    def get_gardens_and_details(self):
        self._cursor = self._connection.cursor()
        self._cursor.execute("Select garden_name, garden_width, garden_height from gardens ORDER BY garden_name ASC;")
        gardens = []
        results = self._cursor.fetchall()
        for row in results:
            gardens.append({'name': row[0], 'width': row[1], 'height': row[2]})
        return gardens

    def add_garden(self, garden_name, width, height):
        self._cursor = self._connection.cursor()
        self._cursor.execute("INSERT INTO gardens (garden_name, garden_width, garden_height) VALUES (%s, %s, %s);",
                             (garden_name, width, height))
        self._cursor.execute("COMMIT")

    def edit_garden(self, garden_name, width, height):
        self._cursor = self._connection.cursor()
        self._cursor.execute("UPDATE gardens SET garden_width = %s, garden_height = %s WHERE garden_name = %s;",
                             (width, height, garden_name))
        self._cursor.execute("COMMIT")

    def delete_garden(self, garden_name):
        self._cursor = self._connection.cursor()
        self._cursor.execute("DELETE FROM gardens WHERE garden_name = %s;",
                             [garden_name])

        # Also delete plans associated with this garden:
        self._cursor.execute("DELETE FROM Bed_Plans WHERE Bed_Name = %s;",
                             [garden_name])

        self._cursor.execute("COMMIT")

    def get_crops_overview(self):
        crops_dict = {}

        self._cursor = self._connection.cursor()
        self._cursor.execute("SELECT Crop, Crop_Subtype, sum(Quantity), Quantity_Units FROM Planting_Records GROUP BY Crop, Crop_Subtype, Quantity_Units;")
        planting_results = self._cursor.fetchall()

        for planting_row in planting_results:
            crop = planting_row[0]
            subtype = planting_row[1]
            units = planting_row[3]
            num = planting_row[2]

            key = crop + " - " + subtype

            if key not in crops_dict:
                crops_dict[key] = {'planted': [], 'harvested': []}
            crops_dict[key]['planted'].append({'units': units, 'num': num})

        self._cursor.execute(
            "SELECT Crop, Crop_Subtype, sum(Quantity), Quantity_Units FROM Harvest_Records GROUP BY Crop, Crop_Subtype, Quantity_Units;")
        harvest_results = self._cursor.fetchall()

        for harvest_row in harvest_results:
            crop = harvest_row[0]
            subtype = harvest_row[1]
            units = harvest_row[3]
            num = harvest_row[2]

            key = crop + " - " + subtype

            if key not in crops_dict:
                crops_dict[key] = {'planted': [], 'harvested': []}
            crops_dict[key]['harvested'].append({'units': units, 'num': num})

        return crops_dict

        
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

    # Adds a list of QuizQuestion objects to the given course
    # Can use a list of a single element to add a single question
    def add_quiz(self, course_name, questions):
        self._cursor = self._connection.cursor()
        for question in questions:
            self._cursor.execute("INSERT into Quiz_Questions (Question_Text, Course_Name) values (%s, %s)", (question._Text, course_name))
            question_id = self._cursor.lastrowid
            for answer in question._Answers:
                self._cursor.execute("INSERT into Quiz_Answers (QuestionID, Answer_Text, Is_Correct) values (%s, %s, %s)", (question_id, answer._Text, answer._IsCorrect))

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

    def edit_question_title(self, questionID, questionText):
        self._cursor = self._connection.cursor()
        self._cursor.execute("UPDATE Quiz_Questions SET Question_Text = %s WHERE QuestionID = %s", (questionText, questionID))
        self._cursor.execute("COMMIT")

    def edit_quiz_answer(self, answerID, answerText, isCorrect):
        self._cursor = self._connection.cursor()
        self._cursor.execute("UPDATE Quiz_Answers SET Answer_Text = %s, Is_Correct = %s WHERE AnswerID = %s", (answerText, isCorrect, answerID))
        self._cursor.execute("COMMIT")

    def delete_quiz_question(self, question_id):
        # Need to first delete answers associated with this question:
        self._cursor = self._connection.cursor()
        self._cursor.execute("DELETE FROM Quiz_Answers WHERE QuestionID = %s", [question_id])
        self._cursor.execute("COMMIT")

        # Then delete the question itself:
        self._cursor = self._connection.cursor()
        self._cursor.execute("DELETE FROM Quiz_Questions WHERE QuestionID = %s", [question_id])
        self._cursor.execute("COMMIT")

    def addQuizAttempt(self, coursename, username, passed, questions):
        self._cursor = self._connection.cursor()
        self._cursor.execute("INSERT into Quiz_Attempts (Course_Name, Username, Passed, Question1_ID, Answer1_ID, Question2_ID, Answer2_ID, Question3_ID, Answer3_ID, Question4_ID, Answer4_ID, Question5_ID, Answer5_ID, Question6_ID, Answer6_ID, Question7_ID, Answer7_ID, Question8_ID, Answer8_ID, Question9_ID, Answer9_ID, Question10_ID, Answer10_ID) values (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)", (coursename, username, passed, questions[0]["questionID"], questions[0]["answerID"], questions[1]["questionID"], questions[1]["answerID"], questions[2]["questionID"], questions[2]["answerID"], questions[3]["questionID"], questions[3]["answerID"], questions[4]["questionID"], questions[4]["answerID"], questions[5]["questionID"], questions[5]["answerID"], questions[6]["questionID"], questions[6]["answerID"], questions[7]["questionID"], questions[7]["answerID"], questions[8]["questionID"], questions[8]["answerID"], questions[9]["questionID"], questions[9]["answerID"]))
        self._cursor.execute("COMMIT")

    # Currently, this will get every chapter completed by every user.
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

    def save_bed_plan(self, bed_name, bed_plan, canvas_data, username):
        self._cursor = self._connection.cursor()
        self._cursor.execute("INSERT into Bed_Plans (Bed_Name, Bed_Plan, Bed_Canvas, Created_By, Updated_At, Updated_By) values (%s, %s, %s, %s, now(), %s)", (bed_name, bed_plan, canvas_data, username, username))
        plan_id = self._cursor.lastrowid
        self._cursor.execute("COMMIT")
        return plan_id

    def update_bed_plan(self, plan_id, canvas_data, username):
        self._cursor = self._connection.cursor()
        self._cursor.execute(
            "UPDATE Bed_Plans SET Bed_Canvas = %s, Updated_At = now(), Updated_By = %s WHERE PlanID = %s",
            (canvas_data, username, plan_id))
        self._cursor.execute("COMMIT")

    def get_bed_plans(self, bed_name):
        self._cursor = self._connection.cursor()
        self._cursor.execute("SELECT PlanID, Bed_Plan, Updated_At, Created_At FROM Bed_Plans WHERE Bed_Name = %s AND Is_Deleted = 0 AND Is_Current = 0 AND Was_Current = 0", [bed_name])
        return self._cursor.fetchall()

    def get_past_bed_plans(self, garden_name):
        self._cursor = self._connection.cursor()
        self._cursor.execute(
            "SELECT PlanID, Year(Marked_As_Current_At), Marked_As_Current_At as year, Marked_As_Current_By FROM Bed_Plans WHERE Bed_Name = %s AND Was_Current = 1 Order By Marked_As_Current_At DESC",
            [garden_name])
        results = self._cursor.fetchall()

        year_dict = {}
        for row in results:
            plan_id = row[0]
            year = row[1]
            date = row[2]
            marked_current_by = row[3]

            if year not in year_dict:
                year_dict[year] = []

            year_dict[year].append({'id': plan_id, 'date': date, 'marked_current_by': marked_current_by})

        return year_dict

    # Gathers all plan data for a given garden, for use on admin side
    def get_all_bed_plans(self, garden_name):
        self._cursor = self._connection.cursor()

        # Get current:
        current = self.get_current_bed_plan_data(garden_name)

        # Get existing plans:
        existing = self.get_existing_bed_plans_for_garden(garden_name)

        # Get past plans
        past = self.get_past_bed_plans(garden_name)

        # Get user-deleted plans:
        deleted = self.get_deleted_bed_plans_for_garden(garden_name)

        return {'current': current, 'existing': existing, 'past': past, 'deleted': deleted}


    def get_bed_canvas(self, plan_id):
        self._cursor = self._connection.cursor()
        self._cursor.execute("SELECT Bed_Canvas FROM Bed_Plans WHERE PlanID = %s", [plan_id])
        return self._cursor.fetchone()

    def get_current_bed_canvas(self, garden_name):
        self._cursor = self._connection.cursor()
        self._cursor.execute("SELECT Bed_Canvas FROM Bed_Plans WHERE Bed_Name = %s AND Is_Current = 1", [garden_name])
        return self._cursor.fetchone()

    def get_bed_plan_data(self, plan_id):
        self._cursor = self._connection.cursor()
        self._cursor.execute("SELECT Bed_Plan, Created_By, Created_At, Updated_By, Updated_At, PlanID FROM Bed_Plans WHERE PlanID = %s", [plan_id])
        results = self._cursor.fetchall()

        if len(results) == 0:
            return None

        row = results[0]
        data = {'plan_name': row[0],
            'created_by': row[1],
            'created_date': str(row[2]),
            'updated_by': row[3],
            'updated_date': str(row[4]),
            'plan_id': row[5]}

        return data

    def get_current_bed_plan_data(self, garden_name):
        self._cursor = self._connection.cursor()
        self._cursor.execute("SELECT Bed_Plan, Marked_As_Current_By, Marked_As_Current_At, PlanID FROM Bed_Plans WHERE Bed_Name = %s AND Is_Current = 1", [garden_name])
        results = self._cursor.fetchall()

        if len(results) == 0:
            return None

        row = results[0]
        data = {'plan_name': row[0],
            'created_by': row[1],
            'date': str(row[2]),
            'plan_id': row[3]}

        return data

    # Gets existing plans - not the current, not past currents, and not deleted ones:
    def get_existing_bed_plans_for_garden(self, garden_name):
        self._cursor = self._connection.cursor()
        self._cursor.execute("SELECT Bed_Plan, Created_By, Created_At, Updated_By, Updated_At, PlanID FROM Bed_Plans WHERE Bed_Name = %s AND Is_Current = 0 AND Was_Current = 0 AND Is_Deleted = 0", [garden_name])
        results = self._cursor.fetchall()

        if len(results) == 0:
            return None

        all_data = []
        for row in results:

            data = {'plan_name': row[0],
                'created_by': row[1],
                'created_date': str(row[2]),
                'updated_by': row[3],
                'updated_date': str(row[4]),
                'plan_id': row[5]}
            all_data.append(data)

        return all_data

    # Gets existing plans - not the current, not past currents, and not deleted ones:
    def get_deleted_bed_plans_for_garden(self, garden_name):
        self._cursor = self._connection.cursor()
        self._cursor.execute(
            "SELECT Bed_Plan, Created_By, Created_At, Deleted_By, Deleted_At, PlanID FROM Bed_Plans WHERE Bed_Name = %s AND Is_Current = 0 AND Was_Current = 0 AND Is_Deleted = 1",
            [garden_name])
        results = self._cursor.fetchall()

        if len(results) == 0:
            return None

        all_data = []
        for row in results:
            data = {'plan_name': row[0],
                    'created_by': row[1],
                    'created_date': str(row[2]),
                    'deleted_by': row[3],
                    'deleted_date': str(row[4]),
                    'plan_id': row[5]}
            all_data.append(data)

        return all_data

    def mark_bed_plan_as_current(self, garden_name, plan_id, username):
        self._cursor = self._connection.cursor()

        # Have to update a current one as "Was_Current"
        self._cursor.execute(
            "UPDATE Bed_Plans SET Is_Current = 0, Was_Current = 1 WHERE Is_Current = 1 AND Bed_Name = %s",
            [garden_name])


        self._cursor.execute("UPDATE Bed_Plans SET Is_Current = 1, Marked_As_Current_By = %s, Marked_As_Current_At = now() WHERE PlanID = %s", (username, plan_id))
        self._cursor.execute("COMMIT")

    # Called from user-side, doesn't actually delete, just hides plan from users
    def delete_bed_plan(self, plan_id, username):
        self._cursor = self._connection.cursor()
        self._cursor.execute("UPDATE Bed_Plans SET Is_Deleted = 1, Deleted_By = %s, Deleted_At = now() WHERE PlanID = %s", (username, plan_id))
        self._cursor.execute("COMMIT")

    # Called when admin deletes a plan, actually deletes
    def admin_delete_bed_plan(self, plan_id):
        self._cursor = self._connection.cursor()
        self._cursor.execute(
            "DELETE FROM Bed_Plans WHERE PlanID = %s;", [plan_id])
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

    def get_harvest_records(self):
        self._cursor = self._connection.cursor()
        self._cursor.execute(
            "SELECT RecordId, Username, Crop, Quantity, Location, DATE_FORMAT(Date, '%m/%d/%Y') AS RecDate, YEAR(Date) as year, Crop_Subtype, Quantity_Units FROM Harvest_Records ORDER BY Date DESC")
        results = self._cursor.fetchall()

        year_records_dict = {}
        for row in results:
            rid = row[0]
            user = row[1]
            crop = row[2]
            quantity = row[3]
            location = row[4]
            date = row[5]
            year = row[6]
            subtype = row[7]
            units = row[8]

            if year not in year_records_dict:
                year_records_dict[year] = []

            year_records_dict[year].append({'id': rid, 'username': user, 'date': date, 'crop': crop, 'location': location, 'quantity': quantity, 'subtype': subtype, 'units': units})

        # Put data into good format for frontend templates:
        records_list = []
        for year, records in year_records_dict.items():
            records_list.append({'year': year, 'records': records})

        records_list_sorted = sorted(records_list, key=lambda k: k['year'], reverse=True)

        return records_list_sorted

    def insert_harvest_record(self, username, date, crop, subtype, location, quantity, units):
        self._cursor = self._connection.cursor()
        self._cursor.execute(
            "INSERT INTO Harvest_Records (Username, Crop, Crop_Subtype, Quantity, Quantity_Units, Date, Location) VALUES (%s, %s, %s, %s, %s, %s, %s)", (username, crop, subtype, quantity, units, date, location))
        self._cursor.execute("COMMIT")

    def delete_harvest_record(self, record_id):
        self._cursor = self._connection.cursor()
        self._cursor.execute(
            "DELETE FROM Harvest_Records WHERE RecordId = %s", [record_id])
        self._cursor.execute("COMMIT")

    def get_planting_records(self):
        self._cursor = self._connection.cursor()
        self._cursor.execute(
            "SELECT RecordId, Username, Crop, Quantity, Location, DATE_FORMAT(Date, '%m/%d/%Y') AS RecDate, YEAR(Date) as year, Crop_Subtype, Quantity_Units FROM Planting_Records ORDER BY Date DESC")
        results = self._cursor.fetchall()

        year_records_dict = {}
        for row in results:
            rid = row[0]
            user = row[1]
            crop = row[2]
            quantity = row[3]
            location = row[4]
            date = row[5]
            year = row[6]
            subtype = row[7]
            units = row[8]

            if year not in year_records_dict:
                year_records_dict[year] = []

            year_records_dict[year].append({'id': rid, 'username': user, 'date': date, 'crop': crop, 'location': location, 'quantity': quantity, 'subtype': subtype, 'units': units})

        # Put data into good format for frontend templates:
        records_list = []
        for year, records in year_records_dict.items():
            records_list.append({'year': year, 'records': records})

        records_list_sorted = sorted(records_list, key=lambda k: k['year'], reverse=True)

        return records_list_sorted

    def insert_planting_record(self, username, date, crop, crop_subtype, location, quantity, units):
        self._cursor = self._connection.cursor()
        self._cursor.execute(
            "INSERT INTO Planting_Records (Username, Crop, Crop_Subtype, Quantity, Quantity_Units, Date, Location) VALUES (%s, %s, %s, %s, %s, %s, %s)", (username, crop, crop_subtype, quantity, units, date, location))
        self._cursor.execute("COMMIT")

    def delete_planting_record(self, record_id):
        self._cursor = self._connection.cursor()
        self._cursor.execute(
            "DELETE FROM Planting_Records WHERE RecordId = %s", [record_id])
        self._cursor.execute("COMMIT")

    def get_garden_notes(self):
        self._cursor = self._connection.cursor()
        self._cursor.execute(
            "SELECT RecordId, Username, Crop, Notes, Location, DATE_FORMAT(Date, '%m/%d/%Y') AS RecDate, YEAR(Date) as year, Crop_Subtype FROM Garden_Notes ORDER BY Date DESC")
        results = self._cursor.fetchall()

        year_records_dict = {}
        for row in results:
            rid = row[0]
            user = row[1]
            crop = row[2]
            notes = row[3]
            location = row[4]
            date = row[5]
            year = row[6]
            subtype = row[7]

            if year not in year_records_dict:
                year_records_dict[year] = []

            year_records_dict[year].append({'id': rid, 'username': user, 'date': date, 'crop': crop, 'subtype': subtype,
                                            'location': location, 'notes': notes})

        # Put data into good format for frontend templates:
        records_list = []
        for year, records in year_records_dict.items():
            records_list.append({'year': year, 'records': records})

        records_list_sorted = sorted(records_list, key=lambda k: k['year'], reverse=True)

        return records_list_sorted

    def insert_garden_note(self, username, date, crop, crop_subtype, location, note):
        self._cursor = self._connection.cursor()
        self._cursor.execute(
            "INSERT INTO Garden_Notes (Username, Crop, Crop_Subtype, Notes, Date, Location) VALUES (%s, %s, %s, %s, %s, %s);", (username, crop, crop_subtype, note, date, location))
        self._cursor.execute("COMMIT")

    def delete_garden_note(self, record_id):
        self._cursor = self._connection.cursor()
        self._cursor.execute(
            "DELETE FROM Garden_Notes WHERE RecordId = %s", [record_id])
        self._cursor.execute("COMMIT")
        print("DELETED GARDEN NOTE")

    # def addDailyLog(self, user, plant, location, quantity, date, notes):
    #     self._cursor = self._connection.cursor()
    #     self._cursor.execute("INSERT INTO Daily_Records (Username, Plant, Location, Quantity, Record_Date, Notes) VALUES (%s, %s, %s, %s, %s, %s)", (user, plant, location, quantity, date, notes))
    #     self._cursor.execute("COMMIT")
        
    def get_current_crops(self):
        self._cursor = self._connection.cursor()
        self._cursor.execute("SELECT crop FROM Current_Crops WHERE is_current = 1 ORDER BY crop ASC;")
        results = self._cursor.fetchall()
        crops = []
        for row in results:
            crop_dict = {'name': row[0]}

            self._cursor.execute("Select Subtype FROM Crop_Subtypes WHERE Crop = %s", [row[0]])
            subtype_results = self._cursor.fetchall()
            subtypes = []
            for subtype_row in subtype_results:
                subtypes.append(subtype_row[0])

            crop_dict['subtypes'] = subtypes
            crops.append(crop_dict)

        return crops

    def get_all_crops(self):
        self._cursor = self._connection.cursor()
        self._cursor.execute("SELECT crop, is_current FROM Current_Crops ORDER BY crop ASC;")
        results = self._cursor.fetchall()
        crops = []
        for row in results:
            crop_info = {'name': row[0], 'is_current': row[1]}

            self._cursor.execute("Select Subtype FROM Crop_Subtypes WHERE Crop = %s", [row[0]])
            subtype_results = self._cursor.fetchall()
            subtypes = []
            for subtype_row in subtype_results:
                subtypes.append(subtype_row[0])

            crop_info['subtypes'] = subtypes
            crops.append(crop_info)

        return crops

    def add_crop(self, new_crop):
        self._cursor = self._connection.cursor()
        self._cursor.execute(
            "INSERT INTO Current_Crops (crop) VALUES (%s);", [new_crop])
        self._cursor.execute("COMMIT")

    def add_crop_subtype(self, crop, subtype):
        self._cursor = self._connection.cursor()
        self._cursor.execute(
            "INSERT INTO Crop_Subtypes (Crop, Subtype) VALUES (%s, %s);", (crop, subtype))
        self._cursor.execute("COMMIT")

    def remove_crop_subtype(self, crop, subtype):
        self._cursor = self._connection.cursor()
        self._cursor.execute(
            "DELETE FROM Crop_Subtypes WHERE Crop = %s AND Subtype = %s;", (crop, subtype))
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
        return self.get_tasks_for_schedule_id(cur_schedule_id)

    def get_tasks_for_schedule_id(self, schedule_id):
        # Now find tasks with that schedule Id:
        self._cursor.execute("SELECT Description, Day, IsComplete, TaskId, CompletedBy, CompletedDate FROM Tasks WHERE ScheduleId = %s ORDER BY Day;", [schedule_id])
        task_rows = self._cursor.fetchall()
        
        # Python is neat - inits a list of 7 elements, each element is empty list:
        tasks_by_day = [[] for _ in range(7)]
        
        for task_row in task_rows:
            task = {'task': task_row[0], 'complete': task_row[2], 'id': task_row[3], 'completed_by': task_row[4],
                    'completed_date': task_row[5]}
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
            day_str = self.switch_day_num_to_string(index)
            tuple_to_append = (day_str, day_tasks_list)
            to_return.append(tuple_to_append)
                
        return to_return

    def get_all_schedules(self):
        # First find all schedule Id's
        self._cursor = self._connection.cursor()
        self._cursor.execute("SELECT ScheduleId, CreatedBy, DateCreated, IsCurrent FROM Schedules ORDER BY DateCreated DESC;")
        schedule_rows = self._cursor.fetchall()

        schedules = []
        for schedule_row in schedule_rows:
            schedule_id = schedule_row[0]
            created_by = schedule_row[1]
            date_created = schedule_row[2]
            is_current = schedule_row[3]
            schedule = self.get_tasks_for_schedule_id(schedule_id)

            schedules.append({'id': schedule_id, 'created_by': created_by, 'date_created': date_created,
                              'is_current': is_current, 'schedule': schedule})

        return schedules

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

        0: 'Monday',
        1: 'Tuesday',
        2: 'Wednesday',
        3: 'Thursday',
        4: 'Friday',
        5: 'Saturday',
        6: 'Sunday',
    }
    
    def switch_day_num_to_string(self, day_num):
        return self.day_dict.get(day_num, 'Unknown Day')

    def delete_schedule(self, schedule_id):
        self._cursor = self._connection.cursor()

        # First delete tasks associated with this schedule:
        self._cursor.execute("DELETE FROM Tasks WHERE ScheduleId = %s", [schedule_id])

        # Then delete schedule entry:
        self._cursor.execute("DELETE FROM Schedules WHERE ScheduleId = %s", [schedule_id])

        self._cursor.execute("COMMIT")

    def make_current_schedule(self, schedule_id):
        self._cursor = self._connection.cursor()

        # First thing to do is set the current schedule to non-current
        self._cursor.execute("UPDATE Schedules SET IsCurrent = 0 WHERE IsCurrent = 1")
        self._cursor.execute("COMMIT")

        # Now just make this one current:
        self._cursor.execute("UPDATE Schedules SET IsCurrent = 1 WHERE ScheduleId = %s", [schedule_id])
        self._cursor.execute("COMMIT")


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
