from django import forms
from .validators import create_file_validator


class UploadFileForm(forms.Form):

    def __init__(self, *args, **kwargs):
        
        if 'valid_extensions' in kwargs:
            self.valid_extensions = kwargs.pop('valid_extensions')
            self.extra_validation_funcs = kwargs.pop('extra_validation_funcs')
            file_validator = create_file_validator(self.valid_extensions, 
                self.extra_validation_funcs)
            super(UploadFileForm, self).__init__(*args, **kwargs)
            self.fields['file'].validators = [file_validator]
        
        else:
            super(UploadFileForm, self).__init__(*args, **kwargs)
    
    file = forms.FileField()