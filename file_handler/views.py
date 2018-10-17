import json
import logging

from django.core.files.uploadedfile import UploadedFile
from django.http import Http404, HttpResponseRedirect, HttpResponse, HttpResponseBadRequest
from django.shortcuts import render, redirect, get_object_or_404

# Create your views here.
from django.urls import reverse
from rest_framework import status
from rest_framework.parsers import FileUploadParser, MultiPartParser
from rest_framework.response import Response
from rest_framework.views import APIView

from file_handler.forms import UploadFileForm
from file_handler.models import Img
from file_handler.serializers import ImgSerializer
from django.utils.translation import ugettext as _

from file_handler.utils import get_thumbnail

log = logging

class ImgList(APIView):

    """
    list all images, or create a new image.
    """
    parser_classes = (MultiPartParser,)

    def get(self,request):
        images = Img.objects.all()
        serializer = ImgSerializer(images,many=True)
        return Response(serializer.data)

    def post(self,request):
        serializer = ImgSerializer()
        if request.method == 'POST':
            form = UploadFileForm(request.POST,request.FILES)
            if form.is_valid():
                instance = form.save()
                serializer = ImgSerializer(instance)
            return Response(serializer.data,status=status.HTTP_201_CREATED)
        else:
            return Response(serializer.errors,status=status.HTTP_400_BAD_REQUEST)


class ImgDetail(APIView):
    """
    Retrieve, update or delete a Img instance.
    """
    def get_object(self, pk):
        try:
            return Img.objects.get(pk=pk)
        except Img.DoesNotExist:
            raise Http404

    def get(self,request, pk, format=None):
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


def fileupload(request,noajax=False):
    """
    Main Multiuploader module.
    Parses data from jQuery plugin and makes database changes.
    """
    if request.method == 'POST':
        log.info('received POST to main multiuploader view')

        if request.FILES is None:
            response_data = [{"error": _('Must have files attached!')}]
            return HttpResponse(json.dumps(response_data))

        # if not u'form_type' in request.POST:
        #     response_data = [{"error": _("Error when detecting form type, form_type is missing")}]
        #     return HttpResponse(json.dumps(response_data))

        file = request.FILES[u'file']
        wrapped_file = UploadedFile(file)
        filename = wrapped_file.name
        file_size = wrapped_file.file.size

        log.info('Got file: "%s"' % filename)

        # writing file manually into model
        # because we don't need form of any type.

        fl = Img()
        fl.filename = filename
        fl.file = file
        fl.save()

        log.info('File saving done')

        thumb_url = ""

        try:
            thumb_url = get_thumbnail(fl.file, "80x80", quality=50)
        except Exception as e:
            log.error(e)

        # generating json response array
        result = [{"id": fl.id.__str__(),
                   "name": filename,
                   "size": file_size,
                   "url": fl.file.path.__str__(),
                   "thumbnail_url": thumb_url,
                   "delete_url": reverse('multiuploader_delete', args=[fl.pk]),
                   "delete_type": "POST", }]

        response_data = json.dumps(result)

        # checking for json data type
        # big thanks to Guy Shapiro
        if noajax:
            if request.META['HTTP_REFERER']:
                redirect(request.META['HTTP_REFERER'])

        if "application/json" in request.META['HTTP_ACCEPT_ENCODING']:
            content_type = 'application/json'
        else:
            content_type = 'text/plain'
        return HttpResponse(response_data, content_type=content_type)
    else:  # GET
        return HttpResponse('Only POST accepted')


def multiuploader_delete(request, pk):
    if request.method == 'POST':
        log.info('Called delete file. File id=' + str(pk))
        fl = get_object_or_404(Img, pk=pk)
        fl.delete()
        log.info('DONE. Deleted file id=' + str(pk))

        return HttpResponse(1)

    else:
        log.info('Received not POST request to delete file view')
        return HttpResponseBadRequest('Only POST accepted')

