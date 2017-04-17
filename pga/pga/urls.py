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

urlpatterns = [
    url(r'^$', TemplateView.as_view(template_name='home.html'), name='home'),
    url(r'^register/$', views.UserFormView.as_view(), name='register'),
    url(r'^login/$', views.login_view, name='login'),
    url(r'^logout/$', auth_views.logout, {'template_name': 'logout.html'}, name='logout'),
    url(r'^admin/', admin.site.urls),

    # the '.' character in a regex matches any char besides newline
    url(r'^pgaadmin/unit/(?P<unit>.+)/(?P<lesson>.+)', views.adminLesson),
    url(r'^pgaadmin/unit/(?P<unit>.+)', views.adminUnit),
    url(r'^pgaadmin/quiz/(?P<unit>.+)', views.adminQuiz),
    url(r'^pgaadmin/supplementaryMaterials', views.adminSupplementaryMaterials),
    url(r'^pgaadmin/quizStatistics', views.adminQuizStatistics),
    url(r'^pgaadmin/userProgress', views.adminUserProgress),
    url(r'^pgaadmin/courseMgmt', views.adminCourseMgmt),
    url(r'^pgaadmin/courseInfo', views.adminCourseInfo),
    url(r'^pgaadmin/', views.adminHome),

    url(r'^quiz/(?P<course>[A-Za-z\s]+)', views.quiz, name='quiz'),
    url(r'^quizResults/(?P<course>[A-Za-z\s]+)', views.quizResults, name='quizResults'),

    url(r'^glossary', views.glossary, name='glossary'),
    url(r'^plan', views.plan, name='plan'),
    url(r'^maintain', views.maintain, name='maintain'),
    url(r'^pests', views.pests, name='pests'),
    # url(r'^pestQuiz', views.pestsQuiz, name='pestsQuiz'),
    # url(r'^quizResults', views.quizResults, name='quizResults'),
    url(r'^fertilizer', views.fertilizer, name='fertilizer'),
    url(r'^produce', views.produce, name='produce'),
    url(r'^maturityTimeline', views.maturityTimeline, name='maturityTimeline'),
    url(r'^watering', views.watering, name='watering'),
    url(r'^weedRecognition', views.weedRecognition, name='weedRecognition'),
    url(r'^disease', views.disease, name='disease'),

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
