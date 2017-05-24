# python imports:
import datetime
import json

# Django imports:
from django.shortcuts import render, redirect, render_to_response
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse, Http404

# PGA imports:
from pga.dataAccess import DataAccess
from . import view_utils


@login_required(login_url='/login/')
def create_schedule(request):
    if request.is_ajax() and request.method == "POST":
        # Uploaded new schedule:
        username = request.user.username
        
        # Extract tasks for days from JSON request data:
        day_tasks_dict = {}
        for day, tasks_str in request.POST.items():
            tasks_dict = json.loads(tasks_str)
            tasks_list = []
            for task_idx, task in tasks_dict.items():
                tasks_list.append(task)
            day_tasks_dict[day] = tasks_list
            
        DataAccess().create_schedule(username, day_tasks_dict)
        
        response = {
            'success': True,
            'status': 200,
            'message': 'Successfully saved changes on canvas'
        }
        return HttpResponse(json.dumps(response), content_type='application/json')
        
    else:
        # Just loading the create new schedule page:
        dict = view_utils.get_home_page_dict()
        dict.update({'days': ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday']})
        return render(request, 'create_schedule.html', view_utils.add_courses_to_dict(dict))


# Called when user presses 'Complete' on a task on the home page
@login_required(login_url='/login/')
def mark_task_complete(request, task):
    username = request.user.username
    DataAccess().mark_task_complete(task, username)
    return redirect('home')