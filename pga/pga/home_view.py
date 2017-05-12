#python imports:
import datetime

#Django imports:
from django.shortcuts import render, redirect, render_to_response

#PGA imports:
from pga.dataAccess import DataAccess
from . import view_utils

def home_page(request):
    authenticated = request.user.is_authenticated()
    
    if authenticated:
    
        # Get list of completed/non-completed courses to display
        # db = DataAccess()
        # units = db.getAllUnits()
        # completed_units = db.getCompletedCoursesForUser(request.user.get_username())
        # units_quiz_completed = [False] * len(units)
        # units_has_quiz = [False] * len(units)
        # for index, unit in enumerate(units):
            # if unit in completed_units:
                # units_quiz_completed[index] = True
            # has_quiz = db.doesCourseHaveQuiz(unit)
            # if has_quiz > 0:
                # units_has_quiz[index] = True
                
        # units_zipped = zip(units, units_quiz_completed, units_has_quiz)
        # dict = get_home_page_dict()
        # dict.update({'units': units_zipped})
        # dict = add_courses_to_dict(dict)
        
        db = DataAccess()
        dict = view_utils.get_home_page_dict()
        # TODO Get crops, #harvested, and #planted from DB
        # list of tuples (crop_name, planted_int, harvested_int)
        crops = [{'crop': 'corn', 'planted': 22, 'harvested': 10}, 
                {'crop': 'soybeans', 'planted': 122, 'harvested': 110},
                {'crop': 'eggplant', 'planted': 99, 'harvested': 75},
                {'crop': 'bananas', 'planted': 357, 'harvested': 150},
                {'crop': 'tomatoes', 'planted': 2012, 'harvested': 20}]
                
        # TODO Get schedule items from DB:
        schedule = [
                     ('Monday', [{'task': 'Water if necessary', 'complete': True, 'id': 1}]),
                     ('Tuesday', [{'task': 'Harvest the vegetables the kitchen wantes', 'complete': True, 'id': 2},
                                {'task': 'Keep them in the shade', 'complete': True, 'id': 3},
                                {'task': '2pm: Wash vegetables (ask CO to open sally port)', 'complete': False, 'id': 4},
                                {'task': '2:30pm: Give harvest to kitchen and ask for a copy of the yields', 'complete': False, 'id': 5}]),
                     ('Wednesday', [{'task': 'Harvest and wash produce for food pantry', 'complete': False, 'id': 6}, 
                                            {'task': 'ISU will pick them up at 10:45am', 'complete': False, 'id': 7}, 
                                            {'task': 'Communicate any issues or challenges to ISU', 'complete': False, 'id': 8},
                                            {'task': 'Record keeper takes Garden Manager\'s role', 'complete': False, 'id': 9},
                                            {'task': 'Tool Queen becomes the record keeper', 'complete': False, 'id': 10},
                                            {'task': 'New Record Keeper appoints new Tool Queen', 'complete': False, 'id': 11},
                                            {'task': 'New Garden Manager and new Record Keeper establish a list of tasks to accomplish during the week, ' +
                                                'and assign people to different tasks as necessary', 'complete': False, 'id': 12},
                                            {'task': 'Garden Manager tells Tim what the anticipated schedule is for watering or any other things where he might be needed', 'complete': False, 'id': 13}]),
                     ('Thursday', [{'task': 'Garden Manager and Record Keeper make a list of vegetables that will be ready to harvest the following Tuesday', 'complete': False, 'id': 14},
                                    {'task': 'Give that list to the kitchen, who has until Monday to decide what vegetables they want', 'complete': False, 'id': 15}]),
                     ('Friday', [{'task': 'Water if necessary', 'complete': False, 'id': 16}])
                    ]
                    
        day_of_week = datetime.datetime.today().weekday()
                
        dict.update({'crops': crops})
        dict.update({'schedule': schedule})
        dict.update({'current_day': 2})
        dict = view_utils.add_courses_to_dict(dict)
        
        return render(request, 'home.html', dict)
    else:
        return render(request, 'home.html', view_utils.get_home_page_dict())