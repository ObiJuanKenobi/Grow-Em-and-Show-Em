#python imports:
import json
import random

#Django imports:
from django.shortcuts import render, redirect, render_to_response
from django.http import HttpResponse
from django.contrib.auth.decorators import login_required


from pga.dataAccess import DataAccess
from pga.view_utils import add_courses_to_dict

# TODO could store in DB and make editable
num_questions = 10

@login_required(login_url='/login/')
def quiz(request, course):
    db = DataAccess()
    questions = db.getQuizQuestions(course)
    
    #get random 'num_questions' questions 
    # (or all if there are <= num_questions):
    if len(questions) > num_questions:
        questions = random.sample(questions, num_questions)
        
    #Shuffle the questions & answers (also remove 'None' from answers):
    random.shuffle(questions)
    
    for idx, question in enumerate(questions):
        answers = questions[idx]['answers']
        valid_answers = [a for a in answers if a['answer'] is not None]
        random.shuffle(valid_answers)
        questions[idx]['answers'] = valid_answers
    
    color = db.getCourseColor(course)
    return render(request, 'quiz.html', add_courses_to_dict({'questions': questions, 'course': course, 'color': color}))
    
@login_required(login_url='/login/')
def grade_quiz(request, course):

    response = {}
    
    if request.method == "POST":
        
        db = DataAccess()
        all_questions = db.getQuizQuestions(course)
        
        questions = request.POST.getlist('questions[]')
        answers = request.POST.getlist('answers[]')
        
        #Stores info to be sent back to front-end:
        graded_questions = []
        
        #Stores info to be sent to DB:
        users_attempt = []
        
        #Sets how many correct questions are needed to consider as passed:
        needed_to_pass = 10 
        
        #Tracks how many questions user gets right:
        num_correct = 0
        
        loop = range(0, len(questions))
        for index in loop:
            question_id = int(questions[index])
            answer_id = int(answers[index])
            users_attempt.append({'questionID': question_id, 'answerID': answer_id})
            
            for q in all_questions:
                if q['id'] == question_id:
                    user_correct, correct_id = check_answers(q['answers'], answer_id)
                    if user_correct:
                        num_correct += 1
                    gq = GradedQuestion(question_id, correct_id, user_correct)
                    graded_questions.append(gq.toJSON())
 
        username = request.user.username
        passed = 0
        if num_correct >= needed_to_pass:
            passed = 1
        #Right now there are quizzes with < 10 questions, so if they got all right count as passed
        elif num_correct == len(graded_questions): 
            passed = 1
            
        # TODO - addQuizAttempt expects 10 questions always, is there a better approach?
        while len(users_attempt) < 10:
            users_attempt.append({'questionID': -1, 'answerID': -1})
        
        db.addQuizAttempt(course, username, passed, users_attempt)
        
        if passed == 1:
            response.update({'redirect_url': '/quizResults/' + course, 'passed': True})
        else:
            response.update({'redirect_url': '/quiz/' + course})

        response.update({
            'status': 200,
            'results': graded_questions,
            'message': 'Quiz graded'
        })
    else:
        response.update({
            'status': 404,
            'message': 'Invalid request'
        })
    return HttpResponse(json.dumps(response), content_type='application/json')
    
    
def check_answers(answers, users_answer):
    for answer in answers:
        if answer['correct'] == True:
            return users_answer == answer['id'], answer['id']
            
class GradedQuestion:
    def __init__(self, question_id, answer_id, user_correct):
        self.question_id = question_id
        self.answer_id = answer_id
        self.user_correct = user_correct
        
    def toJSON(self):
        return json.dumps(self, sort_keys=True, indent=4, default=lambda o: o.__dict__)

@login_required(login_url='/login/')
def quiz_results(request, course):
    db = DataAccess()
    color = db.getCourseColor(course)
    return render(request, 'quizResults.html', add_courses_to_dict({'course': course, 'color': color}))