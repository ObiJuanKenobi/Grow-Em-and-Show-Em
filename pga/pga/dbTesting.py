'''
This file is simply for testing out the database functions with hardcoded values.
'''

from dataAccess import DataAccess, QuizQuestion, QuizAnswer

dataAccess = DataAccess()

#dataAccess.addLesson("Planting", "Digging a hole", "F:\Folder\Doc")
print(dataAccess.getLesson("Planting", "Digging a hole"))
