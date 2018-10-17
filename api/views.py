from django.shortcuts import render

# Create your views here.
from rest_framework.response import Response
from rest_framework.views import APIView

from api.models import Entry
from api.serializers import EntrySerializer
from file_handler.views import ImgList


class EntryList(APIView):

    def get(self,request):
        entrys = Entry.objects.all()
        serializer = EntrySerializer(entrys)
        return Response(serializer.data)

    def post(self,request):
        if request.FILES:
            instence = ImgList.post(ImgList(),request)
            imgpk = instence.get('id')



