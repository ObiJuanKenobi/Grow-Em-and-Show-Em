from django.core.serializers import json
from django.http import HttpResponse, Http404
from django.shortcuts import render, redirect, render_to_response
from django.contrib.auth import authenticate, login
from django.views.generic.edit import CreateView, UpdateView
from django.template import loader
from django.template import *
from django.contrib.auth.decorators import login_required
from django.contrib.admin.views.decorators import staff_member_required
from pga.dataAccess import DataAccess
from django.views.generic import View
from .forms import UserForm, RecordTableForm
import json


def home_page(request):
    authenticated = request.user.is_authenticated()
    return render(request, 'home.html', add_courses_to_dict(get_home_page_dict(), authenticated))


def login_view(request):
    username = request.POST.get('username')
    password = request.POST.get('password')
    user = authenticate(username=username, password=password)
    if user is not None:
        login(request, user)
        return redirect('home')
    else:
        return render(request, 'login.html', add_courses_to_dict(get_home_page_dict(), False))

@login_required(login_url='/login/')
def createRecordTable_Form(request):
    if request.method == 'POST':
        form = RecordTableForm(request.POST)
        if form.is_valid():
            if request.user.is_authenticated():
                plant = form.cleaned_data['plant']
                quantity = form.cleaned_data['quantity']
                location = form.cleaned_data['location']
                notes = form.cleaned_data['notes']
                year = form.cleaned_data['year']
                month = form.cleaned_data['month']
                day = form.cleaned_data['day']
                username = request.user.get_username()
                time = year + '/' + month + '/' + day
                db = DataAccess()
                db.addDailyLog(user=username, plant=plant, location=location, quantity=quantity, date=time, notes=notes)
                db.__del__()
                return redirect('table_home')
    else:
        form = RecordTableForm()
    return render(request, 'recordstable_form.html', add_courses_to_dict({'form': form}))
@login_required(login_url='/login/')
def recordTable_Home(request):
    db = DataAccess()
    logs = db.getDailyLogs()

    return render(request, 'recordstable_home.html', add_courses_to_dict({'logs' : logs}))

# Maintenance lessons:
@login_required(login_url='/login/')
def pests(request):
    return render(request, 'pests.html', add_courses_to_dict({}))

def garden(request, garden):
    return render(request, 'garden.html', {'gardenName': garden})

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

def getBedCanvas(request):
    planID = request.GET['planID']
    db = DataAccess()
    canvas = db.getBedCanvas(planID)
    return HttpResponse(canvas, content_type='application/json')

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
def courseNav(request, course):
    db = DataAccess()
    color = db.getCourseColor(course)
    lessons = db.getCourseLessons(course)
    for lesson in lessons:
        link = DataAccess().getLesson(course, lesson['name'])
        lesson['link'] = link.replace(".", "", 1)
        
    completed_courses = db.getCompletedCoursesForUser(request.user.username)
    passed = False 
    if course in completed_courses:
        passed = True
        
    return render(request, 'courseNav.html', add_courses_to_dict({'lessons': lessons, 'course': course.replace('-', ' '), 'color': color, 'passed': passed}))
    
@login_required(login_url='/login/')
def lesson(request, course, lesson):
    db = DataAccess()
    color = db.getCourseColor(course)
    lesson_file_path = DataAccess().getLesson(course, lesson)
    
    #records url does not have the preceding '.'
    if "static" in lesson_file_path:
        lesson_file_path = lesson_file_path.replace(".", "", 1)#lesson_file_path.replace("./static/", "", 1)
    
    if "Garden Planning" in lesson:
        return redirect('/courseNav/Gardens')
    
    return render(request, 'lesson.html', add_courses_to_dict({'course': course, 'lesson': lesson, 'color': color, 'lesson_file_path': lesson_file_path}))
    
@login_required(login_url='/login/')
def quiz_wrapper(request, course):
    db = DataAccess()
    color = db.getCourseColor(course)
    lesson_file_path = "/quiz/" + course
    
    return render(request, 'lesson.html', add_courses_to_dict({'course': course, 'color': color, 'lesson_file_path': lesson_file_path}))

#Retrieves all courses and adds them to the data dictionary passed in,
# which is returned by each view
def add_courses_to_dict(dict, is_authenticated=True):
    if is_authenticated is True:
        db = DataAccess()
        courses = db.getCourses()
        #dict['courses'] = courses
        
        colors = []
        for course in courses:
            colors.append(db.getCourseColor(course['Course_Name']))
        #dict['colors'] = colors
        dict['courses'] = zip(courses, colors)
    return dict;
    
#Sets color and name for home page & login/logout views
def get_home_page_dict():
    return {'course': 'Prison Garden Production', 'color': '01af01'}
    

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
