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
from pga.admin_views import *

urlpatterns = [
    url(r'^$', TemplateView.as_view(template_name='home.html'), name='home'),
    url(r'^register/$', views.UserFormView.as_view(), name='register'),
    url(r'^login/$', views.login_view, name='login'),
    url(r'^logout/$', auth_views.logout, {'template_name': 'logout.html'}, name='logout'),
    url(r'^admin/', admin.site.urls),

    # the '.' character in a regex matches any char besides newline
    url(r'^pgaadmin/unit/(?P<unit>.+)/(?P<lesson>.+)', AdminLessonView.as_view()),
    url(r'^pgaadmin/unit/(?P<unit>.+)', AdminUnitView.as_view()),
    url(r'^pgaadmin/quiz/(?P<unit>.+)', views.adminQuiz),
    url(r'^pgaadmin/supplementaryMaterials/(?P<resource_type>.+)', AdminSuppMatView.as_view()),
    url(r'^pgaadmin/supplementaryMaterials', adminSupplementaryMaterials),
    url(r'^pgaadmin/quizStatistics', views.adminQuizStatistics),
    url(r'^pgaadmin/userProgress', views.adminUserProgress),
    url(r'^pgaadmin/courseMgmt', CourseMgmtView.as_view()),#views.adminCourseMgmt),
    url(r'^pgaadmin/courseInfo', views.adminCourseInfo),
    url(r'^pgaadmin/', views.adminHome),

    url(r'^quiz/(?P<course>[A-Za-z\s]+)', views.quiz, name='quiz'),
    url(r'^quizResults/(?P<course>[A-Za-z\s]+)', views.quizResults, name='quizResults'),
    url(r'^courseNav/(?P<course>[a-z-]+)/(?P<color>[a-z0-9]+)/', views.courseNav, name='courseNav'),

    url(r'^glossary', views.glossary, name='glossary'),
    url(r'^pests', views.pests, name='pests'),
    # url(r'^pestQuiz', views.pestsQuiz, name='pestsQuiz'),
    # url(r'^quizResults', views.quizResults, name='quizResults'),

    #Urls for records
    url(r'^harvest', views.harvest, name='harvest'),
    url(r'^postHarvest', views.postHarvest, name='postHarvest'),
    url(r'^records', views.records, name='records'),
    url(r'^communication', views.communication, name='communication'),
    url(r'^garden', views.garden, name='garden'),
    url(r'^savePlan/$', views.savePlan, name='savePlan'),
    url(r'^showPlans/$', views.showPlans, name='showPlans'),
    url(r'^deletePlan/$', views.deletePlan, name='deletePlan'),
    url(r'^getBedCanvas/$', views.getBedCanvas, name='getBedCanvas')
]

urlpatterns += staticfiles_urlpatterns()
