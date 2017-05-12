#python imports:
import json

#Django imports:
from django.core.serializers import json
from django.http import HttpResponse, Http404
from django.shortcuts import render, redirect, render_to_response
from django.contrib.auth import authenticate, login
from django.views.generic.edit import CreateView, UpdateView
from django.template import loader
from django.template import *
from django.contrib.auth.decorators import login_required
from django.contrib.admin.views.decorators import staff_member_required
from django.views.generic import View

#pga imports:
from .forms import UserForm, RecordTableForm
from pga.dataAccess import DataAccess
from . import view_utils

#TODO - store this in DB?
gardens_color = '00AA00'


def login_view(request):
    username = request.POST.get('username')
    password = request.POST.get('password')
    user = authenticate(username=username, password=password)
    if user is not None:
        login(request, user)
        return redirect('home')
    else:
        return render(request, 'login.html', view_utils.get_home_page_dict())
        
@login_required(login_url='/login/')
def create_schedule(request):
    dict = view_utils.get_home_page_dict()
    dict.update({'days': ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday']})
    return render(request, 'create_schedule.html', view_utils.add_courses_to_dict(dict))

# Maintenance lessons:
@login_required(login_url='/login/')
def pests(request):
    return render(request, 'pests.html', view_utils.add_courses_to_dict({}))

@login_required(login_url='/login/')
def garden(request, garden):
    return render(request, 'garden.html', view_utils.add_courses_to_dict({'gardenName': garden,
        'course': garden, 'color': gardens_color}))

@login_required(login_url='/login/')
def savePlan(request):
    if request.is_ajax() and request.POST:
        bedName = request.POST.get('bedName')
        bedPlan = request.POST.get('bedPlan')
        bedCanvas = request.POST.get('bedCanvas')
        db = DataAccess()
        db.saveBedPlan(bedName, bedPlan, bedCanvas)
        response = {
            'status': 200,
            'message': 'Successfully saved changes on canvas'
        }
    else:
        response = {
            'status': 404,
            'message': 'Unable to save canvas as an image'
        }
    return HttpResponse(json.dumps(response), content_type='application/json')

@login_required(login_url='/login/')
def showPlans(request):
    bedName = request.GET['bedName']
    db = DataAccess()
    plans = db.getBedPlans(bedName)
    response = {
        'status': 200,
        'context': []
    }
    for plan in plans:
        p = {
            'planID': plan[0],
            'bedPlan': plan[1],
            'updatedAt': str(plan[2].now()),
            'createdAt': str(plan[3].now())
        }
        response["context"].append(p)

    return HttpResponse(json.dumps(response),content_type='application/json')

@login_required(login_url='/login/')
def getBedCanvas(request):
    planID = request.GET['planID']
    db = DataAccess()
    canvas = db.getBedCanvas(planID)
    return HttpResponse(canvas, content_type='application/json')

@login_required(login_url='/login/')
def deletePlan(request):
    if request.POST:
        planID = request.POST.get('planID')
        db = DataAccess()
        db.deleteBedPlan(planID)
        response = {
            'status': 200,
            'message': 'Successfully remove the selected plan'
        }
    else:
        response = {
            'status': 404,
            'message': 'Invalid request'
        }
    return HttpResponse(json.dumps(response), content_type='application/json')


@login_required(login_url='/login/')
def gardenNav(request):
    course = 'Gardens'
    db = DataAccess()
    lessons = db.getGardens()
        
    return render(request, 'gardenNav.html', view_utils.add_courses_to_dict({'lessons': lessons, 'course': course, 'color': gardens_color}))
    
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
        return redirect('/gardenNav/')
    
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
