#python imports:
import datetime

#Django imports:
from django.shortcuts import render, redirect, render_to_response
from django.contrib.auth.decorators import login_required

#PGA imports:
from pga.dataAccess import DataAccess
from . import view_utils

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
    return render(request, 'recordstable_form.html', view_utils.add_courses_to_dict({'form': form}))
    
    
@login_required(login_url='/login/')
def recordTable_Home(request):
    db = DataAccess()
    #logs = db.getDailyLogs()
    
    #TODO set up these tables
    # Make sure years are returned in descending order
    
    harvest_logs = [
                        {'year': 2017, 
                          'records':
                            [
                              {'username': 'jstimes', 'logdate': '05/12/2017', 'plant': 'corn', 'location': 'Athena', 'quantity': 100},
                              {'username': 'jstimes', 'logdate': '05/11/2017', 'plant': 'tomatoes', 'location': 'Athena', 'quantity': 10},
                              {'username': 'jstimes', 'logdate': '05/10/2017', 'plant': 'soybeans', 'location': 'Athena', 'quantity': 1000}
                            ]
                        },
                        {'year': 2016, 
                            'records':
                            [
                              {'username': 'jstimes', 'logdate': '05/12/2016', 'plant': 'corn', 'location': 'Athena', 'quantity': 100},
                              {'username': 'jstimes', 'logdate': '05/11/2016', 'plant': 'tomatoes', 'location': 'Athena', 'quantity': 10},
                              {'username': 'jstimes', 'logdate': '05/10/2016', 'plant': 'soybeans', 'location': 'Athena', 'quantity': 1000}
                            ]
                        }
                    ]
                    
    notes_logs = [
                        {'year': 2017, 
                        'records':
                            [
                              {'username': 'jstimes', 'logdate': '05/12/2017', 'notes': 'Planted 2 bags of tomato seeds in Athena'},
                              {'username': 'jstimes', 'logdate': '05/11/2017', 'notes': 'Plants are being eaten by rabbits'},
                              {'username': 'jstimes', 'logdate': '05/10/2017', 'notes': 'Athena has great soil for carrots'}
                            ]
                        },
                        {'year': 2016, 
                        'records':
                            [
                              {'username': 'jstimes', 'logdate': '05/12/2016', 'notes': 'Almost time to harvest Athena'},
                              {'username': 'jstimes', 'logdate': '05/11/2016', 'notes': 'I can\' remember any garden names besides Athena'},
                              {'username': 'jstimes', 'logdate': '05/10/2016', 'notes': 'Another old note'}
                            ]
                        }
                    ]
                    
    #TODO add current crops table 
    current_crops = ['corn', 'tomatoes', 'soybeans', 'carrots', 'eggplant']
    gardens = ['Athena', 'Garden 2', 'Garden 3']
    today = datetime.datetime.today().strftime("%m/%d/%Y");
    
    dict = {'harvest_logs' : harvest_logs, 'notes_logs': notes_logs, 'current_crops': current_crops, 'gardens': gardens, 'today': today}

    return render(request, 'recordstable_home.html', view_utils.add_courses_to_dict(dict))