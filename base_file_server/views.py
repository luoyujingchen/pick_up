import json

from django.core.serializers.json import DjangoJSONEncoder
from django.http import HttpResponse
from django.shortcuts import render

# Create your views here.
from rest_framework import status

from base_file_server.models import TypeImg


def deal_with_img(request):
    if request.method == 'POST':
        if request.FILES['img']:
            img = TypeImg(file=request.FILES['img'])
            img.save()

            result = [{
                'id': img.pk,
                'url': img.file.url,
                'modified':img.modified
            }]

            response_data = json.dumps(result,cls=DjangoJSONEncoder)
            return HttpResponse(response_data,status=status.HTTP_201_CREATED)
        else:
            result = [{
                'error':'no file uploaded.'
            }]
            response_data = json.dumps(result)
            return HttpResponse(response_data,status=status.HTTP_400_BAD_REQUEST)
    elif request.method == 'GET':
        """
        get img's url by pk.
        """
        if request.GET['pk']:
            img = TypeImg.objects.get(pk=request.GET['pk'])
            result = [{
                'id': img.pk,
                'url': img.file.url,
                'modified': img.modified
            }]
            response_data = json.dumps(result, cls=DjangoJSONEncoder)
            return HttpResponse(response_data, status=status.HTTP_200_OK)
        else:
            result = [{
                'error': 'need parameter pk.'
            }]
            response_data = json.dumps(result)
            return HttpResponse(response_data, status=status.HTTP_400_BAD_REQUEST)
    else:
        result = [{
            'error': 'wrong method.'
        }]
        response_data = json.dumps(result)
        return HttpResponse(response_data, status=status.HTTP_400_BAD_REQUEST)


def test_upload(request):
    return render(request, 'bfs_upload.html')
