from django.core.serializers import json
from django.http import HttpResponse, Http404

from pga.dataAccess import DataAccess, QuizQuestion, QuizAnswer

import json


def edit_quiz_question(request):
    if request.method == 'POST':
    
        question_id = request.POST.get('questionid')
        new_question = request.POST.get('newquestion')
        
        db = DataAccess()
        db.edit_question_title(question_id, new_question)
        
        response = {
            'status': 200,
            'message': 'Successfully updated quiz'
        }
    else:
        response = {
            'status': 404,
            'message': 'Invalid request'
        }
    return HttpResponse(json.dumps(response), content_type='application/json')


def edit_quiz_answer(request):
    if request.method == 'POST':
    
        answer_id = request.POST.get('answerid')
        new_answer = request.POST.get('newanswer')
        is_correct_str = request.POST.get('iscorrect')
        
        # Getting bool's from ajax don't convert to python bools. fun.
        is_correct = False
        if is_correct_str == u'true':
            is_correct = True
        
        db = DataAccess()
        db.edit_quiz_answer(answer_id, new_answer, is_correct)
        
        response = {
            'status': 200,
            'message': 'Successfully updated quiz'
        }
    else:
        response = {
            'status': 404,
            'message': 'Invalid request'
        }
    return HttpResponse(json.dumps(response), content_type='application/json')


def delete_quiz_question(request):
    if request.method == 'POST':

        question_id = request.POST.get('questionId')

        db = DataAccess()
        db.delete_quiz_question(question_id)

        response = {
            'status': 200,
            'message': 'Successfully updated quiz'
        }
    else:
        response = {
            'status': 404,
            'message': 'Invalid request'
        }
    return HttpResponse(json.dumps(response), content_type='application/json')


def add_quiz_question(request):
    if request.method == 'POST':

        question = request.POST.get('question')
        answers = request.POST.getlist('answers[]')

        # Subtract 1 because UI starts at 1:
        correct = int(request.POST.get('correct')) - 1
        course = request.POST.get('course')

        question_object = QuizQuestion()
        question_object._Text = question
        for answer in answers:
            answer_object = QuizAnswer()
            answer_object._Text = answer
            question_object._Answers.append(answer_object)

        question_object._Answers[correct]._IsCorrect = True
        question_list = [question_object]

        db = DataAccess()
        db.add_quiz(course, question_list)

        response = {
            'status': 200,
            'message': 'Successfully updated quiz'
        }
    else:
        response = {
            'status': 404,
            'message': 'Invalid request'
        }
    return HttpResponse(json.dumps(response), content_type='application/json')
