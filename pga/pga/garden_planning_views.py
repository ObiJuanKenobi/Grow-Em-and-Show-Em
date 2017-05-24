# python imports:
import json
import datetime

# Django imports:
from django.shortcuts import render, redirect, render_to_response
from django.http import HttpResponse, Http404
from django.contrib.auth.decorators import login_required

# PGA imports:
from pga.dataAccess import DataAccess
from . import view_utils


# TODO - store this in DB?
gardens_color = '00AA00'


@login_required(login_url='/login/')
def garden(request, garden):
    return render(request, 'garden.html', view_utils.add_courses_to_dict({'gardenName': garden,
        'course': garden, 'color': gardens_color}))


@login_required(login_url='/login/')
def savePlan(request):
    if request.is_ajax() and request.method == "POST":
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
    if request.method == "POST":
        planID = request.POST.get('planID')
        db = DataAccess()
        db.deleteBedPlan(planID)
        response = {
            'status': 200,
            'message': 'Successfully removed the selected plan'
        }
    else:
        response = {
            'status': 404,
            'message': 'Invalid request'
        }
    return HttpResponse(json.dumps(response), content_type='application/json')



# This view should show a map of all prison gardens
# and list all gardens on the side
@login_required(login_url='/login/')
def gardensNav(request):
    course = 'Garden Planning'
    db = DataAccess()
    gardens = db.get_gardens()
    # gardens = [{'name': 'Athena'}, {'name': 'Venus'}, {'name': 'Other Garden'}, {'name': 'Other Garden2'}, {'name': 'Other Garden3'}]
        
    return render(request, 'gardensNav.html', view_utils.add_courses_to_dict({'gardens': gardens, 'course': course, 'color': gardens_color}))


# This view should the various options for a specific garden
@login_required(login_url='/login/')
def gardenNav(request, garden):
    course = garden
        
    return render(request, 'gardenNav.html', view_utils.add_courses_to_dict({'course': course, 'color': gardens_color}))
