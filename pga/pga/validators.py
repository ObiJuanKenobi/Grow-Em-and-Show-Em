import os
from django.core.exceptions import ValidationError


def create_file_validator(valid_extensions_list, extra_validation_functions = []):

    def validate_file(value):
        ext = os.path.splitext(value.name)[1]  # [0] returns path+filename
        if not ext.lower() in valid_extensions_list:
            error_msg = 'Unsupported file extension - expected: '
            
            first = True
            for ext in valid_extensions_list:
                if not first:
                    error_msg += ', '
                error_msg += ext
                first = False
            raise ValidationError(error_msg)
            
        for func in extra_validation_functions:
            func(value)
    
    return validate_file
            
        