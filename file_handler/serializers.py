from rest_framework import serializers

from file_handler.models import Img


class ImgSerializer(serializers.HyperlinkedModelSerializer):
    file = serializers.FileField(use_url=True)
    class Meta:
        model = Img
        fields = ('id','upload_time','update_time','file')



