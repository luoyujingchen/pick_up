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
        serializer = EntrySerializer()
        form = UploadFileForm(request.POST, request.FILES)
        files = request.FILES.getlist('fileupload')  # 获得多个文件上传进来的文件列表。
        if form.is_valid():  # 表单数据如果合法
            for f in files:
                img = Img(file=f)
                img.save()
                entry.imgs.add(img)
            if form.cleaned_data['description']:
                entry.description = form.changed_data['description']
            if form.cleaned_data['tags']:
                entry.tags = form.cleaned_data['tags']
            if form.cleaned_data['name']:
                entry.name = form.cleaned_data['name']
            serializer = EntrySerializer(entry)
            if serializer.is_valid():
                return Response(serializer.data,status=status.HTTP_201_CREATED)
            else:
                return Response(serializer.errors,status=status.HTTP_400_BAD_REQUEST)
        else:
            return Response(form.errors,status=status.HTTP_400_BAD_REQUEST)


def ue(request):
    return render(request,'uploadentry.html',{'form':EntryForm})