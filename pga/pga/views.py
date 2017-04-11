from django.core.serializers import json
from django.http import HttpResponse, Http404
from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login
from django.views.generic.edit import CreateView, UpdateView
from django.template import loader
from django.template import *
from django.contrib.auth.decorators import login_required
from django.contrib.admin.views.decorators import staff_member_required
from pga.dataAccess import DataAccess
from django.views.generic import View
from .forms import UserForm
import json


def login_view(request):
    username = request.POST.get('username')
    password = request.POST.get('password')
    user = authenticate(username=username, password=password)
    if user is not None:
        login(request, user)
        return redirect('home')
    else:
        return render(request, 'login.html', {})


@login_required(login_url='login/')
def glossary(request):
    return render(request, 'glossary.html')


@login_required(login_url='login/')
def plan(request):
    return render(request, 'plan.html')


@login_required(login_url='login/')
def maintain(request):
    return render(request, 'maintain.html')


@login_required(login_url='login/')
def harvest(request):
    return render(request, 'harvest.html')


@login_required(login_url='login/')
def postHarvest(request):
    return render(request, 'postHarvest.html')


@login_required(login_url='login/')
def records(request):
    return render(request, 'records.html')


@login_required(login_url='login/')
def communication(request):
    return render(request, 'communication.html')


# Maintenance lessons:
@login_required(login_url='login/')
def pests(request):
    return render(request, 'pests.html')


@login_required(login_url='login/')
def fertilizer(request):
    return render(request, 'fertilizer.html')


@login_required(login_url='login/')
def produce(request):
    return render(request, 'produce.html')


@login_required(login_url='login/')
def maturityTimeline(request):
    return render(request, 'maturityTimeline.html')


@login_required(login_url='login/')
def watering(request):
    return render(request, 'watering.html')


@login_required(login_url='login/')
def weedRecognition(request):
    return render(request, 'weedRecognition.html')


@login_required(login_url='login/')
def disease(request):
    return render(request, 'disease.html')


@login_required(login_url='login/')
def quiz(request, course):
    db = DataAccess();
    questions = db.getQuizQuestions(course);
    return render(request, 'quiz.html', {'questions': questions, 'course': course});


@login_required(login_url='login/')
def pestsQuiz(request):
    return render(request, 'quiz.html')


def quizResults(request, course):
    db = DataAccess()
    db.addQuizAttempt(course, 'todo-get username', 1)
    return render(request, 'quizResults.html', {'course': course})

def garden(request):
	return render(request, 'garden.html')


def saveImage(request):
    if request.is_ajax() and request.POST:
        bedName = request.POST.get('bedName')
        canvasData = request.POST.get('canvasData')
        db = DataAccess()
        db.saveBedPlan(bedName, canvasData)
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

def loadImage(request):
    bedName = request.GET['bedName']
    db = DataAccess()
    plan = db.getBedPlan(bedName)
    return HttpResponse(plan,content_type='application/json')

@staff_member_required
def adminHome(request):
    return render(request, 'admin/home.html');


@staff_member_required
def adminCourseInfo(request):
    return render(request, 'admin/course_info.html');


@staff_member_required
def adminCourseMgmt(request):
    courses = DataAccess().getCourses()
    return render(request, 'admin/course_mgmt.html', {'courses': courses});


@staff_member_required
def adminUserProgress(request):
    return render(request, 'admin/user_progress.html');


@staff_member_required
def adminQuizStatistics(request):
    return render(request, 'admin/quiz_statistics.html');


@staff_member_required
def adminSupplementaryMaterials(request):
    return render(request, 'admin/supplementary_materials.html');


@staff_member_required
def adminUnit(request, unit):
    lessons = DataAccess().getCourseLessons(unit)
    return render(request, 'admin/unit.html', {'lessons': lessons, 'unit': unit});


@staff_member_required
def adminLesson(request, lesson, unit):
    return render(request, 'admin/lesson.html', {'lesson': lesson, 'unit': unit});


@staff_member_required
def adminQuiz(request, unit):
    questions = DataAccess().getQuizQuestions(unit);

    return render(request, 'admin/quiz.html', {'unit': unit, 'questions': questions});


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
