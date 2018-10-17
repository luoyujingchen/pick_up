from django.forms import ModelForm

from api.models import Entry


class EntryForm(ModelForm):
    class Meta:
        model = Entry
        exclude = ['imgs','modified','created']