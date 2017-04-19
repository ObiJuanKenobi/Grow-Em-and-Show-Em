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
    return render(request, 'home.html', add_courses_to_dict({}))


def login_view(request):
    username = request.POST.get('username')
    password = request.POST.get('password')
    user = authenticate(username=username, password=password)
    if user is not None:
        login(request, user)
        return redirect('home')
    else:
        return render(request, 'login.html', add_courses_to_dict({}))


def createRecordTable_Form(request):
    if request.method == 'POST':
        form = RecordTableForm(request.POST)
        if form.is_valid():
            plant = form.cleaned_data['plant']
            quantity = form.cleaned_data['quantity']
            location = form.cleaned_data['location']
            notes = form.cleaned_data['notes']
            year = form.cleaned_data['year']
            month = form.cleaned_data['month']
            day = form.cleaned_data['day']
            redirect('table_home')
    else:
        form = RecordTableForm()
    return render(request, 'recordstable_form.html', add_courses_to_dict({'form': form}))

def recordTable_Home(request):
    return render(request, 'recordstable_home.html')

@login_required(login_url='/login/')
def glossary(request):
    return render(request, 'glossary.html', add_courses_to_dict({}))


@login_required(login_url='/login/')
def plan(request):
    return render(request, 'plan.html')


@login_required(login_url='/login/')
def maintain(request):
    return render(request, 'maintain.html')


@login_required(login_url='/login/')
def harvest(request):
    return render(request, 'harvest.html')


@login_required(login_url='/login/')
def postHarvest(request):
    return render(request, 'postHarvest.html')


@login_required(login_url='/login/')
def records(request):
    return render(request, 'records.html')


@login_required(login_url='/login/')
def communication(request):
    return render(request, 'communication.html')


# Maintenance lessons:
@login_required(login_url='/login/')
def pests(request):
    return render(request, 'pests.html', add_courses_to_dict({}))


@login_required(login_url='/login/')
def fertilizer(request):
    return render(request, 'fertilizer.html')


@login_required(login_url='/login/')
def produce(request):
    return render(request, 'produce.html')


@login_required(login_url='/login/')
def maturityTimeline(request):
    return render(request, 'maturityTimeline.html')


@login_required(login_url='/login/')
def watering(request):
    return render(request, 'watering.html')


@login_required(login_url='/login/')
def weedRecognition(request):
    return render(request, 'weedRecognition.html')


@login_required(login_url='/login/')
def disease(request):
    return render(request, 'disease.html')


@login_required(login_url='/login/')
def quiz(request, course):
    db = DataAccess();
    questions = db.getQuizQuestions(course);
    return render(request, 'quiz.html', add_courses_to_dict({'questions': questions, 'course': course}));


@login_required(login_url='/login/')
def pestsQuiz(request):
    return render(request, 'quiz.html')


def quizResults(request, course):
    db = DataAccess()
    db.addQuizAttempt(course, 'todo-get username', 1)
    return render(request, 'quizResults.html', add_courses_to_dict({'course': course}))


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
        
    return render(request, 'courseNav.html', add_courses_to_dict({'lessons': lessons, 'course': course.replace('-', ' '), 'color': color}))
    
def lesson(request, course, lesson):
    db = DataAccess()
    color = db.getCourseColor(course)
    lesson_file_path = DataAccess().getLesson(course, lesson)
    lesson_file_path = lesson_file_path.replace(".", "", 1)#lesson_file_path.replace("./static/", "", 1)
    return render(request, 'lesson.html', add_courses_to_dict({'course': course, 'lesson': lesson, 'color': color, 'lesson_file_path': lesson_file_path}))

#Retrieves all courses and adds them to the data dictionary passed in,
# which is returned by each view
def add_courses_to_dict(dict):
    courses = DataAccess().getCourses();
    dict['courses'] = courses;
    return dict;
    

class UserFormView(View):
    form_class = UserForm
    template_name = 'registration_form.html'

    def get(self, request):
        form = self.form_class(None)
        return render(request, self.template_name, {'form': form})

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
            user = authenticate(username=username, password=password)

            if user is not None:
                if user.is_active:
                    login(request, user)
                    return redirect('home')

        return render(request, self.template_name, {'form': form})
