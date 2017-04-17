from django.views.generic import TemplateView
from django.http import HttpResponse, Http404
from django.shortcuts import render, redirect
from django.utils.decorators import method_decorator
from django.contrib.admin.views.decorators import staff_member_required

from pga.upload_file_form import UploadFileForm

@method_decorator(staff_member_required, name='dispatch')
class AbstractFileUploadView(TemplateView):

    template_name = "abstract.html"
    
    def __init__(self, valid_file_extensions, extra_validation_funcs):
        self.valid_file_extensions = valid_file_extensions
        self.extra_validation_funcs = extra_validation_funcs
        self.form = UploadFileForm()
        self.uploading = False 
        self.upload_status = ''
        self.upload_success = False
        self.extra_params_errors = ''
    
    def get(self, request, *args, **kwargs):
        self.uploading = False
        
        #Ensure correct URL, get extra parameters 
        if not self.extract_extra_params(*args, **kwargs):
            return render(request, self.template_name, 
                    {'extra_params_errors': self.extra_params_errors})
                    
        data_dict = self.get_data_dict()
        return render(request, self.template_name, data_dict)
        
    def post(self, request, *args, **kwargs):
        self.uploading = True
        
        #Ensure correct URL, get extra parameters 
        if not self.extract_extra_params(*args, **kwargs):
            return render(request, self.template_name, 
                    {'extra_params_errors': self.extra_params_errors})
                    
        self.form = UploadFileForm(request.POST, request.FILES,
                        valid_extensions = self.valid_file_extensions,
                        extra_validation_funcs = self.extra_validation_funcs)
        
        if self.form.is_valid():
            file_handle_result = self.page_specific_handle_file(request.FILES['file'])
            self.upload_success = file_handle_result.is_success
            self.upload_status = file_handle_result.handling_msg
        else:
            self.upload_status = self.form.errors['file'][0]
            self.upload_success = False
            
        data_dict = self.get_data_dict()
        return render(request, self.template_name, data_dict)
        
    def get_data_dict(self):
        data_dict = { 'form': self.form,
                'uploading': self.uploading,
                'upload_success': self.upload_success,
                'upload_status': self.upload_status }
        data_dict.update(self.get_page_specific_data())
        return data_dict
            
    def get_page_specific_data(self):
        raise NotImplementedError("Implement this method to return a dict of page-specific info")
        
    def page_specific_handle_file(self, file):
        raise NotImplementedError("Implement this method to handle the expected file upload and return a FileHandlingResult object")
        
    #If a view should have extra incoming parameters, override this method 
    # to extract them into the appropriate instance variables
    # If they aren't set, populate 'self.extra_params_errors' accordingly 
    # & return false
    def extract_extra_params(self, *args, **kwargs):
        return True
        
        
class FileHandlingResult:
    #if File uploaded successfully, use True for is_success and 'Uploaded Successfully' for msg
    #else use False and a specific error message
    def __init__(self, is_success, handling_msg):
        self.is_success = is_success 
        self.handling_msg = handling_msg
        
