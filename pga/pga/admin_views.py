from pga.abstract_upload_view import *
from pga.dataAccess import DataAccess
from pga.coursemanager import *

#Displays all units, allowing users to delete them, upload another,
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
        
#Displays all lessons in a given unit, allowing users to delete them, upload more,
# or go to the unit quiz
class AdminUnitView(AbstractFileUploadView):
    
    template_name = 'admin/unit.html'
    unit = None
    
    def __init__(self):
        super(AdminUnitView, self).__init__( ['.html'], [])
        
    def extract_extra_params(self, *args, **kwargs):
        self.unit = kwargs.pop('unit', None)
        if self.unit is not None:
            return True
            
        #Invalid URL:
        if self.unit is None:
            self.extra_params_errors += 'Valid unit not found'
        return False
    
    def get_page_specific_data(self):
        #Ensures 'self.unit' is set before this code is reached
        lessons = DataAccess().getCourseLessons(self.unit)
        return { 'lessons': lessons, 'unit': self.unit }
        
    def page_specific_handle_file(self, file):
        return FileHandlingResult(True, 'TODO - not implemented')
        
#Renders info for a given lesson. Gives option to download lesson 
# or upload a replacement
class AdminLessonView(AbstractFileUploadView):
    
    template_name = 'admin/lesson.html'
    unit = None
    lesson = None
    
    def __init__(self):
        super(AdminLessonView, self).__init__( ['.html'], [])
            
    def extract_extra_params(self, *args, **kwargs):
        self.unit = kwargs.pop('unit', None)
        self.lesson = kwargs.pop('lesson', None)
        if self.unit is not None and self.lesson is not None:
            return True
            
        #Invalid URL:
        if self.unit is None:
            self.extra_params_errors += 'Valid unit not found'
        if self.lesson is None:
            self.extra_params_errors += 'Valid lesson not found'
        return False
    
    def get_page_specific_data(self):
        #Ensures 'self.unit' & 'self.lesson' is set before this code is reached
        return { 'lesson': self.lesson, 'unit': self.unit }
        
    def page_specific_handle_file(self, file):
        return FileHandlingResult(True, 'TODO - not implemented')
        
        
#Renders info for a given lesson. Gives option to download lesson 
# or upload a replacement
class AdminSuppMatView(AbstractFileUploadView):
    
    template_name = 'admin/supplementary_materials.html'
    
    def __init__(self):
        super(AdminSuppMatView, self).__init__( [], [])
            
    def extract_extra_params(self, *args, **kwargs):
        self.resource_type = kwargs.pop('resource_type', None)
        if self.resource_type is not None:
            if self.resource_type == 'PDF':
                self.valid_file_extensions = ['.pdf']
            elif self.resource_type == 'Image':
                #TODO find more image extensions
                self.valid_file_extensions = ['.jpg', '.jpeg', '.png', '.tiff', '.gif']
            elif self.resource_type == 'Video':
                #TODO find more video extensions
                self.valid_file_extensions = ['.mp4']
            else:
                self.extra_params_errors += self.resource_type + " is not a valid resource type"
            return True
            
        #Invalid URL:
        return False
    
    def get_page_specific_data(self):
        #Ensures 'self.resource_type' is set before reaching here
        #TODO - get actual resources
        resources = [{'name': 'Fake ' + self.resource_type + ' 1'},
                    {'name': 'Fake ' + self.resource_type + ' 2'}]
        return { 'resource_type': self.resource_type, 'resources': resources }
        
    def page_specific_handle_file(self, file):
        # type of material is given by 'self.resource_type'
        return FileHandlingResult(True, 'TODO - not implemented')
        
        
#Simply returns the index page of supp mat's, listing the types, not actual files
@staff_member_required
def adminSupplementaryMaterials(request):
    return render(request, 'admin/supplementary_materials.html', {'index': True});
        
        
