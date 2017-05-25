from django.core.serializers import json
from django.http import HttpResponse, Http404
from pga.dataAccess import DataAccess
import json

def edit_quiz_question(request):
    if request.method == 'POST':
    
        questionid = request.POST.get('questionid')
        newquestion = request.POST.get('newquestion')
        
        db = DataAccess()
        
        db.editQuestionTitle(questionid, newquestion)
        
        response = {
            'status': 200,
            'message': 'Successfully updated quiz'
        }
    else:
        response = {
            'status': 404,
            'message': 'Invalid request'
        }
    return HttpResponse(json.dumps(response), content_type='application/json')
    
def edit_quiz_answer(request):
    if request.method == 'POST':
    
        answerid = request.POST.get('answerid')
        newanswer = request.POST.get('newanswer')
        iscorrectStr = request.POST.get('iscorrect')
        
        #Getting bool's from ajax don't convert to python bools. fun.
        iscorrect = False
        if iscorrectStr == u'true':
            iscorrect = True
        
        db = DataAccess()
        print(iscorrect)
        db.editAnswer(answerid, newanswer, iscorrect)
        
        response = {
            'status': 200,
            'message': 'Successfully updated quiz'
        }
    else:
        response = {
            'status': 404,
            'message': 'Invalid request'
        }
    return HttpResponse(json.dumps(response), content_type='application/json')