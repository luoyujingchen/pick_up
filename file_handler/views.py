from django.http import Http404
from django.shortcuts import render

# Create your views here.
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView

from file_handler.models import Img
from file_handler.serializers import ImgSerializer


class ImgList(APIView):
    """
    list all images, or create a new image.
    """
    def get(self,request):
        images = Img.objects.all()
        serializer = ImgSerializer(images,many=True)
        return Response(serializer.data)

    def post(self,request):
        serializer = ImgSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data,status=status.HTTP_201_CREATED)
        return Response(serializer.errors,status=status.HTTP_400_BAD_REQUEST)

# https://blog.vivekshukla.xyz/uploading-file-using-api-django-rest-framework/
class ImgDetail(APIView):
    """
    Retrieve, update or delete a Img instance.
    """
    def get_object(self, pk):
        try:
            return Img.objects.get(pk=pk)
        except Img.DoesNotExist:
            raise Http404

    def get(self, request, pk, format=None):
        image = self.get_object(pk)
        serializer = ImgSerializer(image)
        return Response(serializer.data)

    def put(self, request, pk, format=None):
        image = self.get_object(pk)
        serializer = ImgSerializer(image, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk, format=None):
        image = self.get_object(pk)
        image.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


def upload(request):
    return render(request,'upload.html')