from rest_framework import serializers

from api.models import Entry


class EntrySerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Entry
        exclude = ('created','modified')