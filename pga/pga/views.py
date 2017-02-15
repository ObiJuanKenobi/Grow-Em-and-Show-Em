from django.shortcuts import render, redirect
from django.contrib.auth import authenticate
from django.template import *

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
	return render(request, 'postHarvest.html');
	
def records(request):
	return render(request, 'records.html');
	
def communication(request):
	return render(request, 'communication.html');
	
	
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
	
	
	
def pestsQuiz(request):
	return render(request, 'quiz.html')
	
def quizResults(request):
	return render(request, 'quizResults.html')

def gardenImage(request):
	return render(request, 'gardenImage.html')
