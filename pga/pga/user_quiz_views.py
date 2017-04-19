from django.shortcuts import render, redirect, render_to_response
from django.http import HttpResponse
from django.contrib.auth.decorators import login_required
from django.core.serializers import json
import json

from pga.dataAccess import DataAccess


@login_required(login_url='/login/')
def quiz(request, course):
    db = DataAccess()
    questions = db.getQuizQuestions(course)
    return render(request, 'quiz.html', {'questions': questions, 'course': course})
    
def grade_quiz(request):
    return HttpResponse()


@login_required(login_url='/login/')
def quiz_results(request, course):
    db = DataAccess()
    username = request.user.username
    db.addQuizAttempt(course, username, 1)
    return render(request, 'quizResults.html', {'course': course})