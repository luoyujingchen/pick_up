from rest_framework import serializers

from file_handler.models import Img


class ImgSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Img
        fields = ('id','description','upload_time','update_time','file')