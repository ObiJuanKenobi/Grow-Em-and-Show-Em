from django.core.serializers import json
from django.http import HttpResponse, Http404
from django.shortcuts import render, redirect

from pga.dataAccess import DataAccess

import json


def admin_planting_records(request):
    db = DataAccess()

    view_dict = {'title': 'Planting Records', 'records': db.get_planting_records(), 'has_notes': False,
                     'delete_url': '/pgaadmin/deletePlantingRecord'}
    return render(request, 'admin/records.html', view_dict)


def admin_harvest_records(request):
    db = DataAccess()

    view_dict = {'title': 'Harvest Records', 'records': db.get_harvest_records(), 'has_notes': False,
                     'delete_url': '/pgaadmin/deleteHarvestRecord'}
    return render(request, 'admin/records.html', view_dict)


def admin_garden_notes(request):
    db = DataAccess()

    view_dict = {'title': 'Garden Notes', 'records': db.get_garden_notes(), 'has_notes': True,
                     'delete_url': '/pgaadmin/deleteGardenNote'}
    return render(request, 'admin/records.html', view_dict)


def delete_planting_record(request, record_id):
    if request.method == 'POST':

        db = DataAccess()

        db.delete_planting_record(int(record_id))

        response = {
            'status': 200,
            'message': 'Successfully deleted record'
        }
    else:
        response = {
            'status': 404,
            'message': 'Invalid request'
        }
    return HttpResponse(json.dumps(response), content_type='application/json')


def delete_harvest_record(request, record_id):
    if request.method == 'POST':

        db = DataAccess()

        db.delete_harvest_record(record_id)

        response = {
            'status': 200,
            'message': 'Successfully deleted record'
        }
    else:
        response = {
            'status': 404,
            'message': 'Invalid request'
        }
    return HttpResponse(json.dumps(response), content_type='application/json')


def delete_garden_note(request, record_id):
    print("DELETE GARDEN--NOTE")
    if request.method == 'POST':

        db = DataAccess()

        db.delete_garden_note(int(record_id))
        print("Here")

        response = {
            'status': 200,
            'message': 'Successfully deleted record'
        }
    else:
        response = {
            'status': 404,
            'message': 'Invalid request'
        }
    return HttpResponse(json.dumps(response), content_type='application/json')