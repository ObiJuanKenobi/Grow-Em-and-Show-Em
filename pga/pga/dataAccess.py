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

    def addQuizAttempt(self, coursename, username, passed):
        #First, check to see if the user has taken the course before
        data = self._cursor.execute("SELECT Attempts FROM Quiz_Attempts WHERE Course_Name = %s AND Username = %s", (coursename, username))
        #If data is empty, this condition evaluates to True
        if not data:
            self._cursor.execute("INSERT into Quiz_Attempts (Course_Name, Username, Attempts, Passed) values (%s, %s, %s, %s)", (coursename, username, 1, passed))
        else:
            self._cursor.execute("UPDATE Quiz_Attempts SET Attempts = Attempts + 1, Passed = %s WHERE Course_Name = %s AND Username = %s", (passed, coursename, username))

    def getQuizQuestions(self, coursename):
        self._cursor.execute("SELECT q.QuestionID as id, q.Question_Text as question, a.Answer_Text as answer, a.Is_Correct as correct FROM Quiz_Questions q, Quiz_Answers a WHERE q.Course_Name = %s AND q.QuestionID = a.QuestionID;", [coursename])
        
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
        