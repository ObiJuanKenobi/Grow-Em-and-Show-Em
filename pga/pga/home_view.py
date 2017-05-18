# python imports:
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
                
        schedule = db.get_current_schedule()
                    
        day_of_week = datetime.datetime.today().weekday()

        # Python's weekday ints go from 0=Monday - 6=Sunday
        day_of_week = day_of_week + 1
        if day_of_week == 7:
            day_of_week = 1
                
        dict.update({'crops': crops})
        dict.update({'schedule': schedule})
        dict.update({'current_day': day_of_week})
        dict = view_utils.add_courses_to_dict(dict)
        
        return render(request, 'home.html', dict)
    else:
        return render(request, 'home.html', view_utils.get_home_page_dict())