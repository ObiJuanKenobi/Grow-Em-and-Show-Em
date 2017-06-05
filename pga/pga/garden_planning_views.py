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
grid_size = 50


def get_garden_dimensions(garden_name):
    garden_details = DataAccess().get_gardens_and_details()
    for garden_dict in garden_details:
        if garden_dict['name'] == garden_name:
            return {'height':  garden_dict['height'] * grid_size,
                'width': garden_dict['width'] * grid_size}
    return {'height': 20 * grid_size,
        'width': 20 * grid_size}

@login_required(login_url='/login/')
def garden(request, garden_name):

    db = DataAccess()
    current_crops = db.get_current_crops()
    garden_details = get_garden_dimensions(garden_name)

    garden_dict = {'gardenName': garden_name,
                   'current_crops': current_crops,
                   'height': garden_details['height'],
                   'width': garden_details['width'],
                    'course': garden_name, 'color': gardens_color}
    return render(request, 'garden.html', view_utils.add_courses_to_dict(garden_dict))


@login_required(login_url='/login/')
def current_garden(request, garden_name):
    db = DataAccess()
    # canvas = db.get_current_bed_canvas(garden_name)
    data = db.get_current_bed_plan_data(garden_name)
    garden_dimensions = get_garden_dimensions(garden_name)

    has_data = True
    if data is None:
        has_data = False

    return render(request, 'current_garden.html', view_utils.add_courses_to_dict({'gardenName': garden_name,
        'course': garden_name, 'color': gardens_color,
        'height': garden_dimensions['height'], 'width': garden_dimensions['width'],
        'data': data, 'has_data': has_data}))


@login_required(login_url='/login/')
def past_plans(request, garden_name):
    db = DataAccess()

    garden_dimensions = get_garden_dimensions(garden_name)
    past_plan_ids = db.get_past_bed_plans(garden_name)

    return render(request, 'past_gardens.html', view_utils.add_courses_to_dict({'gardenName': garden_name,
                                                                                'height': garden_dimensions['height'],
                                                                                'width': garden_dimensions['width'],
        'course': garden_name, 'color': gardens_color, 'past_plans': past_plan_ids}))


@login_required(login_url='/login/')
def save_plan(request):
    if request.is_ajax() and request.method == "POST":
        bed_name = request.POST.get('bedName')
        bed_plan = request.POST.get('bedPlan')
        bed_canvas = request.POST.get('bedCanvas')
        username = request.user.username

        db = DataAccess()
        plan_id = db.save_bed_plan(bed_name, bed_plan, bed_canvas, username)
        response = {
            'status': 200,
            'message': 'Successfully saved changes on canvas',
            'username': username,
            'plan_id': plan_id
        }
    else:
        response = {
            'status': 404,
            'message': 'Unable to save canvas as an image'
        }
    return HttpResponse(json.dumps(response), content_type='application/json')


@login_required(login_url='/login/')
def update_plan(request):
    if request.is_ajax() and request.method == "POST":
        plan_id = request.POST.get('plan_id')
        canvas_data = request.POST.get('canvas')
        username = request.user.username

        db = DataAccess()
        db.update_bed_plan(plan_id, canvas_data, username)
        response = {
            'status': 200,
            'message': 'Successfully saved changes on canvas',
            'username': username,
            'plan_id': plan_id
        }
    else:
        response = {
            'status': 404,
            'message': 'Unable to save canvas as an image'
        }
    return HttpResponse(json.dumps(response), content_type='application/json')


@login_required(login_url='/login/')
def mark_current(request):
    if request.method == "POST":
        plan_id = request.POST.get('plan_id')
        bed_name = request.POST.get('bed_name')
        DataAccess().mark_bed_plan_as_current(bed_name, plan_id, request.user.username)
        response = {
            'status': 200,
            'message': 'Successfully marked as current'
        }
    else:
        response = {
            'status': 404,
            'message': 'Invalid request'
        }
    return HttpResponse(json.dumps(response), content_type='application/json')



@login_required(login_url='/login/')
def show_plans(request):
    bed_name = request.GET['bedName']
    db = DataAccess()
    plans = db.get_bed_plans(bed_name)
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
def get_bed_canvas(request):
    plan_id = request.GET['planID']
    db = DataAccess()
    canvas = db.get_bed_canvas(plan_id)
    data = db.get_bed_plan_data(plan_id)
    return HttpResponse(json.dumps({'canvas': canvas, 'data': data}), content_type='application/json')


@login_required(login_url='/login/')
def delete_plan(request):
    if request.method == "POST":
        plan_id = request.POST.get('planID')
        username = request.user.username
        db = DataAccess()
        db.delete_bed_plan(plan_id, username)
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
def gardens_nav(request):
    course = 'Garden Planning'
    db = DataAccess()
    gardens = db.get_gardens()
    # gardens = [{'name': 'Athena'}, {'name': 'Venus'}, {'name': 'Other Garden'}, {'name': 'Other Garden2'}]
        
    return render(request, 'gardensNav.html', view_utils.add_courses_to_dict({'gardens': gardens, 'course': course, 'color': gardens_color}))


# This view should the various options for a specific garden
@login_required(login_url='/login/')
def garden_nav(request, garden_name):
    course = garden_name
        
    return render(request, 'gardenNav.html', view_utils.add_courses_to_dict({'course': course, 'color': gardens_color}))
