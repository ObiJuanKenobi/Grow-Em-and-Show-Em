from django.http import HttpResponse
from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login
from django.views.generic.edit import CreateView, UpdateView
from django.template import loader
from django.template import *
from models import GardenImages
from django.views.generic import View
from .forms import UserForm
from dataAccess import DataAccess

def login_view(request):
     return render(request, 'login.html', {})
#    username = request.POST['username']
#    password = request.POST['password']
#    user = authenticate(username=username, password=password)
#    if user is not None:
#        return redirect('home')
#    else:
#        return render(request, 'login.html', {})

def glossary(request):
	return render(request, 'glossary.html')

def plan(request):
	return render(request, 'plan.html')

def maintain(request):
	return render(request, 'maintain.html')
	
def harvest(request):
	return render(request, 'harvest.html')

def postHarvest(request):
	return render(request, 'postHarvest.html')

def records(request):
	return render(request, 'records.html')

def communication(request):
	return render(request, 'communication.html')

#Maintenance lessons:
def pests(request):
	return render(request, 'pests.html')
	
def fertilizer(request):
	return render(request, 'fertilizer.html')
	
def produce(request):
	return render(request, 'produce.html')
	
def maturityTimeline(request):
	return render(request, 'maturityTimeline.html')
	
def watering(request):
	return render(request, 'watering.html')
	
def weedRecognition(request):
	return render(request, 'weedRecognition.html')
	
def disease(request):
	return render(request, 'disease.html')
	
def quiz(request, course):
	db = DataAccess();
	questions = db.getQuizQuestions(course);
	return render(request, 'quiz.html', { 'questions': questions, 'course': course } );
	
def pestsQuiz(request):
	return render(request, 'quiz.html')
	
def quizResults(request, course):
	db = DataAccess()
	db.addQuizAttempt(course, 'todo-get username', 1)
	return render(request, 'quizResults.html', {'course': course})

def gardenImage(request):
	return render(request, 'gardenImage.html')

def saveImage(request):
	fileName = request.GET['fileName']
	imageData = request.GET['imageData']
	image = GardenImages.objects.create(
		name=fileName,
		imageData=imageData
	)
	image.save()
	return HttpResponse("Success")

class UserFormView(View):
    form_class = UserForm
    template_name = 'registration_form.html'

    def get(self, request):
        form = self.form_class(None)
        return render(request, self.template_name, {'form':form})
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
            user = authenticate(username = username, password = password)

            if user is not None:
                if user.is_active:
                    login(request,user)
                    return redirect('home')

        return render(request, self.template_name, {'form': form})