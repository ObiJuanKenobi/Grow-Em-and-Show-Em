from django.http import HttpResponse, Http404
from django.contrib.admin.views.decorators import staff_member_required

from pga.abstract_upload_view import *
from pga.dataAccess import DataAccess
from pga.coursemanager import *
import json


# Displays all units, allowing users to delete them, upload another,
# go to a unit's lessons, or go to supplementary materials
class CourseMgmtView(AbstractFileUploadView):
    
    template_name = 'admin/course_mgmt.html'
    
    def __init__(self):
        super(CourseMgmtView, self).__init__(['.zip'], [])
    
    def get_page_specific_data(self):
        courses = DataAccess().getCourses()
        return { 'courses': courses }
        
    def page_specific_handle_file(self, file):
        status, message = processCourseZip(file)
        return FileHandlingResult(status, message)


@staff_member_required
def delete_unit(request, unit):
    if request.method == 'POST':

        db = DataAccess()
        # Need to delete all lessons, sup mats, quiz data, then unit itself

        response = {
            'status': 200,
            'message': 'Successfully deleted lesson'
        }
    else:
        response = {
            'status': 404,
            'message': 'Invalid request'
        }
    return HttpResponse(json.dumps(response), content_type='application/json')


# Displays all lessons in a given unit, allowing users to delete them, upload more,
# or go to the unit quiz
class AdminUnitView(AbstractFileUploadView):
    
    template_name = 'admin/unit.html'
    unit = None
    
    def __init__(self):
        super(AdminUnitView, self).__init__(['.zip'], [])
        
    def extract_extra_params(self, *args, **kwargs):
        self.unit = kwargs.pop('unit', None)
        if self.unit is not None:
            return True
            
        # Invalid URL:
        if self.unit is None:
            self.extra_params_errors += 'Valid unit not found'
        return False
    
    def get_page_specific_data(self):
        # Ensures 'self.unit' is set before this code is reached
        lessons = DataAccess().getCourseLessons(self.unit)
        return { 'lessons': lessons, 'unit': self.unit }
        
    def page_specific_handle_file(self, file):
        return FileHandlingResult(True, 'TODO - not implemented')


@staff_member_required
def delete_lesson(request, lesson):
    if request.method == 'POST':

        db = DataAccess()
        db.deleteLesson(lesson)

        response = {
            'status': 200,
            'message': 'Successfully deleted lesson'
        }
    else:
        response = {
            'status': 404,
            'message': 'Invalid request'
        }
    return HttpResponse(json.dumps(response), content_type='application/json')


# Renders info for a given lesson. Gives option to download lesson
# or upload a replacement
class AdminLessonView(AbstractFileUploadView):
    
    template_name = 'admin/lesson.html'
    unit = None
    lesson = None
    
    def __init__(self):
        super(AdminLessonView, self).__init__( ['.zip'], [])
            
    def extract_extra_params(self, *args, **kwargs):
        self.unit = kwargs.pop('unit', None)
        self.lesson = kwargs.pop('lesson', None)
        if self.unit is not None and self.lesson is not None:
            return True
            
        # Invalid URL:
        if self.unit is None:
            self.extra_params_errors += 'Valid unit not found'
        if self.lesson is None:
            self.extra_params_errors += 'Valid lesson not found'
        return False
    
    def get_page_specific_data(self):
        # Ensures 'self.unit' & 'self.lesson' is set before this code is reached
        return { 'lesson': self.lesson, 'unit': self.unit }
        
    def page_specific_handle_file(self, file):
        return FileHandlingResult(True, 'TODO - not implemented')
        
        
# Renders info for a given lesson. Gives option to download lesson
# or upload a replacement
class AdminSuppMatView(AbstractFileUploadView):
    
    template_name = 'admin/supplementary_materials.html'
    unit = None
    
    def __init__(self):
        super(AdminSuppMatView, self).__init__( ['.pdf',
                                                '.jpg', '.jpeg', '.png', '.tiff', '.gif', '.bmp', #image types
                                                '.mp4', '.m4p', '.m4v', '.flv', '.f4v', '.f4p', '.f4a', '.f4b', '.mpg', '.mpeg', '.avi', '.mov', '.qt', #video types
                                                '.zip'], [])
            
    def extract_extra_params(self, *args, **kwargs):
        self.unit = kwargs.pop('unit', None)
        if self.unit is not None:
            return True
           
        # Invalid URL:
        self.extra_params_errors += "couldn't find unit in url"
        return False
    
    def get_page_specific_data(self):
        # Ensures 'self.unit' is set before reaching here
        resources = getMaterialPaths(self.unit)
        resources_list = []
        for resource in resources:
            resource_path = resource.replace(".", "", 1)
            last_slash_index = resource.rfind('/')
            resource_name = resource[last_slash_index+1:]
            resource_html_id = resource_name.replace(".", "")
            resources_list.append({'path': resource_path, 'name': resource_name, 'html_id': resource_html_id})
        
        return {'unit': self.unit, 'resources': resources_list}
        
    def page_specific_handle_file(self, file):
        # type of material is given by 'self.resource_type'
        return FileHandlingResult(True, 'TODO - not implemented')


@staff_member_required
def garden_mgmt_menu(request):
    links = [{'name': 'View/Edit Current Crops', 'link': '/pgaadmin/cropMgmt'},
             {'name': 'View/Edit Gardens & Plans', 'link': '/pgaadmin/gardensMgmt'},
             {'name': 'View/Edit Records', 'link': '/pgaadmin/recordsMgmt'},
             {'name': 'View/Edit Schedules', 'link': '/pgaadmin/scheduleMgmt'}]

    back_link = '/pgaadmin'

    title = 'Garden & Records Management'

    return render(request, 'admin/menu.html', {'links': links, 'title': title, 'back_link': back_link})


@staff_member_required
def admin_schedule_mgmt(request):
    schedules_list = DataAccess().get_all_schedules()
    print "NumSchedules: " + str(len(schedules_list))
    data_dict = {'schedules': schedules_list}
    return render(request, 'admin/schedule_mgmt.html', data_dict)


@staff_member_required
def admin_delete_schedule(request):
    if request.method == 'POST':
        schedule_id = request.POST.get('schedule_id')
        DataAccess().delete_schedule(schedule_id)
        return HttpResponse(json.dumps({'status': 200, 'message': 'Success'}), content_type='application/json')

    else:
        return HttpResponse(json.dumps({'status': 404, 'message': 'POST requests only'}), content_type='application/json')


@staff_member_required
def admin_make_current_schedule(request):
    if request.method == 'POST':
        schedule_id = request.POST.get('schedule_id')
        DataAccess().make_current_schedule(schedule_id)
        return HttpResponse(json.dumps({'status': 200, 'message': 'Success'}), content_type='application/json')

    else:
        return HttpResponse(json.dumps({'status': 404, 'message': 'POST requests only'}), content_type='application/json')


class GardensMgmtView(AbstractFileUploadView):
    template_name = 'admin/gardens_mgmt.html'

    def __init__(self):
        super(GardensMgmtView, self).__init__(['.jpg'], [])

    def get_page_specific_data(self):
        gardens = DataAccess().get_gardens_and_details()
        return {'gardens': gardens}

    def page_specific_handle_file(self, file):
        # status, message = processCourseZip(file)
        return FileHandlingResult(True, 'TODO - not implemented')


class CropMgmtView(AbstractFileUploadView):
    template_name = 'admin/crop_mgmt.html'
    crop = None

    def __init__(self):
        super(CropMgmtView, self).__init__(['.jpg', '.png', '.jpeg'], [])
        self.extra_params_on_post_only = True

    def get_page_specific_data(self):
        crops = DataAccess().get_all_crops()
        return {'crops': crops}

    def extract_extra_params(self, *args, **kwargs):
        self.crop = kwargs.pop('crop', None)
        if self.crop is not None:
            return True

        # Invalid URL:
        self.extra_params_errors += "couldn't find crop in url"
        return False

    def page_specific_handle_file(self, file):
        # status, message = processCourseZip(file)
        return FileHandlingResult(True, 'TODO - not implemented')


@staff_member_required
def add_garden(request):
    if request.method == 'POST':
        garden = request.POST.get('garden')
        width = int(request.POST.get('width'))
        height = int(request.POST.get('height'))
        DataAccess().add_garden(garden, width, height)
        return HttpResponse(json.dumps({'status': 200, 'message': 'Success'}), content_type='application/json')

    else:
        return HttpResponse(json.dumps({'status': 404, 'message': 'POST requests only'}), content_type='application/json')


@staff_member_required
def edit_garden(request):
    if request.method == 'POST':
        garden = request.POST.get('garden')
        width = int(request.POST.get('width'))
        height = int(request.POST.get('height'))
        DataAccess().edit_garden(garden, width, height)
        return HttpResponse(json.dumps({'status': 200, 'message': 'Success'}), content_type='application/json')

    else:
        return HttpResponse(json.dumps({'status': 404, 'message': 'POST requests only'}),
                            content_type='application/json')


@staff_member_required
def delete_garden(request):
    if request.method == 'POST':
        garden = request.POST.get('garden')
        DataAccess().delete_garden(garden)
        return HttpResponse(json.dumps({'status': 200, 'message': 'Success'}), content_type='application/json')

    else:
        return HttpResponse(json.dumps({'status': 404, 'message': 'POST requests only'}),
                            content_type='application/json')

@staff_member_required
def garden_plans(request, garden_name):
    plans = DataAccess().get_all_bed_plans(garden_name)
    return render(request, 'admin/garden_plans_mgmt.html', {'garden': garden_name, 'plans': plans})


@staff_member_required
def delete_garden_plan(request):
    if request.method == 'POST':
        plan_id = request.POST.get('plan_id')
        DataAccess().admin_delete_bed_plan(plan_id)
        return HttpResponse(json.dumps({'status': 200, 'message': 'Success'}), content_type='application/json')

    else:
        return HttpResponse(json.dumps({'status': 404, 'message': 'POST requests only'}),
                            content_type='application/json')


@staff_member_required
def admin_add_crop(request, new_crop):
    DataAccess().add_crop(new_crop)
    return HttpResponse(json.dumps({'status': 200, 'message': 'Success'}), content_type='application/json')


@staff_member_required
def admin_add_subtype(request):
    if request.method == 'POST':
        crop = request.POST.get('crop')
        subtype = request.POST.get('subtype')
        DataAccess().add_crop_subtype(crop, subtype)
        return HttpResponse(json.dumps({'status': 200, 'message': 'Success'}), content_type='application/json')

    else:
        return HttpResponse(json.dumps({'status': 404, 'message': 'POST requests only'}), content_type='application/json')


@staff_member_required
def admin_remove_subtype(request):
    if request.method == 'POST':
        crop = request.POST.get('crop')
        subtype = request.POST.get('subtype')
        DataAccess().remove_crop_subtype(crop, subtype)
        return HttpResponse(json.dumps({'status': 200, 'message': 'Success'}), content_type='application/json')

    else:
        return HttpResponse(json.dumps({'status': 404, 'message': 'POST requests only'}), content_type='application/json')


@staff_member_required
def admin_toggle_current_crop(request, crop, is_current):
    DataAccess().toggle_current_for_crop(crop, int(is_current))
    return HttpResponse(json.dumps({'status': 200, 'message': 'Success'}), content_type='application/json')


@staff_member_required
def admin_home(request):
    return render(request, 'admin/home.html')


@staff_member_required
def admin_course_info(request):
    links = [{'name': 'User Progress', 'link': '/pgaadmin/userProgress'},
             {'name': 'Quiz Statistics', 'link': '/pgaadmin/quizStatistics'}]

    back_link = '/pgaadmin'

    title = 'Course Information'

    return render(request, 'admin/menu.html', {'links': links, 'title': title, 'back_link': back_link})


@staff_member_required
def adminUserProgress(request, user):
    db = DataAccess()
    completed = db.getCompletedCoursesForUser(user)
    
    return render(request, 'admin/user_progress.html', {'completed_courses': completed})


@staff_member_required
def adminUserProgressOverview(request):
    db = DataAccess()
    progress = db.getAllUserProgress()
    
    completed = []
    
    for user in progress:
        num_courses = len(progress[user])
        completed.append(num_courses)
    # print(progress)
    
    user_progress = zip(progress, completed)
    return render(request, 'admin/user_progress_overview.html', {'user_progress': user_progress})


@staff_member_required
def adminQuizStatistics(request, unit):
    # TODO get quiz stats...
    return render(request, 'admin/quiz_statistics.html', {'unit': unit})


@staff_member_required
def adminQuizStatisticsOverview(request):
    db = DataAccess()
    units = db.getAllUnits()
    quiz_units = []
    for unit in units:
        if db.doesCourseHaveQuiz(unit) > 0:
            quiz_units.append(unit)
    return render(request, 'admin/quiz_statistics_overview.html', {'units': quiz_units})
    
def adminSetCourseColor(request, course, color):
    DataAccess().setCourseColor(course, color)
    return HttpResponse(json.dumps({ 'status': 200, 'message': 'Success' }), content_type='application/json')


@staff_member_required
def records_mgmt_menu(request):
    links = [{'name': 'Planting Records', 'link': '/pgaadmin/plantingRecords'},
             {'name': 'Harvest Records', 'link': '/pgaadmin/harvestRecords'},
             {'name': 'Garden Notes', 'link': '/pgaadmin/gardenNotes'}]

    back_link = '/pgaadmin/gardenMgmtMenu'

    title = 'Records Management'

    return render(request, 'admin/menu.html', {'links': links, 'title': title, 'back_link': back_link})


class AdminQuizView(AbstractFileUploadView):
        
    template_name = 'admin/quiz.html'
    unit = None
    
    def __init__(self):
        super(AdminQuizView, self).__init__( ['.csv', '.xlsx', '.xls'], [])
            
    def extract_extra_params(self, *args, **kwargs):
        self.unit = kwargs.pop('unit', None)
        if self.unit is not None:
            return True
            
        # Invalid URL:
        self.extra_params_errors = "Couldn't find unit for quiz"
        return False
    
    def get_page_specific_data(self):
        questions = DataAccess().getQuizQuestions(self.unit);
        return {'unit': self.unit, 'questions': questions}
        
    def page_specific_handle_file(self, file):
        # type of material is given by 'self.resource_type'
        add_new_quiz(self.unit, file)
        return FileHandlingResult(True, 'Quiz uploaded')
