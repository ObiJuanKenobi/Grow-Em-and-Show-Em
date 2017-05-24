# python imports:
import json

# Django imports:
from django.core.serializers import json
from django.http import HttpResponse, Http404
from django.shortcuts import render, redirect, render_to_response
from django.contrib.auth import authenticate, login
from django.views.generic.edit import CreateView, UpdateView
from django.template import loader
from django.template import *
from django.contrib.auth.decorators import login_required
from django.views.generic import View

# pga imports:
from .forms import UserForm
from pga.dataAccess import DataAccess
from . import view_utils

def login_view(request):
    username = request.POST.get('username')
    password = request.POST.get('password')
    user = authenticate(username=username, password=password)
    if user is not None:
        login(request, user)
        return redirect('home')
    else:
        return render(request, 'login.html', view_utils.get_home_page_dict())


# Maintenance lessons:
@login_required(login_url='/login/')
def pests(request):
    return render(request, 'pests.html', view_utils.add_courses_to_dict({}))


@login_required(login_url='/login/')
def courseNav(request, course):
    db = DataAccess()
    color = db.getCourseColor(course)
    lessons = db.getCourseLessons(course)
    for lesson in lessons:
        link = DataAccess().getLesson(course, lesson['name'])
        lesson['link'] = link.replace(".", "", 1)
        
    has_quiz = db.doesCourseHaveQuiz(course)
    
    completed_courses = db.getCompletedCoursesForUser(request.user.username)
    passed = False 
    if course in completed_courses:
        passed = True
        
    return render(request, 'courseNav.html', view_utils.add_courses_to_dict({'lessons': lessons, 'course': course.replace('-', ' '), 'color': color, 'has_quiz': has_quiz, 'passed': passed}))


@login_required(login_url='/login/')
def lesson(request, course, lesson):
    db = DataAccess()
    color = db.getCourseColor(course)
    lesson_file_path = DataAccess().getLesson(course, lesson)
    
    #records url does not have the preceding '.'
    if "static" in lesson_file_path:
        lesson_file_path = lesson_file_path.replace(".", "", 1)#lesson_file_path.replace("./static/", "", 1)
    
    if "Garden Planning" in lesson:
        return redirect('/gardensNav/')

    if "Record Keeping" in lesson:
        return redirect('/recordsNav/')
    
    return render(request, 'lesson.html', view_utils.add_courses_to_dict({'course': course, 'lesson': lesson, 'color': color, 'lesson_file_path': lesson_file_path}))
    
# @login_required(login_url='/login/')
# def quiz_wrapper(request, course):
    # db = DataAccess()
    # color = db.getCourseColor(course)
    # lesson_file_path = "/quiz/" + course
    
    # return render(request, 'lesson.html', add_courses_to_dict({'course': course, 'color': color, 'lesson_file_path': lesson_file_path}))
    

class UserFormView(View):
    form_class = UserForm
    template_name = 'registration_form.html'

    def get(self, request):
        form = self.form_class(None)
        dict = get_home_page_dict()
        dict['form'] = form
        return render(request, self.template_name, dict)

    def post(self, request):
        form = self.form_class(request.POST)
        if form.is_valid():
            db = DataAccess()
            user = form.save(commit=False)
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']
            first_name = form.cleaned_data['first_name']
            last_name = form.cleaned_data['last_name']
            user.set_password(password)
            user.save()
            db.addUser(username, password, first_name, last_name)
            db.__del__()
            user = authenticate(username=username, password=password)

            if user is not None:
                if user.is_active:
                    login(request, user)
                    return redirect('home')

        dict = get_home_page_dict()
        dict['form'] = form
        return render(request, self.template_name, dict)
