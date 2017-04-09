'''
This file is simply for testing out the database functions with hardcoded values.
'''

from dataAccess import DataAccess, QuizQuestion, QuizAnswer

dataAccess = DataAccess()

#dataAccess.addLesson("Planting", "Digging a hole", "F:\Folder\Doc")
# dataAccess.addCourse("Picking", 2, "FakePath\Picking.html")
# dataAccess.addQuizAttempt("Planting", "mkoenig", True)
print dataAccess.getQuizAttempt(7)
