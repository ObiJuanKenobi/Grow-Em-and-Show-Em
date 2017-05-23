from django.http import HttpResponse, Http404
from pga.abstract_upload_view import *
from pga.dataAccess import DataAccess
from pga.coursemanager import *
import json

# Displays all units, allowing users to delete them, upload another,
# go to a unit's lessons, or go to supplementary materials
class CourseMgmtView(AbstractFileUploadView):
    
    template_name = 'admin/course_mgmt.html'
    
    def __init__(self):
        super(CourseMgmtView, self).__init__( ['.zip'], [])
    
    def get_page_specific_data(self):
        courses = DataAccess().getCourses()
        return { 'courses': courses }
        
    def page_specific_handle_file(self, file):
        status, message = processCourseZip(file)
        return FileHandlingResult(status, message)
        
# Displays all lessons in a given unit, allowing users to delete them, upload more,
# or go to the unit quiz
class AdminUnitView(AbstractFileUploadView):
    
    template_name = 'admin/unit.html'
    unit = None
    
    def __init__(self):
        super(AdminUnitView, self).__init__( ['.zip'], [])
        
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
            last_slash_index = resource.rfind('\\')
            resource_name = resource[last_slash_index+1:]
            resources_list.append({'path': resource_path, 'name': resource_name})
        
        return {'unit': self.unit, 'resources': resources_list}
        
    def page_specific_handle_file(self, file):
        # type of material is given by 'self.resource_type'
        return FileHandlingResult(True, 'TODO - not implemented')


@staff_member_required
def garden_mgmt_menu(request):
    return render(request, 'admin/gardenMgmtMenu.html')


@staff_member_required
def admin_crop_mgmt(request):
    crops = DataAccess().get_all_crops()
    return render(request, 'admin/crop_mgmt.html', {'crops': crops})

@staff_member_required
def admin_add_crop(request, new_crop):
    DataAccess().add_crop(new_crop)
    return HttpResponse(json.dumps({'status': 200, 'message': 'Success'}), content_type='application/json')

@staff_member_required
def admin_toggle_current_crop(request, crop, is_current):
    DataAccess().toggle_current_for_crop(crop, int(is_current))
    return HttpResponse(json.dumps({'status': 200, 'message': 'Success'}), content_type='application/json')

@staff_member_required
def adminHome(request):
    return render(request, 'admin/home.html')


@staff_member_required
def adminCourseInfo(request):
    return render(request, 'admin/course_info.html')

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
    #print(progress)
    
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

class AdminQuizView(AbstractFileUploadView):
        
    template_name = 'admin/quiz.html'
    unit = None
    
    def __init__(self):
        super(AdminQuizView, self).__init__( ['.csv', '.xlsx', '.xls'], [])
            
    def extract_extra_params(self, *args, **kwargs):
        self.unit = kwargs.pop('unit', None)
        if self.unit is not None:
            return True
            
        #Invalid URL:
        self.extra_params_errors = "Couldn't find unit for quiz"
        return False
    
    def get_page_specific_data(self):
        #Ensures 'self.unit'
        questions = DataAccess().getQuizQuestions(self.unit);
        return {'unit': self.unit, 'questions': questions}
        
    def page_specific_handle_file(self, file):
        # type of material is given by 'self.resource_type'
        return FileHandlingResult(True, 'TODO - not implemented')
