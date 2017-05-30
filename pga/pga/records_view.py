# python imports:
import datetime

# Django imports:
from django.shortcuts import render, redirect, render_to_response
from django.contrib.auth.decorators import login_required

# PGA imports:
from pga.dataAccess import DataAccess
from . import view_utils
from pga.forms import RecordTableFormWithQuantity, RecordTableFormWithNotes


@login_required(login_url='/login/')
def records_nav(request):
    course = 'Record Keeping'
    color = DataAccess().getCourseColor('Records')

    return render(request, 'recordsNav.html',
                view_utils.add_courses_to_dict({'course': course, 'color': color}))


@login_required(login_url='/login/')
def harvest_records(request):

    db = DataAccess()
    view_dict = get_default_records_dict()

    if request.method == 'POST':
        form = RecordTableFormWithQuantity(request.POST)
        if form.is_valid() and request.user.is_authenticated():
            crop = form.cleaned_data['crop']
            subtype = 'NA' # form.cleaned_data['subtypes']
            location = form.cleaned_data['location']
            quantity = form.cleaned_data['quantity']
            units = form.cleaned_data['units']
            username = request.user.get_username()
            date = datetime.datetime.today().strftime("%Y-%m-%d")
            db.insert_harvest_record(username, date, crop, subtype, location, quantity, units)
            view_dict['success'] = 'Record inserted successfully!'
        else:
            view_dict['error'] = form.errors

    view_dict['course'] = 'Harvest Records'
    view_dict['records'] = db.get_harvest_records()
    view_dict['has_notes'] = False
    view_dict['form'] = RecordTableFormWithQuantity()

    return render(request, 'recordsTable.html', view_utils.add_courses_to_dict(view_dict))


@login_required(login_url='/login/')
def planting_records(request):

    db = DataAccess()
    view_dict = get_default_records_dict()

    if request.method == 'POST':
        form = RecordTableFormWithQuantity(request.POST)
        if form.is_valid() and request.user.is_authenticated():
            crop = form.cleaned_data['crop']
            crop_subtype = 'NA' # form.cleaned_data['subtypes']
            location = form.cleaned_data['location']
            quantity = form.cleaned_data['quantity']
            units = form.cleaned_data['units']
            username = request.user.get_username()
            date = datetime.datetime.today().strftime("%Y-%m-%d")
            db.insert_planting_record(username, date, crop, crop_subtype, location, quantity, units)
            view_dict['success'] = 'Record inserted successfully!'
        else:
            view_dict['error'] = form.errors

    view_dict['course'] = 'Planting Records'
    view_dict['records'] = db.get_planting_records()
    view_dict['has_notes'] = False
    view_dict['form'] = RecordTableFormWithQuantity()

    return render(request, 'recordsTable.html', view_utils.add_courses_to_dict(view_dict))


@login_required(login_url='/login/')
def garden_notes(request):

    db = DataAccess()
    view_dict = get_default_records_dict()

    if request.method == 'POST':
        form = RecordTableFormWithNotes(request.POST)
        if form.is_valid() and request.user.is_authenticated():
            crop = form.cleaned_data['crop']
            location = form.cleaned_data['location']
            notes = form.cleaned_data['notes']
            username = request.user.get_username()
            date = datetime.datetime.today().strftime("%Y-%m-%d")
            db.insert_garden_note(username, date, crop, location, notes)
            view_dict['success'] = 'Record inserted successfully!'
        else:
            view_dict['error'] = form.errors

    view_dict['course'] = 'Garden Notes'
    view_dict['records'] = db.get_garden_notes()
    view_dict['has_notes'] = True
    view_dict['form'] = RecordTableFormWithNotes()

    return render(request, 'recordsTable.html', view_utils.add_courses_to_dict(view_dict))


def get_default_records_dict():
    db = DataAccess()
    color = db.getCourseColor('Records')
    current_crops = db.get_current_crops()
    gardens = db.get_gardens()
    today = datetime.datetime.today().strftime("%m/%d/%Y")

    return {'today': today, 'color': color, 'current_crops': current_crops, 'gardens': gardens,}


# @login_required(login_url='/login/')
# def createRecordTable_Form(request):
#     if request.method == 'POST':
#         form = RecordTableForm(request.POST)
#         if form.is_valid():
#             if request.user.is_authenticated():
#                 plant = form.cleaned_data['plant']
#                 quantity = form.cleaned_data['quantity']
#                 location = form.cleaned_data['location']
#                 notes = form.cleaned_data['notes']
#                 year = form.cleaned_data['year']
#                 month = form.cleaned_data['month']
#                 day = form.cleaned_data['day']
#                 username = request.user.get_username()
#                 time = year + '/' + month + '/' + day
#                 db = DataAccess()
#                 db.addDailyLog(user=username, plant=plant, location=location, quantity=quantity, date=time, notes=notes)
#                 db.__del__()
#                 return redirect('table_home')
#     else:
#         form = RecordTableForm()
#     return render(request, 'recordstable_form.html', view_utils.add_courses_to_dict({'form': form}))
    
    
# @login_required(login_url='/login/')
# def recordTable_Home(request):
#     db = DataAccess()
#     #logs = db.getDailyLogs()
#
#     # TODO set up these tables
#     # Make sure years are returned in descending order
#
#     harvest_logs = [
#                         {'year': 2017,
#                           'records':
#                             [
#                               {'username': 'jstimes', 'logdate': '05/12/2017', 'plant': 'corn', 'location': 'Athena', 'quantity': 100},
#                               {'username': 'jstimes', 'logdate': '05/11/2017', 'plant': 'tomatoes', 'location': 'Athena', 'quantity': 10},
#                               {'username': 'jstimes', 'logdate': '05/10/2017', 'plant': 'soybeans', 'location': 'Athena', 'quantity': 1000}
#                             ]
#                         },
#                         {'year': 2016,
#                             'records':
#                             [
#                               {'username': 'jstimes', 'logdate': '05/12/2016', 'plant': 'corn', 'location': 'Athena', 'quantity': 100},
#                               {'username': 'jstimes', 'logdate': '05/11/2016', 'plant': 'tomatoes', 'location': 'Athena', 'quantity': 10},
#                               {'username': 'jstimes', 'logdate': '05/10/2016', 'plant': 'soybeans', 'location': 'Athena', 'quantity': 1000}
#                             ]
#                         }
#                     ]
#
#     notes_logs = [
#                         {'year': 2017,
#                         'records':
#                             [
#                               {'username': 'jstimes', 'logdate': '05/12/2017', 'notes': 'Planted 2 bags of tomato seeds in Athena'},
#                               {'username': 'jstimes', 'logdate': '05/11/2017', 'notes': 'Plants are being eaten by rabbits'},
#                               {'username': 'jstimes', 'logdate': '05/10/2017', 'notes': 'Athena has great soil for carrots'}
#                             ]
#                         },
#                         {'year': 2016,
#                         'records':
#                             [
#                               {'username': 'jstimes', 'logdate': '05/12/2016', 'notes': 'Almost time to harvest Athena'},
#                               {'username': 'jstimes', 'logdate': '05/11/2016', 'notes': 'I can\' remember any garden names besides Athena'},
#                               {'username': 'jstimes', 'logdate': '05/10/2016', 'notes': 'Another old note'}
#                             ]
#                         }
#                     ]
#
#     current_crops = db.get_current_crops()
#     gardens = db.get_gardens()
#     today = datetime.datetime.today().strftime("%m/%d/%Y");
#
#     dict = {'harvest_logs' : harvest_logs, 'notes_logs': notes_logs, 'current_crops': current_crops, 'gardens': gardens, 'today': today}
#
#     return render(request, 'recordstable_home.html', view_utils.add_courses_to_dict(dict))