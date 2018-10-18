import gc
import json

from django.core.serializers.json import DjangoJSONEncoder
from django.http import HttpResponse
from django.shortcuts import render

# Create your views here.
from rest_framework import status
from rest_framework.parsers import MultiPartParser
from rest_framework.response import Response
from rest_framework.views import APIView

from api.forms import EntryForm
from api.models import Entry
from api.serializers import EntrySerializer
from file_handler.forms import UploadFileForm
from file_handler.models import Img
from file_handler.views import ImgList


class EntryList(APIView):
    parser_classes = (MultiPartParser,)

    def get(self,request):
        entrys = Entry.objects.all()
        serializer = EntrySerializer(entrys)
        return Response(serializer.data)

    def post(self,request):
        entry = Entry()
        # form = UploadFileForm(request.POST, request.FILES)
        files = request.FILES.getlist('fileupload')  # 获得多个文件上传进来的文件列表。
        # if form.is_valid():  # 表单数据如果合法
        if request.data['description']:
            entry.description = request.data['description']
        if request.data['tags']:
            entry.tags = request.data['tags']
        if request.data['name']:
            entry.name = request.data['name']
        img_list = []
        if files:
            for f in files:
                img = Img(file=f)
                img.save()
                img_list.append(img.get_id())
        entry.imgs = img_list
        entry.save()

        # generating json response array
        result = [{"id": entry.id.__str__(),
                   "name": entry.name,
                   "imgs": entry.imgs,
                   "description":entry.description,
                   "tags":entry.tags,
                   "modified":entry.modified,
                   }]
        response_data = json.dumps(result,cls=DjangoJSONEncoder)

        # checking for json data type
        # big thanks to Guy Shapiro
        # if noajax:
        #     if request.META['HTTP_REFERER']:
        #         redirect(request.META['HTTP_REFERER'])

        if "application/json" in request.META['HTTP_ACCEPT_ENCODING']:
            content_type = 'application/json'
        else:
            content_type = 'text/plain'
        return HttpResponse(response_data, content_type=content_type)



def ue(request):
    return render(request,'uploadentry.html',{'form':EntryForm})