"""pga URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.10/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.conf.urls import url, include
    2. Add a URL to urlpatterns:  url(r'^blog/', include('blog.urls'))
"""
from django.conf.urls import url
from django.contrib import admin
from django.contrib.auth import views as auth_views
from django.contrib.staticfiles.urls import staticfiles_urlpatterns
from django.views.generic.base import TemplateView

from . import views
from . import home_view
from . import records_view
from . import schedule_views
from . import garden_planning_views
from . import view_utils
from pga.admin_views import *
from . import user_quiz_views
from . import admin_quiz_mgmt
from . import admin_records_views

urlpatterns = [

    # Home page, schedule, & authentication-related urls:
    url(r'^$', home_view.home_page, name='home'),
    url(r'^register/$', views.UserFormView.as_view(), name='register'),
    url(r'^login/$', views.login_view, name='login'),
    url(r'^logout/$', auth_views.logout, {'template_name': 'logout.html', 'extra_context': view_utils.get_home_page_dict() }, name='logout', ),
    
    # Schedule related urls:
    url(r'^createNewSchedule', schedule_views.create_schedule, name='schedule'),
    url(r'^markTaskComplete/(?P<task>[A-Za-z0-9\-\s]+)', schedule_views.mark_task_complete, name='completeTask'),
    

    # Admin urls:
    url(r'^admin/', admin.site.urls),
    url(r'^pgaadmin/unit/(?P<unit>[A-Za-z0-9\-\s]+)/supplementaryMaterials', AdminSuppMatView.as_view()),
    url(r'^pgaadmin/unit/(?P<unit>[A-Za-z0-9\-\s]+)/(?P<lesson>[A-Za-z0-9\-\s]+)', AdminLessonView.as_view()),
    url(r'^pgaadmin/unit/(?P<unit>[A-Za-z0-9\-\s]+)', AdminUnitView.as_view()),

    url(r'^pgaadmin/deleteLesson/(?P<lesson>[A-Za-z0-9\-\s]+)', delete_lesson),
    url(r'^pgaadmin/deleteUnit/(?P<unit>[A-Za-z0-9\-\s]+)', delete_unit),

    url(r'^pgaadmin/quiz/editQuestion', admin_quiz_mgmt.edit_quiz_question),
    url(r'^pgaadmin/quiz/deleteQuestion', admin_quiz_mgmt.delete_quiz_question),
    url(r'^pgaadmin/quiz/addQuestion', admin_quiz_mgmt.add_quiz_question),
    url(r'^pgaadmin/quiz/editAnswer', admin_quiz_mgmt.edit_quiz_answer),
    url(r'^pgaadmin/quiz/(?P<unit>[A-Za-z0-9\-\s]+)', AdminQuizView.as_view()),

    url(r'^pgaadmin/quizStatistics/(?P<unit>[A-Za-z0-9\-\s]+)', adminQuizStatistics),
    url(r'^pgaadmin/quizStatistics', adminQuizStatisticsOverview),

    url(r'^pgaadmin/courseMgmt', CourseMgmtView.as_view()),
    url(r'^pgaadmin/changeColor/(?P<course>[A-Za-z0-9\-\s]+)/(?P<color>[A-Za-z0-9\-\s]+)', adminSetCourseColor),

    url(r'^pgaadmin/userProgress/(?P<user>[A-Za-z0-9\-\s]+)', adminUserProgress),
    url(r'^pgaadmin/userProgress', adminUserProgressOverview),

    url(r'^pgaadmin/cropMgmt', admin_crop_mgmt),
    url(r'^pgaadmin/addCrop/(?P<new_crop>[A-Za-z0-9\-\s]+)', admin_add_crop),
    url(r'^pgaadmin/toggleCrop/(?P<crop>[A-Za-z0-9\-\s]+)/(?P<is_current>[A-Za-z0-9\-\s]+)', admin_toggle_current_crop),

    url(r'^pgaadmin/gardenMgmtMenu', garden_mgmt_menu),

    url(r'^pgaadmin/recordsMgmt', records_mgmt_menu),
    url(r'^pgaadmin/plantingRecords', admin_records_views.admin_planting_records),
    url(r'^pgaadmin/deletePlantingRecord/(?P<record_id>[A-Za-z0-9\-\s]+)', admin_records_views.delete_planting_record),
    url(r'^pgaadmin/harvestRecords', admin_records_views.admin_harvest_records),
    url(r'^pgaadmin/deleteHarvestRecord/(?P<record_id>[A-Za-z0-9\-\s]+)', admin_records_views.delete_harvest_record),
    url(r'^pgaadmin/gardenNotes', admin_records_views.admin_garden_notes),
    url(r'^pgaadmin/deleteGardenNote/(?P<record_id>[A-Za-z0-9\-\s]+)', admin_records_views.delete_garden_note),

    url(r'^pgaadmin/courseInfo', admin_course_info),
    url(r'^pgaadmin/', admin_home),

    # User-quiz urls:
    # url(r'^takeQuiz/(?P<course>[A-Za-z0-9\-\s]+)', views.quiz_wrapper),
    url(r'^quiz/(?P<course>[A-Za-z0-9\-\s]+)', user_quiz_views.quiz, name='quiz'),
    url(r'^gradeQuiz/(?P<course>[A-Za-z0-9\-\s]+)', user_quiz_views.grade_quiz, name='quiz'),
    url(r'^quizResults/(?P<course>[A-Za-z0-9\-\s]+)', user_quiz_views.quiz_results, name='quizResults'),
    
    # General course urls:
    url(r'^lesson/(?P<course>[A-Za-z0-9\-\s]+)/(?P<lesson>[A-Za-z0-9\-\s\_]+)/', views.lesson, name='courseNav'),
    url(r'^courseNav/(?P<course>[A-Za-z0-9\-\s]+)/', views.courseNav, name='courseNav'),

    # Demo url - remove
    url(r'^pests', views.pests, name='pests'),

    # Record keeping urls:
    url(r'^recordsNav/', records_view.records_nav, name='recordsNav'),
    url(r'^plantingRecords/', records_view.planting_records, name='recordsNav'),
    url(r'^harvestRecords/', records_view.harvest_records, name='recordsNav'),
    url(r'^gardenNotes/', records_view.garden_notes, name='recordsNav'),

    #url(r'^table_form/$', records_view.createRecordTable_Form, name='table_form'),
    #url(r'^table_home/$', records_view.recordTable_Home, name='table_home'),
    
    # Garden planning urls:
    url(r'^gardensNav/', garden_planning_views.gardensNav, name='gardensNav'),
    url(r'^gardenNav/(?P<garden>[A-Za-z0-9\-\s]+)', garden_planning_views.gardenNav, name='gardenNav'),
    url(r'^garden/(?P<garden>[A-Za-z0-9\-\s]+)', garden_planning_views.garden, name='garden'),
    url(r'^savePlan/$', garden_planning_views.savePlan, name='savePlan'),
    url(r'^showPlans/$', garden_planning_views.showPlans, name='showPlans'),
    url(r'^deletePlan/$', garden_planning_views.deletePlan, name='deletePlan'),
    url(r'^getBedCanvas/$', garden_planning_views.getBedCanvas, name='getBedCanvas')
]

urlpatterns += staticfiles_urlpatterns()
