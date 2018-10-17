from django.db import models

# Create your models here.
from django.utils import timezone

from file_handler.models import Img


class BaseEntry(models.Model):
    id = models.AutoField(primary_key=True)
    created = models.DateField(editable=False)
    modified = models.DateField()

    def save(self,*args,**kwargs):
        if not self.id:
            self.created = timezone.now()
        self.modified = timezone.now()
        return super(BaseEntry,self).save(*args,**kwargs)

class Entry(BaseEntry):
    name = models.CharField(max_length=255)
    tags = models.CharField(max_length=255)
    imgs = models.ManyToManyField(Img,null=True)
    description = models.TextField(blank=True)